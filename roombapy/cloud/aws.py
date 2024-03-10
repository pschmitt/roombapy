"""Generate AWSv4 signature headers.

Code is partially borrowed from tedder/requests-aws4auth (MIT licensed)
"""

from __future__ import annotations

import datetime
import hashlib
import hmac
import posixpath
import re
import shlex
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import parse_qs, quote, unquote, urlparse

DEFAULT_HEADERS = frozenset({"host", "content-type", "date", "x-amz-*"})
DEFAULT_IROBOT_HEADERS = frozenset({"host", "date", "x-amz-*"})

Headers = dict[str, str]


def normalize_whitespace(text: str) -> str:
    """Replace runs of whitespace with a single space.

    Ignore text enclosed in quotes.
    """
    if re.search(r"\s", text):
        return " ".join(shlex.split(text, posix=False))
    return text


def _canonicalize_query_string(query_string: str) -> str:
    """Parse and format querystring as per AWS4 auth requirements.

    Perform percent quoting as needed.
    """
    safe_qs_unresvd = "-_.~"
    space = " "
    query_string = query_string.split(space)[0]
    # prevent parse_qs from interpreting semicolon as an alternative
    # delimiter to ampersand
    query_string = query_string.replace(";", "%3B")
    qs_items = {}
    for name, vals in parse_qs(query_string, keep_blank_values=True).items():
        key = quote(name, safe=safe_qs_unresvd)
        values = [quote(val, safe=safe_qs_unresvd) for val in vals]
        qs_items[key] = values

    return "&".join(
        [
            f"{name}={value}"
            for name, values in sorted(qs_items.items())
            for value in sorted(values)
        ]
    )


def _canonicalize_path(request_path: str, service: str) -> str:
    """Generate the canonical path as per AWS4 auth requirements.

    Not documented anywhere, determined from aws4_testsuite examples,
    problem reports and testing against the live services.
    """
    safe_chars = "/~"
    qs = ""
    fixed_path = request_path
    if "?" in fixed_path:
        fixed_path, qs = fixed_path.split("?", 1)
    fixed_path = posixpath.normpath(fixed_path)
    fixed_path = re.sub("/+", "/", fixed_path)
    if request_path.endswith("/") and not fixed_path.endswith("/"):
        fixed_path += "/"
    full_path = fixed_path
    # S3 seems to require unquoting first. 'host' service is used in
    # amz_testsuite tests
    if service in ["s3", "host"]:
        full_path = unquote(full_path)
    full_path = quote(full_path, safe=safe_chars)
    if qs:
        qm = "?"
        full_path = qm.join((full_path, qs))
    return full_path


def _get_canonical_headers(
    url: str, headers: Headers, include_header_names: Iterable[str]
) -> tuple[str, str]:
    """Generate the Canonical Headers section of the Canonical Request.

    :param url: URL to get Host header
    :param headers: Existing request headers
    :param include_header_names: List of headers to include in the canonical
           and signed headers. It's primarily included to allow testing against
           specific examples from Amazon. If omitted or None it includes host,
           content-type and any header starting 'x-amz-' except for
           x-amz-client context, which appears to break mobile analytics auth
           if included. Except for the x-amz-client-context exclusion these
           defaults are per the AWS documentation.

    :returns: Canonical Headers and the Signed Headers strs as a tuple
             (canonical_headers, signed_headers).
    """
    include = [x.lower() for x in include_header_names]
    headers = headers.copy()
    # Temporarily include the host header - AWS requires it to be included
    # in the signed headers, but Requests doesn't include it in a
    # PreparedRequest
    if "host" not in headers:
        headers["host"] = urlparse(str(url)).netloc.split(":")[0]
    # Aggregate for upper/lowercase header name collisions in header names,
    # AMZ requires values of colliding headers be concatenated into a
    # single header with lowercase name.  Although this is not possible with
    # Requests, since it uses a case-insensitive dict to hold headers, this
    # is here just in case you duck type with a regular dict
    canonical_headers: dict[str, list[str]] = {}
    for header, value in headers.items():
        hdr = header.strip().lower()
        val = normalize_whitespace(value).strip()
        if (
            hdr in include
            or "*" in include
            or (
                "x-amz-*" in include
                and hdr.startswith("x-amz-")
                and hdr != "x-amz-client-context"
            )
        ):
            vals = canonical_headers.setdefault(hdr, [])
            vals.append(val)
    # Flatten cano_headers dict to string and generate signed_headers
    cano_headers = ""
    signed_headers_list = []
    for hdr in sorted(canonical_headers):
        vals = canonical_headers[hdr]
        val = ",".join(sorted(vals))
        cano_headers += f"{hdr}:{val}\n"
        signed_headers_list.append(hdr)
    signed_headers = ";".join(signed_headers_list)
    return cano_headers, signed_headers


