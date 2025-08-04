import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_current_dir(self):
        result = get_files_info("calculator", ".")
        expected = ['Result for current directory:', 'tests.py: file_size=', 'main.py: file_size=', 'is_dir=False', 'is_dir=True', 'pkg: file_size=']
        self.assertTrue(all(x in result for x in expected))
        print(result)

    def test_specific_dir(self):
        result = get_files_info("calculator", "pkg")
        expected = ["Result for 'pkg' directory:", 'calculator.py: file_size=', 'render.py: file_size=', 'is_dir=False']
        self.assertTrue(all(x in result for x in expected))
        print(result)

    def test_outside_workspace(self):
        result = get_files_info("calculator", "/bin")
        expected = """Result for '/bin' directory:
Error: Cannot list "/bin" as it is outside the permitted working directory"""
        self.assertEqual(result, expected)
        print(result)

    def test_outside_workspace_via_relative_path(self):
        result = get_files_info("calculator", "../")
        expected = """Result for '../' directory:
Error: Cannot list "../" as it is outside the permitted working directory"""
        self.assertEqual(result, expected)
        print(result)
        
if __name__ == "__main__":
    unittest.main()