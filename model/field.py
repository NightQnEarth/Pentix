class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[None for _ in range(self.width)] for _ in range(
            self.height)]
        self.scores = 0

    def remove_completed_line(self, falling_figure):
        completed_lines = 0
        while self._search_completed_line():
            completed_lines += 1
            completed_line = self._search_completed_line()

            for column in range(self.width):
                self.matrix[completed_line][column] = None

            self._move_down_after_remove_line(completed_line, falling_figure)

        for i in range(completed_lines):
            self.scores += 100 * 2**(i - 1)

    def _move_down_after_remove_line(self, number_of_removed_line,
                                     falling_figure):
        falling_figure.remove_figure_from_field()
        for row in range(number_of_removed_line, 0, -1):
            for column in range(self.width):
                self.matrix[row][column] = self.matrix[row - 1][column]
                self.matrix[row - 1][column] = None

    def _search_completed_line(self):
        for row_number in range(self.height - 1, -1, -1):
            flag = True
            for element in self.matrix[row_number]:
                if not element:
                    flag = False
                    break
            if flag:
                return row_number
        return

    def clear_field(self):
        for row in range(self.height):
            for column in range(self.width):
                self.matrix[row][column] = None

        self.scores = 0
