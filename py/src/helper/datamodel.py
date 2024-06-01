from py.src.helper.point import Point


class DataModel():

    def __init__(self, x_pos, y_pos, tail=20):
        self.position_points, self.noise_points, self.kalman_points = self.prefill(
            tail, x_pos, y_pos)

    def add_new_pos_point(self, point=Point()):
        self.position_points.pop(0)
        self.position_points.insert(len(self.position_points), point)

    def add_new_noise_point(self, point=Point()):
        self.noise_points.pop(0)
        self.noise_points.insert(len(self.noise_points), point)

    def add_new_kalman_point(self, point=Point()):
        self.kalman_points.pop(0)
        self.kalman_points.insert(len(self.kalman_points), point)

    def prefill(self, tail, x, y):
        positon_points = []
        noise_points = []
        kalman_points = []

        for i in range(tail):
            positon_points.append(Point(x, y))
            noise_points.append(Point(x, y))
            kalman_points.append(Point(x, y))

        return positon_points, noise_points, kalman_points


data = DataModel(40, 40)
print(data.position_points)
