import unittest
from model import logic_model, direction, position, color


class Tests(unittest.TestCase):
    LogicModel = None

    def setUp(self):
        self.LogicModel = logic_model.LogicModel()

    def test_update(self):
        self.LogicModel.update()

        figure_flag = False
        for row in self.LogicModel.field.matrix:
            for item in row:
                if isinstance(item, color.Color):
                    figure_flag = True

        self.assertTrue(figure_flag)

    def test_move(self):
        self.LogicModel.falling_figure.try_move(direction.Direction.DOWN)

        current_position = None
        for row in range(self.LogicModel.field.height):
            for column in range(self.LogicModel.field.width):
                if self.LogicModel.field.matrix[row][column] is not None:
                    current_position = position.Position(row, column)

        self.LogicModel.falling_figure.try_move(direction.Direction.LEFT)

        self.assertTrue(
            isinstance(self.LogicModel.field.matrix[current_position.row]
                       [current_position.column - 1], color.Color))

        self.LogicModel.falling_figure.try_move(direction.Direction.RIGHT)

        self.assertTrue(
            isinstance(self.LogicModel.field.matrix[current_position.row]
                       [current_position.column], color.Color))

    def test_rotate(self):
        for i in range(5):
            self.LogicModel.update()

        self.LogicModel.falling_figure.try_rotate_left()

    def test_clear_field(self):
        for _ in range(10):
            self.LogicModel.update()
        self.LogicModel.field.clear_field()

        for row in self.LogicModel.field.matrix:
            for item in row:
                self.assertIsNone(item)

    def test_end_of_the_game(self):
        for i in range(100):
            self.LogicModel.update()

        self.assertTrue(self.LogicModel.end_of_the_game())

    def test_remove_line(self):
        self.LogicModel.field.matrix[0][0] = color.Color.BLUE

        for column in range(self.LogicModel.field.width):
            self.LogicModel.field.matrix[1][column] = color.Color.CYAN
            self.LogicModel.field.matrix[2][column] = color.Color.GREEN

        self.LogicModel.field.remove_completed_line(
            self.LogicModel.falling_figure)

        self.assertTrue(self.LogicModel.field.matrix[2][0] is color.Color.BLUE)

    def test_drop_figure(self):
        self.LogicModel.falling_figure.drop_figure()
        self.assertFalse(self.LogicModel.falling_figure.check_move(
            direction.Direction.DOWN))


if __name__ == '__main__':
    unittest.main()
