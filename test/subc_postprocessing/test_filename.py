
import pytest
import unittest

from pathlib import PosixPath

from subc_postprocessing import filenames


class TestFilenames( unittest.TestCase ):

    def test_filename(self):

        self.assertEqual(PosixPath("2021-01-18T23:46:58.764.dng"), filenames.regularize_filename("2021.1.18 23.46.58.764.dng"))
