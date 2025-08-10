import unittest
from functions.run_python import run_python_file

class TestGetFileContent(unittest.TestCase):

    def test_run_main(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        self.assertTrue("STDOUT:" in result)

    def test_run_with_args(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)
        self.assertTrue("STDOUT" in result)

    def test_run_test(self):
        result = run_python_file("calculator", "tests.py")
        print(result)
        self.assertTrue("OK" in result)

    def test_bad_path(self):
        result = run_python_file("calculator", "../main.py")
        self.assertEqual(result, f'Error: Cannot execute "../main.py" as it is outside the permitted working directory')
        print(result)

    def test_nonexistent(self):
        result = run_python_file("calculator", "nonexistent.py")
        self.assertEqual(result, f'Error: File "nonexistent.py" not found.')
        print(result)

    # def test_overwrite(self):
    #     result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    #     self.assertEqual(result, f'Successfully wrote to "lorem.txt" ({len("wait, this isn't lorem ipsum")} characters written)')
    #     print(result)

    # def test_new_file(self):
    #     result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    #     self.assertEqual(result, f'Successfully wrote to "pkg/morelorem.txt" ({len("lorem ipsum dolor sit amet")} characters written)')
    #     print(result)

    # def test_unpermitted(self):
    #     result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    #     self.assertEqual(result, f'Error: Cannot write to "{"/tmp/temp.txt"}" as it is outside the permitted working directory')
    #     print(result)

    # def test_main(self):
    #     result = get_file_content("calculator", "main.py")
    #     print(result)
    #     self.assertTrue('expression = " ".join(sys.argv[1:])' in result)
    
    # def test_calculator(self):
    #     result = get_file_content("calculator", "pkg/calculator.py")
    #     print(result)
    #     self.assertTrue('values.append(self.operators[operator](a, b))' in result)
    
    # def test_restricted_path(self):
    #     result = get_file_content("calculator", "/bin/cat")
    #     expected = """Error: Cannot list "/bin/cat" as it is outside the permitted working directory"""
    #     self.assertEqual(result, expected)
    #     print(result)
    
    # def test_does_not_exist(self):
    #     result = get_file_content("calculator", "pkg/does_not_exist.py")
    #     expected = 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
    #     self.assertEqual(result, expected)
    #     print(result)

# class TestGetFilesInfo(unittest.TestCase):
#     def test_current_dir(self):
#         result = get_files_info("calculator", ".")
#         expected = ['Result for current directory:', 'tests.py: file_size=', 'main.py: file_size=', 'is_dir=False', 'is_dir=True', 'pkg: file_size=']
#         self.assertTrue(all(x in result for x in expected))
#         print(result)

#     def test_specific_dir(self):
#         result = get_files_info("calculator", "pkg")
#         expected = ["Result for 'pkg' directory:", 'calculator.py: file_size=', 'render.py: file_size=', 'is_dir=False']
#         self.assertTrue(all(x in result for x in expected))
#         print(result)

#     def test_outside_workspace(self):
#         result = get_files_info("calculator", "/bin")
#         expected = """Result for '/bin' directory:
# Error: Cannot list "/bin" as it is outside the permitted working directory"""
#         self.assertEqual(result, expected)
#         print(result)

#     def test_outside_workspace_via_relative_path(self):
#         result = get_files_info("calculator", "../")
#         expected = """Result for '../' directory:
# Error: Cannot list "../" as it is outside the permitted working directory"""
#         self.assertEqual(result, expected)
#         print(result)
        
if __name__ == "__main__":
    unittest.main()