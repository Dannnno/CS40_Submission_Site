from importlib import import_module

from submission_site.sub_site.handle_database import query_db
from submission_site.exceptions import InvalidAssignmentException


def grade_assignment(assignment_id, submitted_files):
    try:
        required_files = _find_assignment(assignment_id))
    except InvalidAssignmentException:
        return {}

    autograder = import_module("grade_assignment{}".format(assignment_id),
                                package="submission_site.autograder")
    grade_results = autograder.grade(submitted_files)
    return grade_results


def _find_assignment(id_):
    query = "SELECT * FROM assignments WHERE assignmentid=?"
    args = (id_,)
    query_result = query_db(query, args)
    if query_result:
        required_files = query_result[0]
        return required_files
    else:
        raise InvalidAssignmentException(
            "No assignment id #{}".format(assignment_id))
