# -*- coding: utf-8 -*-

from .context import aimay

import unittest

class TestMain(unittest.TestCase):

  def test_f(self):
    self.assertEqual(3, main.f())

if __name__ == "__main__":
    unittest.main()