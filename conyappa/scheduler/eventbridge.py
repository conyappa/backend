from django.conf import settings

import boto3
from utils.metaclasses import Singleton


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = boto3.client(
            service_name="events",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

    def fetch(self, rule):
        data = self.client.list_rules(NamePrefix=rule.unique_name, Limit=1)
        rule_data = data["Rules"][0]

        rule.schedule_expression = rule_data["ScheduleExpression"]

    def put(self, rule):
        target_arn = settings.AWS_ARN(service_name="lambda", resource_type="function", resource_id=rule.function)

        self.client.put_rule(Name=rule.unique_name, ScheduleExpression=rule.schedule_expression)
        self.client.put_targets(Rule=rule.unique_name, Targets=[{"Id": rule.unique_name, "Arn": target_arn}])

    def delete(self, rule):
        self.client.remove_targets(Rule=rule.unique_name, Ids=[rule.unique_name])
        self.client.delete_rule(Name=rule.unique_name)
