
class RectangularPath():
    
    def __init__(self, x_dim, y_dim, step_size, padding):
       self.padding = padding
       self.width = x_dim
       self.x_dot = x_dim
       self.height = y_dim
       self.y_dot = y_dim
       self.step_size = step_size
    
    def update_position(self):
        if (self.dot_x < (self.width - self.route_padding) and self.dot_y == self.route_padding):
            # TR
            self.dot_x = self.dot_x + self.step_size
        elif (self.dot_x == (self.width - self.route_padding) and self.dot_y <= (self.height - self.route_padding)):
            # TL
            self.dot_y = self.dot_y + self.step_size
        elif (self.dot_x > self.route_padding and self.dot_y >= (self.canvas_height - self.route_padding)):
            # BR
            self.dot_x = self.dot_x - self.step_size
        else:
            # BL
            self.dot_y = self.dot_y - self.step_size

        return self.dot_x, self.dot_y