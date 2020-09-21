
import json


import canopy.auth as auth

from canopy.client import ClientAPI


def from_json(path: str) -> ClientAPI:
    """Generates a `ClientAPI` from a json configuration file.

    Parameters
    ----------
    path : str
        The path of the configuration file.

    Returns
    -------
    `ClientAPI`
        A client api generated from the configuration file.
    """
    config = json.load(open(path))
    api = ClientAPI(
        name=config['name'],
        uri=config['uri'],
        endpoints=config['endpoints'],
        **config.get('session', {})
    )
    return api


def api(name: str, **kwargs) -> ClientAPI:

    if name in ClientAPI.apis:
        client = ClientAPI.apis[name]
        if kwargs:
            client.auth(**kwargs)
        return client

    path = __path__[0] + f"/registry/{name}.json"
    client = from_json(path)

    if kwargs:
        client.auth(**kwargs)

    return client
