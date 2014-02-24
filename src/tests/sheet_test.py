from imaging import sheet
import numpy
import unittest

class TestSheetFunctions(unittest.TestCase):
    def setUp(self):
        # prepare numpy
        numpy.set_printoptions(threshold=numpy.nan)
        # create sheet music from mary had a little lamb gif
        self.lamb_sheet = sheet.Sheet('../../bin/mary-had-a-little-lamb.gif')
        # hardcoded test values from marry had a little lamb gif
        self.REAL_WIDTH = 469;
        self.REAL_HEIGHT = 520;
        self.REAL_MIDPOINT = 469/2;

    def test_to_array(self):
        # test that array is not empty or null
        self.assertTrue(self.lamb_sheet.image_array != None)
        self.assertTrue(self.lamb_sheet.image_array.size > 0)

    def test_dimensions(self):
        # test that the correct midpoint of width is found
        self.assertTrue((self.lamb_sheet.width == self.REAL_WIDTH),
            ("Width Found: " + str(self.lamb_sheet.width) + 
            ", expected: " + str(self.REAL_WIDTH)))
        self.assertTrue((self.lamb_sheet.height == self.REAL_HEIGHT),
            ("Height Found: " + str(self.lamb_sheet.height) + 
            ", expected: " + str(self.REAL_HEIGHT)))
        self.assertTrue((self.lamb_sheet.midpoint == self.REAL_MIDPOINT),
            ("Midpoint Found: " + str(self.lamb_sheet.midpoint) + 
            ", expected: " + str(self.REAL_MIDPOINT)))

    def test_beginning_whitespace(self):
        self.lamb_sheet.find_beginning_whitespace()

if __name__ == '__main__':
    unittest.main()
