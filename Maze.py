import turtle
import time

# Define constants
OBSTACLE = '%'
PART_OF_PATH = '.'
TRIED = '-'
DEAD_END = 'x'

class Maze:
    def __init__(self, maze_data):
        self.maze_list = [list(row) for row in maze_data]
        self.start_row, self.start_col = self.find_start()
        self.rows_in_maze = len(self.maze_list)
        self.columns_in_maze = len(self.maze_list[0])
        self.x_translate = -self.columns_in_maze / 2
        self.y_translate = self.rows_in_maze / 2

        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(- (self.columns_in_maze - 1) / 2 - 0.5,
                                    - (self.rows_in_maze - 1) / 2 - 0.5,
                                    (self.columns_in_maze - 1) / 2 + 0.5,
                                    (self.rows_in_maze - 1) / 2 + 0.5)

    def find_start(self):
        for row_index, row in enumerate(self.maze_list):
            if 'S' in row:
                return row_index, row.index('S')
        return None, None

    def draw_maze(self):
        self.t.speed(0)
        for y in range(self.rows_in_maze):
            for x in range(self.columns_in_maze):
                if self.maze_list[y][x] == OBSTACLE:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'tan')

    def draw_centered_box(self, x, y, color):
        self.t.up()
        self.t.goto(x - 0.5, y - 0.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def move_turtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x + self.x_translate, -y + self.y_translate))
        self.t.goto(x + self.x_translate, -y + self.y_translate)
        time.sleep(0.1)

    def drop_bread_crumb(self, color):
        self.t.dot(10, color)

    def update_position(self, row, col, val=None):
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(col, row)
        color_map = {
            PART_OF_PATH: 'green',
            OBSTACLE: 'red',
            TRIED: 'black',
            DEAD_END: 'red'
        }
        if val in color_map:
            self.drop_bread_crumb(color_map[val])

    def is_exit(self, row, col):
        return row == 0 or row == self.rows_in_maze - 1 or col == 0 or col == self.columns_in_maze - 1

    def __getitem__(self, idx):
        return self.maze_list[idx]


def search_from(maze, start_row, start_column):
    maze.update_position(start_row, start_column)

    if maze[start_row][start_column] == OBSTACLE:
        return False
    if maze[start_row][start_column] in (TRIED, DEAD_END):
        return False
    if maze.is_exit(start_row, start_column):
        maze.update_position(start_row, start_column, PART_OF_PATH)
        return True

    maze.update_position(start_row, start_column, TRIED)

    # Try moving in all four directions
    found = (search_from(maze, start_row - 1, start_column) or  # Up
             search_from(maze, start_row + 1, start_column) or  # Down
             search_from(maze, start_row, start_column - 1) or  # Left
             search_from(maze, start_row, start_column + 1))    # Right

    if found:
        maze.update_position(start_row, start_column, PART_OF_PATH)
    else:
        maze.update_position(start_row, start_column, DEAD_END)

    return found

# Sample maze data
maze_data = [
    "%%%%%%%%%%",
    "%S       %",
    "% %%% %% %",
    "%    %   %",
    "%%%% %%% %",
    "%        %",
    "%%%%%%%%E%"
]

# Run the maze solver
my_maze = Maze(maze_data)
my_maze.draw_maze()
my_maze.update_position(my_maze.start_row, my_maze.start_col)
search_from(my_maze, my_maze.start_row, my_maze.start_col)

turtle.done()
