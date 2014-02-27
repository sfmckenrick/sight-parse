from PIL import Image
import math
import numpy as np

class SheetImage:
    def __init__(self, source_image_path):
        # initializes image metadata from analyzing image
        self.image = Image.open(source_image_path)
        self.image_array = np.asarray(self.image)

    def get_width(self):
        # returns the width of the sheet music image
        return self.get_dimensions()[0]
    
    def get_height(self):
        # returns height of sheet music image
        return self.get_dimensions()[1]

    def get_midpoint(self):
        # returns x-midpoint of sheet music image
        return int(math.ceil(self.get_width()/2))

    def get_dimensions(self):
        # returns tuple of (width, height) of the test sheet music
        image_array_shape = self.image_array.shape
        return(image_array_shape[1], image_array_shape[0])

    def __get_all_staffs_ys(self):
        # returns list of staff y positions tuples: [(beg, end)]
        staffs_ys_list = []
        found_staff = True
        while (found_staff):
            current_staff_ys = self.__get_first_staff_ys(staffs_ys_list[-1][1] if len(staffs_ys_list) > 0 else 0)
            if (current_staff_ys == None):
                found_staff = False
            else:
                staffs_ys_list.append(current_staff_ys)

        return staffs_ys_list

    def __get_first_staff_ys(self, vertical_offset):
        # returns a tuple of the beginning and end y positions of the first staff
        # found below the provided vertical_offset
        midpoint = self.get_midpoint()
        image_height = self.get_height()
        staff_spacing_variance = 5

        for y_root in range(vertical_offset+1, image_height-25):
            current_pixel_is_black = self.__pixel_is_black(midpoint, y_root)

            if not current_pixel_is_black:
                continue # haven't found the first ledger line yet
            
            # now we've possibly found the first ledger line
            next_pixel_is_black = self.__pixel_is_black(midpoint, y_root+1)

            if next_pixel_is_black:
                continue # we're assuming for now all lines are 1px thick

            # now we'll find the spacing between this ledger and the next one

            ledger_spacing = 0

            for y_spacing in range(y_root+1, image_height):
                spacing_pixel_is_black = self.__pixel_is_black(midpoint+1, y_spacing)

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
            num_pixels = ledger_spacing*(5)+staff_spacing_variance

            for y_ledger in range(num_pixels):
                pixel_value_is_black = self.__pixel_is_black(midpoint, y_root+y_ledger)
                num_black += pixel_value_is_black

            if (num_black != 5):
                continue # we found too many black pixels

            # for now, we'll assume this is good enough to prove we found a staff
            return (y_root-staff_spacing_variance, y_root+ledger_spacing*5+staff_spacing_variance)

        return None # we couldn't find any staff

    def get_staffs_positions(self):
        # returns 4-tuples of staff dimensions
        # takes a staff_ys_list from get_staff_ys()

        # get the first staff y-values
        staff_ys_list = self.__get_all_staffs_ys()
        first_staff = staff_ys_list[0]

        first_staffs_ys = range(first_staff[0], first_staff[1])
        staff_x_beginning = 0
        staff_x_end = self.get_width()

        # starting from the middle of the page, go left until black pixels aren't found
        for x in reversed(range(0, self.get_midpoint())):
            found_black = False
            for y in first_staffs_ys:
                current_pixel = self.__pixel_is_black(x, y)
                found_black = found_black or current_pixel
            if not found_black:
                staff_x_beginning = x
                break

        # starting from the middle of the page, go right until black pixels aren't found
        for x in range(self.get_midpoint(), self.get_width()):
            found_black = False
            for y in first_staffs_ys:
                current_pixel = self.__pixel_is_black(x, y)
                found_black = found_black or current_pixel
            if not found_black:
                staff_x_end = x
                break

        final_staff_positions = []
        # compile list of x, y, width, height of staffs
        for staff_ys in staff_ys_list:
            x = staff_x_beginning
            width = staff_x_end - staff_x_beginning
            y = staff_ys[0]
            height = staff_ys[1] - staff_ys[0]
            dimensions = (x, y, width, height)
            final_staff_positions.append(dimensions)

        return final_staff_positions

    def __pixel_is_black(self, x, y):
        # returns true if the given pixel is "close enough" to black
        pixel_value = self.__get_pixel_value(x, y)
        threshold = 20 # less than threshold is black
        return (pixel_value < threshold)

    def __get_pixel_value(self, x, y):
        return self.image_array[y][x]

    def __get_row(self, row_number):
        return self.image_array()[row_number]

    def get_column(self, row_number):
        column = []
        image_height = self.get_height()

        for y in range(image_height-25):
            current_pixel_value = self.image_array[y][row_number]
            current_pixel_is_black = self.__pixel_is_black(current_pixel_value)
            column.append(current_pixel_is_black)

        return column

if __name__=="__main__":
    s = SheetImage("../../bin/mary-had-a-little-lamb.gif")
    print(s.get_staffs_positions())
