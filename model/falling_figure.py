from model.color import Color
from model.direction import Direction
from model.figure import Figure
from model.position import Position
import random
import copy

__FIGURES_POSITIONS = {
    Figure.F_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-3, 1), (-2, -1)],
    Figure.I_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0)],
    Figure.L_FIGURE: [(-1, 0), (-1, 1), (-2, 0), (-3, 0), (-4, 0)],
    Figure.N_FIGURE: [(-1, 0), (-2, 0), (-2, 1), (-3, 1), (-4, 1)],
    Figure.P_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-2, 1), (-3, 1)],
    Figure.T_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-3, -1), (-3, 1)],
    Figure.U_FIGURE: [(-1, 0), (-1, -1), (-1, 1), (-2, -1), (-2, 1)],
    Figure.V_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-1, 1), (-1, 2)],
    Figure.W_FIGURE: [(-1, 0), (-2, 0), (-1, 1), (-2, -1), (-3, -1)],
    Figure.X_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-2, -1), (-2, 1)],
    Figure.Y_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-3, -1)],
    Figure.Z_FIGURE: [(-1, 0), (-2, 0), (-3, 0), (-3, -1), (-1, 1)],
}

__FIGURES_COLORS = {
    Figure.F_FIGURE: Color.RED,
    Figure.I_FIGURE: Color.ORANGE,
    Figure.L_FIGURE: Color.YELLOW,
    Figure.N_FIGURE: Color.GREEN,
    Figure.P_FIGURE: Color.CYAN,
    Figure.T_FIGURE: Color.BLUE,
    Figure.U_FIGURE: Color.PURPLE,
    Figure.V_FIGURE: Color.RED,
    Figure.W_FIGURE: Color.ORANGE,
    Figure.X_FIGURE: Color.YELLOW,
    Figure.Y_FIGURE: Color.GREEN,
    Figure.Z_FIGURE: Color.CYAN
}

__PREVIOUS_FIGURE = None


class FallingFigure:
    def __init__(self, field):
        self.field = field
        self.positions_list, self.color = _random_figure_generate(
            self.field.width)
        self.display_figure_on_field()

    def try_move(self, direction):
        if self.check_move(direction):
            self.remove_figure_from_field()

            for positions in self.positions_list:
                if direction == Direction.LEFT:
                    positions.column -= 1
                elif direction == Direction.RIGHT:
                    positions.column += 1
                elif direction == Direction.UP:
                    positions.row -= 1
                else:
                    positions.row += 1

            self.display_figure_on_field()

    def check_move(self, direction):
        for position in self.positions_list:
            new_row = position.row
            new_column = position.column

            if direction == Direction.LEFT:
                new_column -= 1
            elif direction == Direction.RIGHT:
                new_column += 1
            elif direction == Direction.UP:
                new_row -= 1
            else:
                new_row += 1

            if not self._is_valid_position(new_row, new_column):
                return False

        return True

    def try_rotate_left(self):
        data_for_rotate = self._check_rotate_left()
        if data_for_rotate is not None:
            self.remove_figure_from_field()
            self.positions_list = data_for_rotate
            self.display_figure_on_field()

    def _check_rotate_left(self):
        min_row = self.field.height
        min_column = self.field.width
        for position in self.positions_list:
            if position.row < min_row:
                min_row = position.row
            if position.column < min_column:
                min_column = position.column

        new_min_row = self.field.height
        new_min_column = self.field.width
        new_positions = []
        for position in self.positions_list:
            new_row = min_row - (position.column - min_column)
            new_column = position.row - min_row + min_column

            new_positions.append(Position(new_row, new_column))

            if new_row < new_min_row:
                new_min_row = new_row
            if new_column < new_min_column:
                new_min_column = new_column

        if new_min_row < min_row:
            for new_position in new_positions:
                new_position.row += min_row - new_min_row
        if new_min_column < min_column:
            for new_position in new_positions:
                new_position.column += min_column - new_min_column

        for new_position in new_positions:
            if not self._is_valid_position(
                    new_position.row, new_position.column):
                return

        return new_positions

    def _is_valid_position(self, row, column):
        if (row >= self.field.height or
                not 0 <= column < self.field.width):
            return False

        position_in_figure_flag = False
        for _position in self.positions_list:
            if row == _position.row and column == _position.column:
                position_in_figure_flag = True
                break

        if (not position_in_figure_flag and
            row >= 0 and column >= 0 and
                self.field.matrix[row][column]):
            return False

        return True

    def remove_figure_from_field(self):
        for position in self.positions_list:
            if position.row >= 0 and position.column >= 0:
                self.field.matrix[position.row][position.column] = None

    def display_figure_on_field(self):
        for position in self.positions_list:
            if position.row >= 0 and position.column >= 0:
                self.field.matrix[position.row][position.column] = self.color

    def drop_figure(self):
        while self.check_move(Direction.DOWN):
            self.try_move(Direction.DOWN)


def _random_figure_generate(field_width):
    figures_list = list(__FIGURES_POSITIONS.keys())

    global __PREVIOUS_FIGURE
    if __PREVIOUS_FIGURE:
        figures_list.remove(__PREVIOUS_FIGURE)

    random_figure = random.choice(figures_list)

    __PREVIOUS_FIGURE = random_figure

    figure_positions = copy.deepcopy(__FIGURES_POSITIONS[random_figure])
    figure_color = __FIGURES_COLORS[random_figure]

    shift_positions = []
    shift = field_width // 2 - 1
    for position in figure_positions:
        shift_positions.append(Position(position[0], position[1] + shift))

    return shift_positions, figure_color
