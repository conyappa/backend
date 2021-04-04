import random as random_
from logging import getLogger

from django.conf import settings

from utils import aws

logger = getLogger(__name__)


class _container:
    pass


def fetch_seed():
    client = aws.get_client(service_name="lambda")
    response = client.invoke(FunctionName=settings.AWS_RANDOM_SEED_LAMBDA)

    payload = aws.access_json(obj=response, key="Payload")
    body = aws.access_json(obj=payload, key="body")

    return body["value"]


def update():
    try:
        a = fetch_seed()
        random_.seed(a)
        _container.value = random_

        logger.info(f"Random generator seed successfully updated to '{a}'.")

    except Exception as e:
        # An alternative random generator that uses os.urandom.
        _container.value = random_.SystemRandom()

        logger.warning(f"Using SystemRandom as the random generator. Failed to update seed: {e}")


def get():
    try:
        return _container.value
    except AttributeError as e:
        raise AttributeError("The random generator must be updated before it can be retrieved.") from e
