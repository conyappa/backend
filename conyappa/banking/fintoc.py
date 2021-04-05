from django.conf import settings
from django.db import transaction

from fintoc import Client

from utils.metaclasses import Singleton

from .models import Movement


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = Client(api_key=settings.FINTOC_SECRET_KEY)
        self.link = self.client.get_link(link_token=settings.FINTOC_LINK_TOKEN)
        self.account = self.link.find(id_=settings.FINTOC_ACCOUNT_ID)

    @transaction.atomic
    def fetch_movements(self):
        query_params = {"page": 1}

        # Movements are ordered by Fintoc’s post_date. More recent goes first.
        latest_movement = Movement.objects.first()

        if latest_movement is not None:
            query_params["since"] = latest_movement.fintoc_post_date

        while True:
            fintoc_movements = list(self.account.get_movements(**query_params))

            if not fintoc_movements:
                break

            for obj in fintoc_movements:
                data = obj.serialize()
                fintoc_id = data.get("id")

                # Ignore duplicated movements (i.e., with the same fintoc_id).
                movments_w_same_fintoc_id = Movement.objects.filter(fintoc_id=fintoc_id)
                if movments_w_same_fintoc_id.exists():
                    continue

                fintoc_post_datetime = data.get("post_date")
                fintoc_post_date = fintoc_post_datetime.split("T")[0]

                # Use the regular create method instead of bulk_create so the post_save signal is sent.
                # Don’t worry, though. These creations all ocurr in an atomic transaction.
                Movement.objects.create(fintoc_data=data, fintoc_id=fintoc_id, fintoc_post_date=fintoc_post_date)

            query_params["page"] += 1
