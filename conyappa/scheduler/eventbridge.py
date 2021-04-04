from utils import aws
from utils.metaclasses import Singleton


class Interface(metaclass=Singleton):
    def __init__(self):
        self.client = aws.get_client(service_name="events")

    def fetch(self, rule):
        data = self.client.list_rules(NamePrefix=rule.eventbridge_name, Limit=1)
        rule_data = data["Rules"][0]

        rule.schedule_expression = rule_data["ScheduleExpression"]

    def put(self, rule):
        target_arn = aws.get_arn(service_name="lambda", resource_name=f"function:{rule.function}")

        self.client.put_rule(Name=rule.eventbridge_name, ScheduleExpression=rule.schedule_expression)
        self.client.put_targets(Rule=rule.eventbridge_name, Targets=[{"Id": rule.eventbridge_name, "Arn": target_arn}])

    def delete(self, rule):
        self.client.remove_targets(Rule=rule.eventbridge_name, Ids=[rule.eventbridge_name])
        self.client.delete_rule(Name=rule.eventbridge_name)
