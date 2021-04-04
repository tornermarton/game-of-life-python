from __future__ import annotations
from dataclasses import dataclass


@dataclass()
class Coordinates2D(object):
    x: int
    y: int

    def __add__(self, other: Coordinates2D) -> Coordinates2D:
        x = self.x + other.x
        y = self.y + other.y
        return Coordinates2D(x, y)

    def __mul__(self, other: Coordinates2D) -> Coordinates2D:
        """Element wise multiplication"""
        x = self.x * other.x
        y = self.y * other.y
        return Coordinates2D(x, y)

    def __floordiv__(self, other: Coordinates2D) -> Coordinates2D:
        """Element wise multiplication"""
        x = self.x // other.x
        y = self.y // other.y
        return Coordinates2D(x, y)

    def as_tuple(self) -> tuple:
        return self.x, self.y
