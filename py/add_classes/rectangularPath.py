
class RectangularPath():

    def __init__(self, x_dim, y_dim, step_size):
        self.width = x_dim
        self.dot_x = 0
        self.height = y_dim
        self.dot_y = 0
        self.step_size = step_size
        self.rectangle_width, self.rectangle_height = self.calculate_rectangle_dimensions()
        self.rectangle_origin_x, self.rectangle_origin_y = self.calculate_rectangle_origin()

    def update_position(self):
        if (self.dot_x < (self.rectangle_width + self.rectangle_origin_x) and self.dot_y == self.rectangle_origin_y):
            # TR
            self.dot_x = self.dot_x + self.step_size
        elif (self.dot_x == (self.rectangle_width + self.rectangle_origin_x) and self.dot_y <= (self.rectangle_height + self.rectangle_origin_y)):
            # TL
            self.dot_y = self.dot_y + self.step_size
        elif (self.dot_x > self.rectangle_origin_x and self.dot_y == (self.rectangle_height + self.rectangle_origin_y)):
            # BR
            self.dot_x = self.dot_x - self.step_size
        else:
            # BL
            self.dot_y = self.dot_y - self.step_size

        return self.dot_x, self.dot_y

    def calculate_rectangle_dimensions(self):
        temp_rectangle_width = self.width * 0.8
        temp_rectangle_height = self.height * 0.8
        rectangle_width = temp_rectangle_width - \
            (temp_rectangle_width % self.step_size)
        rectangle_height = temp_rectangle_height - \
            (temp_rectangle_height % self.step_size)
        return rectangle_width, rectangle_height

    def calculate_rectangle_origin(self):
        rectangle_origin_x = (self.width - self.rectangle_width) / 2
        rectangle_origin_y = (self.height - self.rectangle_height) / 2
        return rectangle_origin_x, rectangle_origin_y
