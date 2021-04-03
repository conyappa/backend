import random as random_

from django.conf import settings

from utils import aws


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

    except Exception:
        # An alternative random generator that uses os.urandom.
        _container.value = random_.SystemRandom()


def get():
    return _container.value
