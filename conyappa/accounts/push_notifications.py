from logging import getLogger

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError,
)

from utils.metaclasses import Singleton

logger = getLogger(__name__)


class Interface(metaclass=Singleton):
    EXCEPTION_MESSAGE_TEMPLATE = "Unable to send push notification to {device}: {e}"

    def __init__(self):
        self.client = PushClient()

    def _publish_message(self, token, body, data):
        message = PushMessage(to=token, body=body, data=data)
        return self.client.publish(message)

    def send(self, device, body, data=None):
        try:
            response = self._publish_message(self, token=device.expo_push_token, body=body, data=data)
        except Exception as e:
            logger.error(self.EXCEPTION_MESSAGE_TEMPLATE.format(device=device, e=e))

        try:
            response.validate_response()
        except DeviceNotRegisteredError as e:
            logger.warning(self.EXCEPTION_MESSAGE_TEMPLATE.format(device=device, e=e))
        except PushTicketError as e:
            logger.error(self.EXCEPTION_MESSAGE_TEMPLATE.format(device=device, e=e))
