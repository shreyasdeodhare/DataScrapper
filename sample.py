from com.project.Scrapper.Test5 import TestExample


if __name__ == "__main__":
    test_instance = TestExample()

    # Call the decorated test methods
    print(test_instance.test_addition(10, 20))
    print(test_instance.test_subtraction(10, 20))

