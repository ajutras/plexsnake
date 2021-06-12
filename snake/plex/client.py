from opset import config
from plexapi.server import PlexServer

plex_client = None


def get_plex_client() -> PlexServer:
    global plex_client

    if plex_client:
        return plex_client

    plex_client = PlexServer(config.plex.api_endpoint, config.plex.token)

    return plex_client
