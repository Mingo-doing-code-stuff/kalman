
class RectangularPath():

    def __init__(self, x_dim, y_dim, step_size):
        self.width = x_dim
        self.x_dot = 0
        self.height = y_dim
        self.y_dot = 0
        self.step_size = step_size
        self.rectangle_width, self.rectangle_height = self.calculate_rectangle_dimensions()
        self.rectangle_origin_x, self.rectangle_origin_y = self.calculate_rectangle_origin()

    def update_position(self):
        if (self.dot_x < (self.rectangle_width) and self.dot_y == self.padding):
            # TR
            self.dot_x = self.dot_x + self.step_size
        elif (self.dot_x == (self.width - self.padding) and self.dot_y <= (self.height - self.padding)):
            # TL
            self.dot_y = self.dot_y + self.step_size
        elif (self.dot_x > self.padding and self.dot_y >= (self.height - self.padding)):
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
