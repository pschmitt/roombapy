"""Authentication flow for iRobot cloud."""

from __future__ import annotations

import logging

import requests

from roombapy.cloud.models import login as models

logger = logging.getLogger(__name__)

TIMEOUT = 10
APPLICATION_ID = "ANDROID-C7FB240E-DF34-42D7-AE4E-A8C17079A294"
DISCOVERY_URL = (
    "https://disc-prod.iot.irobotapi.com/v1/discover/endpoints?country_code=US"
)
GIGYA_LOGIN_URL_TEMPLATE = "https://accounts.%s/accounts.login"
IROBOT_LOGIN_ENDPOINT = "/v2/login"

LoginResponse = tuple[models.Deployment, models.IRobotLoginResponse]


def login(username: str, password: str) -> LoginResponse:
    """Obtain access credentials and robots' details from cloud."""
    response = requests.get(DISCOVERY_URL, timeout=TIMEOUT)
    deployments = models.DeploymentsResponse.from_json(response.text)
    deployment = deployments.deployments[deployments.current_deployment]
    gigya = deployments.gigya

    gigya_login_url = GIGYA_LOGIN_URL_TEMPLATE % gigya.datacenter_domain
    gigya_login_payload = {
        "apiKey": gigya.api_key,
        "loginID": username,
        "password": password,
        "format": "json",
        "targetEnv": "mobile",
    }
    response = requests.post(
        gigya_login_url, data=gigya_login_payload, timeout=TIMEOUT
    )
    gigya_response = models.GigyaLoginResponse.from_json(response.text)

    irobot_login_url = f"{deployment.http_base}{IROBOT_LOGIN_ENDPOINT}"
    irobot_login_payload = {
        "app_id": APPLICATION_ID,
        "assume_robot_ownership": "0",
        "gigya": {
            "signature": gigya_response.signature,
            "timestamp": gigya_response.signature_timestamp,
            "uid": gigya_response.user_id,
        },
    }
    response = requests.post(
        irobot_login_url, json=irobot_login_payload, timeout=TIMEOUT
    )
    irobot_response = models.IRobotLoginResponse.from_json(response.text)

    return deployment, irobot_response
