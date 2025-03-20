import unittest
import os

def load_tests():
    # Discover and load all test files in the database_tests folder
    test_loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_suite = test_loader.discover(test_dir, pattern="test_*.py")
    return test_suite

if __name__ == "__main__":
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = load_tests()
    runner.run(test_suite)
    print(f"\n\n\nAll failures are explained in the testing document\n\n\n")