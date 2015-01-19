from difflib import get_close_matches as gcm
from copy import deepcopy
from inspect import getmembers, isfunction, isclass, ismethod


def extract_function_names(module, desired_names):
    extracted_functions = getmembers(module, isfunction)
    return _get_best_matches(extracted_functions, desired_names)


def extract_class_names(module, desired_names):
    extracted_classes = getmembers(module, isclass)
    return _get_best_matches(extracted_classes, desired_names)


def extract_methods(class_, desired_names):
    extracted_methods = getmembers(class_, ismethod)
    return _get_best_matches(extracted_methods, desired_names)


def normalize_filenames(submitted_filenames, desired_filenames):
    return _get_best_matches(submitted_filenames, desired_filenames)


def _get_best_matches(user_supplied, api_specified):
    normalized_names = {}
    safe_user_supplied = deepcopy(user_supplied)
    for specified in api_specified:
        matches = gcm(specified, safe_user_supplied)
        normalized_names[specified] = matches
    without_duplicates = _resolve_duplicates(normalized_names)
    return without_duplicates


def _resolve_duplicates(name_maps):
    best_matches = [match[0] for match in name_maps.itervalues()]
    if len(set(best_matches)) == len(best_matches):
        return {name:match[0] for name, match in name_maps.iteritems()}
    else:
        duplicates_removed = {}
        good_names = sorted(name_maps)
        used_names = []
        for name in good_names:
            for match in name_maps[name]:
                if match not in used_names:
                    used_names.append(match)
                    duplicates_removed[name] = match
                    break
            else:
                # There were no matches that aren't already taken
                duplicates_removed[name] = None
        return duplicates_removed


def voodoo(function_name):
    pass
