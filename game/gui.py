import typing as T

import PySimpleGUI as sg

from game import Game, Coordinates2D
from game.cell import Cell
from game.view import View, Clickable


CELL_SIZE = 10


class CellView(View, Clickable):
    def __init__(self, graph: sg.Graph, coordinates: Coordinates2D, cell: Cell):
        self._graph: sg.Graph = graph
        self._coordinates: Coordinates2D = coordinates
        self._id: T.Optional[int] = None

        self._cell: Cell = cell
        self._cell.attach(self)

        self.draw()

    def click(self) -> None:
        if self._cell.state == Cell.State.ALIVE:
            self._cell.set_state(Cell.State.DEAD)
        else:
            self._cell.set_state(Cell.State.ALIVE)

    def update(self) -> None:
        self.draw()

    def draw(self) -> None:
        if self._id:
            self._graph.delete_figure(self._id)

        top_left: Coordinates2D = self._coordinates
        bottom_right: Coordinates2D = Coordinates2D(top_left.x + CELL_SIZE, top_left.y + CELL_SIZE)
        fill: str = "white" if self._cell.state == Cell.State.ALIVE else "black"

        self._id = self._graph.DrawRectangle(
            top_left.as_tuple(),
            bottom_right.as_tuple(),
            line_color="white",
            fill_color=fill
        )


class App(View):
    @staticmethod
    def create_window(width: int, height: int) -> sg.Window:
        layout: list = [
            [
                sg.Graph(
                    canvas_size=(width, height),
                    graph_bottom_left=(0, height),
                    graph_top_right=(width, 0),
                    change_submits=True,
                    background_color='black',
                    key='-GRAPH-'
                )
            ],
            [
                sg.Button("Play", key="-PLAY-"),
                sg.Button("Pause", key="-PAUSE-"),
                sg.Button("Step", key="-STEP-"),
                sg.Button("Reset", key="-RESET-"),
                sg.Text("Generation: 0", key="-OUTPUT-"),
            ],
        ]

        # Create the window
        window: sg.Window = sg.Window("Demo", layout)
        window.Finalize()

        return window

    def __init__(self, n_cells: Coordinates2D):
        self.window: sg.Window = self.create_window(CELL_SIZE * n_cells.x + 1, CELL_SIZE * n_cells.y + 1)

        self.game: Game = Game(n_cells, step_frequency=0.05)
        self.game.attach(self)

        self.cell_views: T.List[T.List[CellView]] = [
            [
                CellView(
                    graph=self.window["-GRAPH-"],
                    coordinates=Coordinates2D(x, y) * Coordinates2D(CELL_SIZE, CELL_SIZE),
                    cell=cell,
                ) for x, cell in enumerate(row)
            ] for y, row in enumerate(self.game.cells)
        ]

    def run(self) -> None:
        # Create an event loop
        while True:
            event, values = self.window.read()
            # End program if user closes window or
            # presses the OK button
            if event == sg.WIN_CLOSED:
                break

            if event == "-PLAY-":
                self.game.start()
            if event == "-PAUSE-":
                self.game.pause()
            if event == "-STEP-":
                self.game.step()
            if event == "-RESET-":
                self.game.reset()

            mouse = values['-GRAPH-']
            if event == '-GRAPH-':

                if mouse == (None, None):
                    continue

                coordinates = Coordinates2D(mouse[0], mouse[1]) // Coordinates2D(CELL_SIZE, CELL_SIZE)
                self.cell_views[coordinates.y][coordinates.x].click()

        self.game.stop()
        self.window.close()

    def update(self) -> None:
        self.draw()

    def draw(self) -> None:
        self.window['-OUTPUT-'].update(f'Generation {self.game.generation}')
