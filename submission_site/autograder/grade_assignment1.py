from importlib import import_module
from inspect import getmembers, ismethod

from ..utilities import extract_function_names, voodoo, \
    normalize_filenames

from .. import TestFunction


files = {'ps1.py': 0}


def grade(submitted_files):
    submitted_files = normalize_filenames(submitted_files, files)
    try:
        ps1 = import_module(submitted_files['ps1.py'].partition('.')[0],
                            package='submission_site.submissions'
    except ImportError:
        pass
    except KeyError:
        pass
    else:
        functions = extract_function_names(ps1)
        function1 = voodoo(ps1, functions[0])
        test = TestFunctionOne(function1, "Function 1 of Problem Set 1"))
        print test.tests


class TestFunctionOne(TestFunction):

    def __init__(self, function, str_test):
        super(TestFunctionOne, self).__init__(function, str_test)

    def test_one(self):
        assert not self.func(1)

    def test_two(self):
        assert not self.func(2)

    def test_zero(self):
        assert self.func(0)

    def test_true(self):
        assert self.func(True)

    def test_false(self):
        assert self.func(False)

    def test_empty_collection(self):
        assert not self.func([])

    def test_collection(self):
        assert self.func([1])
