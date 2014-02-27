from PIL import Image
import math
import numpy as np

class SheetImage:
    def __init__(self, source_image_path):
        # initializes image metadata from analyzing image
        self.image = Image.open(source_image_path)

    def get_image_array(self):
        # returns the image array of the sheet music image
        return np.asarray(self.image)

    def get_width(self):
        # returns the width of the sheet music image
        return self.get_dimensions()[0]
    
    def get_height(self):
        # returns height of sheet music image
        return self.get_dimensions()[1]

    def get_midpoint(self):
        # returns x-midpoint of sheet music image
        return math.ceil(self.get_width()/2)

    def get_dimensions(self):
        # returns tuple of (width, height) of the test sheet music
        image_array_shape = self.get_image_array().shape
        return(image_array_shape[1], image_array_shape[0])

    def get_staffs(self):
        # returns list of tuples 
        pass

    def get_staff(self, vertical_offset):
        # returns the first y value of a staff from vertical_offset down
        midpoint = self.get_midpoint()
        image_array = self.get_image_array()
        image_height = self.get_height()

        for y_root in range(image_height-25):
            current_pixel_value = image_array[y_root][midpoint]
            current_pixel_is_black = self.__pixel_is_black(current_pixel_value)

            if not current_pixel_is_black:
                continue # haven't found the first ledger line yet
            
            # now we've possibly found the first ledger line

            next_pixel_value = image_array[y_root+1][midpoint]
            next_pixel_is_black = self.__pixel_is_black(next_pixel_value)

            if next_pixel_is_black:
                continue # we're assuming for now all lines are 1px thick

            # now we'll find the spacing between this ledger and the next one

            ledger_spacing = 0

            for y_spacing in range(y_root+1, image_height):
                spacing_pixel_value = image_array[y_spacing][midpoint+1]
                spacing_pixel_is_black = self.__pixel_is_black(spacing_pixel_value)

                if (spacing_pixel_is_black):
                    break # we found another ledger line
                else:
                    ledger_spacing += 1 # we found another row of spacing

            # now we must verify that the spacing can predict the next ledger lines
            # firstly, verify that the expected ledger lines are black

            num_non_black = 0

            # make sure it's possible to fit a staff below
            if (y_root + ledger_spacing * 4) > self.get_height():
                continue # continue

            # now we check if we're probably looking at a ledger line
            # we'll make sure there's 5 ledger lines within the amount
            # of space we analyze (ledger_spacing*5+5) (5 for threshold)
            num_black = 0
            num_pixels = ledger_spacing*5+5

            for y_ledger in range(num_pixels):
                pixel_value = image_array[y_ledger][midpoint]
                pixel_value_is_black = self.__pixel_is_black(pixel_value)
                num_black += pixel_value_is_black

            if (num_black != 5):
                continue # we found too many black pixels

            print(num_black)

            # for now, we'll assume this is good enough to prove we found a staff
            return y_root

    def __get_staff_x_values(self):
        # returns the global x staff positions as tuple of (begin, end)
        pass

    def __pixel_is_black(self, pixel_value):
        # returns true if the given pixel is "close enough" to black
        threshold = 20 # less than threshold is black
        return (pixel_value < threshold)

    def __get_row(self, row_number):
        return self.get_image_array()[row_number]

    def get_column(self, row_number):
        column = []
        image_array = self.get_image_array()
        image_height = self.get_height()

        for y in range(image_height-25):
            current_pixel_value = image_array[y][row_number]
            current_pixel_is_black = self.__pixel_is_black(current_pixel_value)
            column.append(current_pixel_is_black)

        return column

if __name__=="__main__":
    s = SheetImage("../../bin/mary-had-a-little-lamb.gif")
    print s.get_staff(0)
