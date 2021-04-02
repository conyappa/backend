import random as rd

from django.conf import settings

from . import aws


def fetch_verifiable_seed():
    lambda_client = aws.get_client(service_name="lambda")
    response = lambda_client.invoke(FunctionName=settings.AWS_RANDOM_SEED_LAMBDA)

    payload = aws.access_json(obj=response, key="Payload")
    body = aws.access_json(obj=payload, key="body")

    return body["value"]


def get_generator():
    try:
        value = fetch_verifiable_seed()
        rd.seed(value)
        return rd

    except Exception:
        # Alternative random generator that uses os.urandom.
        return rd.SystemRandom()
