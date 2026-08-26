"""TLS setup shared by the MQTT client and password retrieval.

The posture here is deliberately permissive and must stay that way: these
robots present self-signed certificates, negotiate small Diffie-Hellman
parameters, and older firmware needs legacy renegotiation. Tightening any of
it breaks real devices.
"""

from __future__ import annotations

import ssl


def generate_tls_context() -> ssl.SSLContext:
    """Build the SSL context a Roomba will accept."""
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.set_ciphers("DEFAULT:!DH")
    ssl_context.load_default_certs()
    # Some robots require legacy renegotiation; without this the handshake
    # fails outright against OpenSSL 3.
    ssl_context.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)
    return ssl_context
