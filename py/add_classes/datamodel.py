from point import Point
# from canvasHandler import CanvasHandler


class DataModel():

    # def __init__(self, model_number, tail, step_size, canvas_width, canvas_height):
    def __init__(self, canvas):
        self.canvas = canvas
        self.tail = 20
        self.x = 40  # delete after
        self.y = 40  # delete after

        # self.step_size = step_size
        # self.canvas_width = canvas_width
        # self.canvas_height = canvas_height
        # self.tail = tail
        # self.canvas = canvas
        # initial_x, initial_y = self.setup(model_number)
        # self.position_points, self.noise_points, self.kalman_points = self.prefill(
        #     self.tail, initial_x, initial_y)
        # print("DataModel running")

    def add_new_pos_point(self, point=Point()):
        self.position_points.pop(0)
        self.position_points.insert(-1, point)

    def add_new_noise_point(self, point=Point()):
        self.noise_points.pop(0)
        self.noise_points.insert(-1, point)

    def add_new_kalman_point(self, point=Point()):
        self.kalman_points.pop(0)
        self.kalman_points.insert(-1, point)

    def oval_create(self, x, y):
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='blue')

    def prefill(self):
        position_points = []
        noise_points = []
        kalman_points = []

        for i in range(self.tail):
            position_points.append(self.oval_create(self.x, self.y))
            noise_points.append(self.oval_create(self.x+40, self.y+40))
            kalman_points.append(self.oval_create(self.x+80, self.y+80))

        return position_points, noise_points, kalman_points

    def setup(self, model_number):
        if (model_number == 1):
            return 0, 0
        elif (model_number == 2):
            return self.canvas.winfo_reqwidth() / 2, self.canvas.winfo_reqheight() / 2
        else:
            return self.calculate_rectangle_origin()

    def calculate_rectangle_dimensions(self):
        temp_rectangle_width = self.canvas_width * 0.8
        temp_rectangle_height = self.canvas_height * 0.8
        rectangle_width = temp_rectangle_width - \
            (temp_rectangle_width % self.step_size)
        rectangle_height = temp_rectangle_height - \
            (temp_rectangle_height % self.step_size)
        return rectangle_width, rectangle_height

    def calculate_rectangle_origin(self):
        rectangle_width, rectangle_height = self.calculate_rectangle_dimensions()
        rectangle_origin_x = (self.canvas_width - rectangle_width) / 2
        rectangle_origin_y = (self.canvas_height - rectangle_height) / 2
        return rectangle_origin_x, rectangle_origin_y