def _get_signature(amz_date: str, canonical_request: str, scope: str) -> bytes:
    """Generate the AWS4 auth signature to sign for the request.

    :param amz_date: Date this request is valid for
    :param canonical_request: The Canonical Request
    :param scope: Request scope:
    :returns: Signature
    """
    hsh = hashlib.sha256(canonical_request.encode())
    sig_items = ["AWS4-HMAC-SHA256", amz_date, scope, hsh.hexdigest()]
    return "\n".join(sig_items).encode("utf-8")


def _get_canonical_request(
    canonical_headers: str,
    signed_headers: str,
    service: str,
    raw_url: str,
    method: str,
    payload_hash: str,
) -> str:
    """Create the AWS authentication Canonical Request string."""
    url = urlparse(raw_url)
    path = _canonicalize_path(url.path, service)
    # AWS handles "extreme" query strings differently to urlparse
    # (see post-vanilla-query-nonunreserved test in aws_testsuite)
    split = raw_url.split("?", 1)
    query_string = split[1] if len(split) == 2 else ""
    query_string = _canonicalize_query_string(query_string)
    request_parts = [
        method.upper(),
        path,
        query_string,
        canonical_headers,
        signed_headers,
        payload_hash,
    ]
    return "\n".join(request_parts)


@dataclass
class SigningKey:
    """AWS signing key. Used to sign AWS authentication strings."""

    scope: str
    key: bytes

    @classmethod
    def from_credentials(
        cls,
        *,
        secret_key: str,
        region: str,
        service: str,
    ) -> SigningKey:
        """Construct signing key from credentials."""

        def _sign(k: bytes, msg: str) -> bytes:
            """Generate an SHA256 HMAC, encoding msg to UTF-8."""
            return hmac.new(k, msg.encode("utf-8"), hashlib.sha256).digest()

        aws_dt = datetime.datetime.now(tz=datetime.UTC).strftime("%Y%m%d")

        init_key = ("AWS4" + secret_key).encode("utf-8")
        date_key = _sign(init_key, aws_dt)
        region_key = _sign(date_key, region)
        service_key = _sign(region_key, service)
        key = _sign(service_key, "aws4_request")

        scope = f"{aws_dt}/{region}/{service}/aws4_request"

        return SigningKey(scope=scope, key=key)


def generate_aws_headers(
    *,
    url: str,
    method: str,
    request_headers: Headers,
    service: str,
    access_id: str,
    signing_key: SigningKey,
    session_token: str | None,
    payload: str | None = None,
    include_headers: Iterable[str] = DEFAULT_IROBOT_HEADERS,
) -> Headers:
    """Client-agnostic helper to generate AWSv4 signature.

    :param url: Full request URL
    :param method: Request method
    :param service: AWS service the key is scoped for
    :param access_id: AWS access ID
    :param session_token: STS temporary credentials
    :param signing_key: An SigningKey instance.
    :param request_headers: Headers for this request
    :param payload: Payload to be signed
    :param include_headers: Headers to be signed
    :return: Headers for HTTP client
    """
    aws_headers = {}

    now = datetime.datetime.now(tz=datetime.UTC)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    aws_headers["x-amz-date"] = amz_date

    if payload is not None:
        content_hash = hashlib.sha256(payload.encode())
    else:
        content_hash = hashlib.sha256(b"")
    payload_hash = content_hash.hexdigest()

    aws_headers["x-amz-content-sha256"] = payload_hash
    if session_token:
        aws_headers["x-amz-security-token"] = session_token

    # generate signature
    result = _get_canonical_headers(url, request_headers, include_headers)
    canonical_headers, signed_headers = result
    cano_req = _get_canonical_request(
        canonical_headers, signed_headers, service, url, method, payload_hash
    )
    signature = _get_signature(amz_date, cano_req, signing_key.scope)
    hsh = hmac.new(signing_key.key, signature, hashlib.sha256)
    sig = hsh.hexdigest()
    auth_str = "AWS4-HMAC-SHA256 "
    auth_str += f"Credential={access_id}/{signing_key.scope}, "
    auth_str += f"SignedHeaders={signed_headers}, "
    auth_str += f"Signature={sig}"
    aws_headers["Authorization"] = auth_str
    return {**request_headers, **aws_headers}
