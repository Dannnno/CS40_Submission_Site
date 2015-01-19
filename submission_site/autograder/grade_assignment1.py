from importlib import import_module

from ..utilities import extract_function_names, voodoo, \
    normalize_filenames


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
        function1 = functions[0]
        test_function1(function1)


def test_function1(function):
    pass
