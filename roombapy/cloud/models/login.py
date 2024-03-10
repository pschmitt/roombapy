"""DTOs for login."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime  # noqa: TCH003 — mashumaro need this in runtime

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class AWSCredentials(DataClassORJSONMixin):
    """AWS credentials to query iRobot cloud API."""

    access_key: str = field(metadata=field_options(alias="AccessKeyId"))
    secret_key: str = field(metadata=field_options(alias="SecretKey"))
    session_token: str = field(metadata=field_options(alias="SessionToken"))
    expiration: datetime = field(metadata=field_options(alias="Expiration"))


@dataclass
class Deployment(DataClassORJSONMixin):
    """Active deployment of iRobot services."""

    aws_region: str = field(metadata=field_options(alias="awsRegion"))
    http_base: str = field(metadata=field_options(alias="httpBase"))
    http_base_auth: str = field(metadata=field_options(alias="httpBaseAuth"))


@dataclass
class GigyaData(DataClassORJSONMixin):
    """Gigya service discovery."""

    api_key: str
    datacenter_domain: str


@dataclass
class DeploymentsResponse(DataClassORJSONMixin):
    """iRobot service discovery."""

    deployments: dict[str, Deployment]
    current_deployment: str
    gigya: GigyaData


@dataclass
class GigyaLoginResponse(DataClassORJSONMixin):
    """User profile."""

    error_code: int
    api_version: int
    status_code: int
    status_reason: str
    user_id: str
    signature: str
    signature_timestamp: str
    is_active: bool
    is_registered: bool
    is_verified: bool

    class Config(BaseConfig):
        """Camel-case all fields."""

        aliases: dict[str, str] = {  # noqa: RUF012 — conflicts with mypy
            "error_code": "errorCode",
            "api_version": "apiVersion",
            "status_code": "statusCode",
            "status_reason": "statusReason",
            "user_id": "UID",
            "signature": "UIDSignature",
            "signature_timestamp": "signatureTimestamp",
            "is_active": "isActive",
            "is_registered": "isRegistered",
            "is_verified": "isVerified",
        }


@dataclass
class CloudRobotInfo(DataClassORJSONMixin):
    """Connected iRobot device."""

    firmware: str = field(metadata=field_options(alias="softwareVer"))
    robot_name: str = field(metadata=field_options(alias="name"))
    sku: str
    capabilities: dict[str, int] = field(metadata=field_options(alias="cap"))
    password: str


@dataclass
class IRobotLoginResponse(DataClassORJSONMixin):
    """Access credentials and connected devices."""

    credentials: AWSCredentials
    robots: dict[str, CloudRobotInfo]
