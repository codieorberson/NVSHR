from multiprocessing import Value

class SharedBool():
    def __init__(self):
        self.numerical_representation = Value('i', 0)

    def get(self):
        return bool(self.numerical_representation.value)

    def set(self, is_true):
        self.numerical_representation.value = int(is_true)
