from PyQt5.QtWidgets import (
    QDesktopWidget, QMessageBox, QGridLayout, QWidget, QMainWindow, QLabel)
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from os import path
from model.color import Color
from model.direction import Direction
from model import falling_figure


class GameWindow(QMainWindow):
    __COLORS_MATCHING = {
        Color.RED: 'red',
        Color.ORANGE: 'orange',
        Color.YELLOW: 'yellow',
        Color.GREEN: 'green',
        Color.CYAN: 'cyan',
        Color.BLUE: 'blue',
        Color.PURPLE: 'purple',
        None: 'white'
    }

    __TICK_TIME = 500
    __MINIMUM_CELL_SIZE = 15
    __MAXIMUM_CELL_SIZE = 30

    def __init__(self, logic_model):
        super().__init__()

        self.logic_model = logic_model
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._timer_tick)
        self._grid, self._cells_matrix = self._grid_create()
        self.timer.start(self.__TICK_TIME)
        self.__window_tune()

    def __window_tune(self):
        self.setMaximumSize(self.__MAXIMUM_CELL_SIZE *
                            self.logic_model.field.width,
                            self.__MAXIMUM_CELL_SIZE *
                            self.logic_model.field.height)
        self.setWindowTitle('Pentix')
        self.setWindowIcon(QIcon(path.join('icons', 'bird.png')))
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Scores: {}'.format(
            int(self.logic_model.field.scores)))
        self._move_center()
        self.show()

    def _grid_create(self):
        grid = QGridLayout()
        grid.setSpacing(2)

        cells_matrix = [[None for _ in range(self.logic_model.field.width)]
                        for _ in range(self.logic_model.field.height)]

        for i in range(self.logic_model.field.height):
            for j in range(self.logic_model.field.width):
                cell = QLabel()
                cell.setMinimumSize(self.__MINIMUM_CELL_SIZE,
                                    self.__MINIMUM_CELL_SIZE)
                cell.setMaximumSize(self.__MAXIMUM_CELL_SIZE,
                                    self.__MAXIMUM_CELL_SIZE)
                cell.setStyleSheet('background-color: {};'.format(
                    self.__COLORS_MATCHING[self.logic_model.field.matrix[i][j]]))
                grid.addWidget(cell, i, j)
                cells_matrix[i][j] = cell

        game_field_widget = QWidget()
        game_field_widget.setLayout(grid)
        self.setCentralWidget(game_field_widget)

        return grid, cells_matrix

    def _grid_update(self):
        for i in range(self.logic_model.field.height):
            for j in range(self.logic_model.field.width):
                color = self.__COLORS_MATCHING[
                    self.logic_model.field.matrix[i][j]]
                self._cells_matrix[i][j].setStyleSheet(
                    'background-color: {};'.format(color))

    def _timer_tick(self):
        if not self.logic_model.end_of_the_game():
            self.logic_model.update()
            self._grid_update()
            self.status_bar.showMessage('Scores: {}'.format(
                int(self.logic_model.field.scores)))
        else:
            self.timer.stop()
            self.status_bar.showMessage('End of the game')

    def _move_center(self):
        self.move(self.width() * -2, 0)
        self.show()
        exact_window_form = self.frameGeometry()
        exact_desktop_center = QDesktopWidget().availableGeometry().center()
        exact_window_form.moveCenter(exact_desktop_center)
        self.move(exact_window_form.topLeft())

    def closeEvent(self, event):
        self.timer.stop()
        self.status_bar.showMessage('Pause')
        caption = 'Confirm Exit'
        question = 'Are you sure you want to exit Pentix?'
        message_box = QMessageBox()
        reply = message_box.question(
            self,
            caption,
            question,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply == message_box.Yes:
            QCoreApplication.exit()
        else:
            event.ignore()

        self.status_bar.showMessage('Scores: {}'.format(
            int(self.logic_model.field.scores)))
        self.timer.start()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            self.closeEvent(QCloseEvent())

        elif key == Qt.Key_R:
            self.logic_model.field.clear_field()
            self.logic_model.falling_figure = falling_figure.FallingFigure(
                self.logic_model.field)
            self.timer.start()

        elif key == Qt.Key_P:
            if self.timer.isActive():
                self.status_bar.showMessage('Pause')
                self.timer.stop()
            else:
                self.timer.start()

        elif self.timer.isActive():
            if key == Qt.Key_Left:
                self.logic_model.falling_figure.try_move(Direction.LEFT)

            elif key == Qt.Key_Right:
                self.logic_model.falling_figure.try_move(Direction.RIGHT)

            elif key == Qt.Key_Down:
                self.logic_model.falling_figure.try_move(Direction.DOWN)

            elif key == Qt.Key_Up:
                self.logic_model.falling_figure.try_rotate_left()

            elif key == Qt.Key_Space:
                self.logic_model.falling_figure.drop_figure()
                self.logic_model.falling_figure = \
                    falling_figure.FallingFigure(self.logic_model.field)
                self.logic_model.field.remove_completed_line(
                    self.logic_model.falling_figure)

        self._grid_update()
