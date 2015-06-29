__author__ = 'skitta'

import unittest

from scripts import ID3


class MyTestCase(unittest.TestCase):
    def test_header(self):
        decoder = ID3.Decoder('../download/3AM.mp3')
        print(decoder.header())


if __name__ == '__main__':
    unittest.main()
