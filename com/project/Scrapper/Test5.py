# test_example.py

from com.project.Logger.CustomLogger import CustomLogger

class TestExample:

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

# Example usage:




