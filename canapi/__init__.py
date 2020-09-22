
import json
import os

import canapi.auth as auth

from canapi.client import ClientAPI


PATHS = {
    "default": __path__[0] + "/registry"
}


def add_registry(name: str, path: str):
    """Adds `path` as a valid registry to search for apis.

    Parameters
    ----------
    name : str
        Name of the registry.
    path : str
        A registry path.
    """
    PATHS[name] = path


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
    client = None

    if name in ClientAPI.apis:
        client = ClientAPI.apis[name]
        if kwargs:
            client.auth(**kwargs)
        return client

    found = False
    for k in PATHS.keys():
        path = PATHS[k] + f"/{name}.json"

        if os.path.exists(path):
            client = from_json(path)
            if kwargs:
                client.auth(**kwargs)
            return client

    return client
