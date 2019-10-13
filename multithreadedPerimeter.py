from multiprocessing import Value

class MultithreadedPerimeter():
    def __init__(self):
        self.x1 = Value('I', 0)
        self.y1 = Value('I', 0)
        self.x2 = Value('I', 0)
        self.y2 = Value('I', 0)

    def get_top_corner(self):
        return (self.x1.value, self.y1.value)

    def get_bottom_corner(self):
        return (self.x2.value, self.y2.value)

    def get_ratio(self):
        return (self.y2.value - self.y1.value) / (self.x2.value - self.x1.value)

    def set(self, x_y_w_h_tuple):
        self.x1.value = x_y_w_h_tuple[0]
        self.y1.value = x_y_w_h_tuple[1]
        self.x2.value = x_y_w_h_tuple[0] + x_y_w_h_tuple[2]
        self.y2.value = x_y_w_h_tuple[1] + x_y_w_h_tuple[3]

    def is_set(self):
        return bool(self.x2.value > 0)
