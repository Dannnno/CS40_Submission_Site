__all__ = ['grade_assignment1']


class TestFunction(object):

    def __init__(self, function, str_test):
        self.func = function
        self.run_test_suite()
        self.str_test = 'Testing {}'.format(str_test)

    def run_test_suite(self):
        methods = [method for method in getmembers(self, ismethod)
                   if method.__name__.startswith('test_')]
        self.tests = {method.__name__: False for method in methods}
        with open('results.log', 'w') as logfile:
            logfile.write('{}\n\n'.format(self.str_test))
            logfile.write('='*len(self.str_test))
            for method in methods:
                try:
                    method()
                except AssertionError e:
                    logfile.write(
                        'Failed test {}\n'.format(method.__name__))
                    logfile.write("{}\n".format(repr(e)))
                else:
                    logfile.write(
                        'Passed test {}\n'.format(method.__name__))
                    self.tests[method.__name__] = True
        with open('results.log', 'r') as logfile:
            print logfile.read()
