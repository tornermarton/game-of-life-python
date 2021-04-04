import typing as T

from game.view import View


class Document(object):
    def __init__(self):
        self._views: T.List[View] = []

    def attach(self, view: View) -> None:
        self._views.append(view)

    def detach(self, view: View) -> None:
        self._views.remove(view)

    def notify(self) -> None:
        for s in self._views:
            s.update()
