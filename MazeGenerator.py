from tkinter import Canvas, Frame, BOTH
import random

canvas = ""
maze_size = 1000
to_move = 25
of_map = 100

# can be green, yellow, blue or any color you want. you can even hex colors. "" for no color
background_color = "black"
line_color = "white"

lines = []
directions = ['up', 'down', 'right', 'left']


class MazeGenerator(Frame):

    def __init__(self):
        super().__init__()
        self.init_maze()

    '''
    to initiate and start the maze
    '''
    def init_maze(self):
        global maze_size, canvas, background_color

        self.master.title("Maze generator")
        self.master.attributes("-topmost", True)
        self.master.resizable(False, False)
        self.pack(fill=BOTH, expand=1)

        self.master.geometry(str(maze_size) + 'x' + str(maze_size))  # for the size of the window

        # convas to hold the 3d renders
        if canvas == "":
            canvas = Canvas(self)
        canvas.pack(fill=BOTH, expand=1)

        canvas.create_polygon([0, 0, 0, maze_size, 0, maze_size, maze_size, maze_size, maze_size, maze_size, maze_size, 0, maze_size, 0, 0, 0], fill=background_color)
        self.generate()

    '''
    to start the maze generation
    '''
    def generate(self):
        global directions, lines, maze_size, to_move, line_color, of_map
        start = maze_size / of_map
        x2, y2 = start, start
        lines = [[x2, y2]]

        while True:
            did_not_draw = False
            stuck_times = 0
            while not did_not_draw:
                path = directions[random.randint(0, len(directions) - 1)]
                if path == "left" and not self.check_path_taken([x2, y2 + to_move]):
                    x, y = x2, y2
                    y2 = y2 + to_move
                    self.create_line([x, y, x2, y2])
                    did_not_draw = True
                if path == "right" and not self.check_path_taken([x2, y2 - to_move]):
                    x, y = x2, y2
                    y2 = y2 - to_move
                    self.create_line([x, y, x2, y2])
                    did_not_draw = True
                if path == "up" and not self.check_path_taken([x2 + to_move, y2]):
                    x, y = x2, y2
                    x2 = x2 + to_move
                    self.create_line([x, y, x2, y2])
                    did_not_draw = True
                if path == "down" and not self.check_path_taken([x2 - to_move, y2]):
                    x, y = x2, y2
                    x2 = x2 - to_move
                    self.create_line([x, y, x2, y2])
                    did_not_draw = True
                stuck_times = stuck_times + 1
                if stuck_times == 10:
                    x2, y2 = self.get_random_location()
                    break
            self.master.update()

    '''
    @param points: array of points in the form of [x, y]
    used to check if a path is already taken to prevent squares/circles
    '''
    def check_path_taken(self, points):
        global maze_size, lines, line_color
        if points[0] < 0 or points[1] < 0:
            return True
        if points[0] > maze_size or points[1] > maze_size:
            return True
        for line in lines:
            if line == [points[0], points[1]]:
                return True
        return False

    '''
    to start at a different location when the other path dies
    '''
    def get_random_location(self):
        global lines, maze_size, to_move, of_map, line_color
        start = maze_size / of_map
        x = start + (to_move * random.randint(0, maze_size / to_move))
        y = start + (to_move * random.randint(0, maze_size / to_move))
        if x >= maze_size:
            x = maze_size - start
        if y >= maze_size:
            y = maze_size - start
        points = [x, y]
        fine_path = self.check_path_taken(points)
        while not fine_path:
            x = start + (to_move * random.randint(0, maze_size / to_move))
            y = start + (to_move * random.randint(0, maze_size / to_move))
            if x >= maze_size:
                x = maze_size - start
            if y >= maze_size:
                y = maze_size - start
            points = [x, y]
            fine_path = self.check_path_taken(points)
        return x, y

    '''
    @param points: array of points in the form of [x, y, x2, y2]
    used to draw a line from x,y to x2, y2 location
    '''
    def create_line(self, points):
        global canvas, line_color, lines, maze_size
        if canvas == "":
            canvas = Canvas(self)
        lines.append([points[2], points[3]])
        canvas.create_polygon(points, fill="", outline=line_color, width=maze_size / of_map)


