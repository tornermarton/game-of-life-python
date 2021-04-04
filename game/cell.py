from __future__ import annotations
from enum import Enum, auto
import typing as T

from game.direction import Direction2D
from game.document import Document
from game.steppable import Steppable


class Cell(Steppable, Document):
    class State(Enum):
        ALIVE = auto()
        DEAD = auto()

    def __init__(self, state: State = State.DEAD):
        super().__init__()

        self.neighbors: T.Dict[Direction2D, Cell] = {}
        self.state: Cell.State = state
        self._next_state = Cell.State.DEAD

    def set_neighbor(self, direction: Direction2D, cell: Cell) -> None:
        self.neighbors[direction] = cell

    def set_state(self, state: Cell.State) -> None:
        if self.state != state:
            self.state = state
            self.notify()

    def calculate_next_state(self) -> None:
        alive_neighbors = 0
        for neighbor in self.neighbors.values():
            if neighbor.state == Cell.State.ALIVE:
                alive_neighbors += 1

        if self.state == Cell.State.ALIVE:
            if not 2 <= alive_neighbors <= 3:
                self._next_state = Cell.State.DEAD
            else:
                self._next_state = Cell.State.ALIVE
        else:
            if alive_neighbors == 3:
                self._next_state = Cell.State.ALIVE
            else:
                self._next_state = Cell.State.DEAD

    def step(self) -> None:
        self.set_state(self._next_state)
