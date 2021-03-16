from django.http import JsonResponse


class AttachmentJsonResponse(JsonResponse):
    def __init__(self, data, filename):
        super().__init__(data, json_dumps_params={"indent": 2})
        self.setdefault("Content-Disposition", f'attachment; filename="{filename}.json"')
