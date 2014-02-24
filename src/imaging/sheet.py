from PIL import Image
import numpy as np

class Sheet:
    def __init__(self, source_image_path):
        self.image = Image.open(source_image_path)
        self.image_array = np.asarray(self.image)
        self.find_dimensions()

    def find_dimensions(self):
        # determine height, width, and midpoint of width
        self.height = self.image_array.shape[0]
        self.width = self.image_array.shape[1]
        self.midpoint = self.width/2
