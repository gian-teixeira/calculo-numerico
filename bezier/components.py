import numpy as np

class Point(np.ndarray):
    def __new__(cls,  input_array, type):
        obj = np.asarray(input_array).view(cls)
        obj.type = type
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None: return
        self.type = getattr(self, 'type', None)
