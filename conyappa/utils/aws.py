import json

from django.conf import settings

import boto3
from botocore.response import StreamingBody


def get_client(service_name):
    return boto3.client(
        service_name=service_name,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )


def get_arn(service_name, resource_name, omit_region_name=False, omit_account_id=False, path=""):
    elements = [
        "arn",
        settings.AWS_PARTITION,
        service_name,
        "" if omit_region_name else settings.AWS_REGION_NAME,
        "" if omit_account_id else settings.AWS_ACCOUNT_ID,
        resource_name,
    ]

    base_arn = ":".join(elements)
    return base_arn + path


def access_json(obj, key):
    data = obj[key]

    if isinstance(data, StreamingBody):
        data = data.read()

    return json.loads(data)
