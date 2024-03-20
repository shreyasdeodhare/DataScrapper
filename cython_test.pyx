# cython_test.pyx
from com.project.Logger import CustomLogger

cdef class TestExample:
    @CustomLogger.log_around
    def test_addition(self, param1, param2):
        """
        Test addition functionality.
        """
        result = param1 + param2
        return result

    @staticmethod
    @CustomLogger.log_around
    def test_subtraction(param1, param2):
        """
        Test subtraction functionality.
        """
        result = param1 - param2
        return result