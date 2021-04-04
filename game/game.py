import time
import typing as T
from threading import Thread
from enum import Enum, auto

from game.cell import Cell
from game.coordinates import Coordinates2D
from game.direction import Direction2D
from game.document import Document
from game.steppable import Steppable


class Game(Steppable, Document):
    class State(Enum):
        RUNNING = auto()
        PAUSED = auto()
        STOPPED = auto()

    @staticmethod
    def create_cell_grid(grid_size: Coordinates2D) -> T.List[T.List[Cell]]:
        cells: T.List[T.List[Cell]] = [[Cell() for _ in range(grid_size.x)] for _ in range(grid_size.y)]

        for y in range(grid_size.y):
            for x in range(grid_size.x):
                cells[y][x].set_neighbor(
                    Direction2D.NORTH, cells[y - 1][x]
                )
                cells[y][x].set_neighbor(
                    Direction2D.NORTH_WEST, cells[y - 1][x - 1]
                )
                cells[y][x].set_neighbor(
                    Direction2D.WEST, cells[y][x - 1]
                )
                cells[y][x].set_neighbor(
                    Direction2D.SOUTH_WEST, cells[y + 1 if y < grid_size.y - 1 else 0][x - 1]
                )
                cells[y][x].set_neighbor(
                    Direction2D.SOUTH, cells[y + 1 if y < grid_size.y - 1 else 0][x]
                )
                cells[y][x].set_neighbor(
                    Direction2D.SOUTH_EAST, cells[y + 1 if y < grid_size.y - 1 else 0][x + 1 if x < grid_size.x - 1 else 0]
                )
                cells[y][x].set_neighbor(
                    Direction2D.EAST, cells[y][x + 1 if x < grid_size.x - 1 else 0]
                )
                cells[y][x].set_neighbor(
                    Direction2D.NORTH_EAST, cells[y - 1][x + 1 if x < grid_size.x - 1 else 0]
                )

        return cells

    def __init__(self, grid_size: Coordinates2D, max_generations: int = None, step_frequency: float = None):
        super().__init__()

        self._grid_size: Coordinates2D = grid_size
        self._cells: T.List[T.List[Cell]] = Game.create_cell_grid(grid_size)

        self._generation: int = 0
        self._max_generations: int = max_generations

        self._state: Game.State = Game.State.STOPPED
        self._step_frequency: float = step_frequency

    @property
    def cells(self):
        return self._cells

    @property
    def generation(self) -> int:
        return self._generation

    def main_loop(self):
        while True:
            if self._max_generations_reached() or self._state == Game.State.STOPPED:
                break

            if self._state == Game.State.RUNNING:
                self.step()

            if self._step_frequency:
                time.sleep(self._step_frequency)

        self._state = Game.State.STOPPED

    def step(self) -> None:
        if self._max_generations_reached():
            return

        for row in self._cells:
            for cell in row:
                cell.calculate_next_state()

        for row in self._cells:
            for cell in row:
                cell.step()

        self._generation += 1
        self.notify()

    def start(self) -> None:
        if self._state == Game.State.STOPPED:
            self._state = Game.State.RUNNING
            Thread(target=self.main_loop).start()
        else:
            self._state = Game.State.RUNNING

    def pause(self) -> None:
        self._state = Game.State.PAUSED

    def stop(self) -> None:
        self._state = Game.State.STOPPED

    def reset(self) -> None:
        self.stop()

        for row in self._cells:
            for c in row:
                c.set_state(Cell.State.DEAD)

        self._generation = 0
        self.notify()

    def revive_cell(self, coordinates: Coordinates2D) -> None:
        self._cells[coordinates.y][coordinates.x].set_state(Cell.State.ALIVE)

    def kill_cell(self, coordinates: Coordinates2D) -> None:
        self._cells[coordinates.y][coordinates.x].set_state(Cell.State.DEAD)

    def _max_generations_reached(self) -> bool:
        return self._max_generations and self._generation == self._max_generations
