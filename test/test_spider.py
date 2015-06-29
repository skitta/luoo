__author__ = 'skitta'

import unittest

from scripts import spider


class MyTestCase(unittest.TestCase):
    def test_favorite(self):
        source = spider.Spider('28049')
        data_list = source.get_favorite([1])
        print(data_list)
        print(len(data_list))


if __name__ == '__main__':
    unittest.main()
