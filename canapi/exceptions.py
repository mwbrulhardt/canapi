

class ClientAPINotRegistered(Exception):

    def __init__(self, name: str, version):
        name =  name if version is None else f"{name}:{version}"
        super().__init__(f"ClientAPI `{name}` is not registered.")
