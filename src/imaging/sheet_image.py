from PIL import Image
import math
import numpy as np

class SheetImage:
    def __init__(self, source_image_path):
        # initializes image metadata from analyzing image
        self.image = Image.open(source_image_path)
        self.image_array = np.asarray(self.image)

    # static methods used for image analysis on both the main image
    # as well as its constituents
    @staticmethod
    def get_width(image):
        # returns the width of the provided image
        return SheetImage.get_dimensions(image)[0]

    @staticmethod
    def get_height(image):
        # returns the width of the provided image
        return SheetImage.get_dimensions(image)[1]

    @staticmethod
    def get_midpoint(image):
        # returns x-midpoint of the provided image
        return int(math.ceil(SheetImage.get_width(image)/2))

    @staticmethod
    def get_dimensions(image):
        # returns tuple of (width, height) of the provided image
        image_array_shape = np.asarray(image).shape
        return image_array_shape[1], image_array_shape[0]

    @staticmethod
    def pixel_is_black(image, x, y, threshold=20):
        # returns true if the given pixel is "within threshold values" to black
        pixel_value = SheetImage.get_pixel_value(image, x, y)
        return pixel_value < threshold

    @staticmethod
    def get_pixel_value(image, x, y):
        return np.asarray(image)[y][x]

    @staticmethod
    def get_row(image, row_number):
        return np.asarray(image)[row_number]

    @staticmethod
    def get_column(image, row_number):
        column = []
        image_height = SheetImage.get_height(image)

        for y in range(image_height):
            column.append(np.asarray(image)[y][row_number])

        return column

    def get_notes(self):
        # returns a list of note images from sheet music image
        print("Attempting to parse notes.")

        staff_images = self.__get_staff_images()
        notes = []

        for staff in staff_images:
            print("Analyzing a staff.")
            width = SheetImage.get_width(staff)
            height = SheetImage.get_height(staff)

            # get the number of black pixels for a staff with no notes
            # to get this, we'll scan the staff and take the least amount of black pixels found
            least_found = None

            for x in range(0, width):
                number_found = 0
                for y in range(0, height):
                    if SheetImage.pixel_is_black(staff, x, y):
                        number_found += 1
                if number_found < least_found or least_found is None:
                    least_found = number_found

            empty_staff_black_pixel_count = least_found
            # now that we have the amount of black pixels expected in a column where there is no
            # note, we can begin to slice out the actual notes

            scanning_note = False
            note_begin = None
            note_end = None

            for x in range(0, width):
                number_found = 0
                for y in range(0, height):
                    if SheetImage.pixel_is_black(staff, x, y):
                        number_found += 1
                if empty_staff_black_pixel_count == number_found: # we're still looking for a note
                    if scanning_note:
                        # we found the end of the note
                        note_end = x-1
                        scanning_note = False
                        # as a rough way to check that it is, in fact, a note, check that it's width > 3px
                        if (note_end - note_begin > 3):
                            # add some image padding
                            note_begin -= 2
                            note_end += 2
                            note = staff.crop((note_begin, 0, note_end, height-1))
                            notes.append(note)
                            print("Found a note.")
                        else:
                            pass # we're probably looking at a divider
                    else:
                        # just keep looking
                        pass
                else:
                    if scanning_note:
                        # we already know we're looking at a note, find the end
                        pass
                    else:
                        # found the end of the note
                        scanning_note = True
                        note_begin = x

        return notes

    def __get_staff_images(self):
        # returns images of the staffs
        staff_positions = self.__get_staffs_positions()
        staff_images = []

        for i, p in enumerate(staff_positions):
            x1 = p[0]
            y1 = p[1]
            x2 = p[0]+p[2]
            y2 = p[1]+p[3]
            image = self.image.crop((x1, y1, x2, y2))
            staff_images.append(image)

        return staff_images

    def __get_staffs_positions(self):
        # returns 4-tuples of staff dimensions
        # takes a staff_ys_list from get_staff_ys()

        # get the first staff y-values
        staff_ys_list = self.__get_all_staffs_ys()
        first_staff = staff_ys_list[0]

        first_staffs_ys = range(first_staff[0], first_staff[1])
        staff_x_beginning = 0
        staff_x_end = SheetImage.get_width(self.image)

        # starting from the middle of the page, go left until black pixels aren't found
        for x in reversed(range(0, SheetImage.get_midpoint(self.image))):
            found_black = False
            for y in first_staffs_ys:
                current_pixel = SheetImage.pixel_is_black(self.image, x, y, 20)
                found_black = found_black or current_pixel
            if not found_black:
                staff_x_beginning = x+3
                break

        # starting from the middle of the page, go right until black pixels aren't found
        for x in range(SheetImage.get_midpoint(self.image), SheetImage.get_width(self.image)):
            found_black = False
            for y in first_staffs_ys:
                current_pixel = SheetImage.pixel_is_black(self.image, x, y, 20)
                found_black = found_black or current_pixel
            if not found_black:
                staff_x_end = x-2
                break

        staff_positions_without_padding = []

        # compile list of x, y, width, height of staffs
        for staff_ys in staff_ys_list:
            x = staff_x_beginning
            width = staff_x_end - staff_x_beginning
            y = staff_ys[0]
            height = staff_ys[1] - staff_ys[0]
            dimensions = (x, y, width, height)
            staff_positions_without_padding.append(dimensions)

        # add paddings to support off-staff notes
        final_staff_positions = []

        # determine padding as half of distance between staff 1 and 2
        for staff_position in staff_positions_without_padding:
            height = staff_position[3]
            padding = int(height / 2)

            width = staff_position[2]
            height += padding * 2
            x = staff_position[0]
            y = staff_position[1] - padding
            final_staff_positions.append((x, y, width, height))

        return final_staff_positions

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
        midpoint = SheetImage.get_midpoint(self.image)
        image_height = SheetImage.get_height(self.image)
        staff_spacing_variance = 5

        for y_root in range(vertical_offset+1, image_height-25):
            current_pixel_is_black = SheetImage.pixel_is_black(self.image, midpoint, y_root, 20)

            if not current_pixel_is_black:
                continue # haven't found the first ledger line yet
            
            # now we've possibly found the first ledger line
            next_pixel_is_black = SheetImage.pixel_is_black(self.image, midpoint, y_root+1, 20)

            if next_pixel_is_black:
                continue # we're assuming for now all lines are 1px thick

            # now we'll find the spacing between this ledger and the next one

            ledger_spacing = 0

            for y_spacing in range(y_root+1, image_height):
                spacing_pixel_is_black = SheetImage.pixel_is_black(self.image, midpoint+1, y_spacing, 20)

                if (spacing_pixel_is_black):
                    break # we found another ledger line
                else:
                    ledger_spacing += 1 # we found another row of spacing

            # now we must verify that the spacing can predict the next ledger lines
            # firstly, verify that the expected ledger lines are black

            num_non_black = 0

            # make sure it's possible to fit a staff below
            if (y_root + ledger_spacing * 4) > SheetImage.get_height(self.image):
                continue # continue

            # now we check if we're probably looking at a ledger line
            # we'll make sure there's 5 ledger lines within the amount
            # of space we analyze (ledger_spacing*5+5) (5 for threshold)
            num_black = 0
            num_pixels = ledger_spacing*(5)+staff_spacing_variance

            for y_ledger in range(num_pixels):
                pixel_value_is_black = SheetImage.pixel_is_black(self.image, midpoint, y_root+y_ledger, 20)
                num_black += pixel_value_is_black

            if (num_black != 5):
                continue # we found too many black pixels

            # for now, we'll assume this is good enough to prove we found a staff
            return (y_root-staff_spacing_variance, y_root+ledger_spacing*5+staff_spacing_variance)

        return None # we couldn't find any staff

if __name__=="__main__":
    s = SheetImage("../../bin/mary-had-a-little-lamb.gif")
    notes = s.get_notes()
    for i, note in enumerate(notes):
        note.save(str(i)+".gif")