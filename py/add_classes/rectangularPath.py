
class RectangularPath():
    
    def __init__(self, x_dim, y_dim, step_size, padding):
       self.padding = padding
       self.width = x_dim
       self.dot_x = x_dim
       self.height = y_dim
       self.dot_y = y_dim
       self.step_size = step_size
    
    def update_position(self):
        if (self.dot_x < (self.width - self.padding) and self.dot_y == self.padding):
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