import uuid


class FilterModule:
    def filters(self):
        return {"uuidv5": self._uuidv5}

    @staticmethod
    def _uuidv5(name, namespace):
        return str(uuid.uuid5(uuid.UUID(namespace), name))
