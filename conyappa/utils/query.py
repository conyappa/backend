class RelatedQuerySetMixin:
    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            self.instance = kwargs.pop("instance")

        super().__init__(*args, **kwargs)

    def _clone(self):
        c = super()._clone()
        c.instance = self.instance
        return c

    @property
    def is_related_to_instance(self):
        return hasattr(self, "instance")
