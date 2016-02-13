#!/usr/bin/python3

import pipeline_caller
import unittest


class TestPlusOne(unittest.TestCase):

    def test_main_returns_zero_on_success(self):
        self.assertEquals(pipeline_caller.tokenTest(), 1)

    def test_main_returns_zero_on_success(self):
        self.assertEquals(pipeline_caller.tokenTest2(), 2)

if __name__ == '__main__':
    unittest.main()
