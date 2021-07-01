"""A video playlist class."""
from .video import Video


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, list_name: str):
        """Video constructor."""
        self._name = list_name
        self._content=[]


    @property
    def name(self) -> str:
        """Returns the title of a video."""
        return self._name

    @property
    def content(self) -> list[Video]:
        """Returns the list of tags of a video."""
        return self._content
