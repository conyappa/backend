import copy as cp


class SetOnlyFieldsMixin:
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        # Don’t modify an OrderedDict during iteration.
        # Instead, iterate over a copy.
        data_copy = cp.deepcopy(data)

        # If bool(self.instance) == True,
        # then the object already exists.
        if self.instance:

            for k in data_copy:
                # Retrieve the field’s current value.
                v = getattr(self.instance, k, None)

                # Check if the field is set-only.
                is_set_only = k in self.Meta.set_only_fields

                if v and is_set_only:
                    del data[k]

        return data
