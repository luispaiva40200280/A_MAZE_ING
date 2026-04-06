import unittest
import os
import tempfile
from pydantic import ValidationError

# Make sure this import matches your exact file structure!
from Maze_Generation.helper_maze_classes import MazeConfig


class TestMazeConfigParser(unittest.TestCase):

    def setUp(self):
        """This runs before every test to create a placeholder variable."""
        self.temp_filepath = ""

    def create_temp_config(self, content: str) -> str:
        """Helper function to create a temporary text file with
        custom content."""
        temp = tempfile.NamedTemporaryFile(delete=False,
                                           mode='w', suffix='.txt')
        temp.write(content)
        temp.close()
        self.temp_filepath = temp.name
        return self.temp_filepath

    def tearDown(self):
        """This runs after every test to clean up the fake files."""
        if os.path.exists(self.temp_filepath):
            os.remove(self.temp_filepath)

    # --- THE TESTS ---

    def test_valid_config_parses_correctly(self):
        content = """
        # This is a comment
        width=20
        height=15
        entry=0,0
        exit=19,14
        perfect=True
        """
        filepath = self.create_temp_config(content)
        config = MazeConfig.parser_file(filepath)

        self.assertEqual(config.width, 20)
        self.assertEqual(config.height, 15)
        self.assertEqual(config.entry, (0, 0))
        self.assertEqual(config.exit, (19, 14))
        self.assertTrue(config.perfect)

    def test_file_not_found_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            MazeConfig.parser_file("ghost_file_that_does_not_exist.txt")

    def test_duplicate_keys_raises_value_error(self):
        filepath = "../configs/config.txt"

        with self.assertRaises(ValueError) as context:
            MazeConfig.parser_file(filepath)

        self.assertIn("Duplicated values", str(context.exception))

    def test_out_of_bounds_entry_raises_validation_error(self):
        content = """
        width=10
        height=10
        entry=15,15  # Out of bounds!
        exit=9,9
        """
        filepath = self.create_temp_config(content)

        # Pydantic wraps our custom ValueErrors inside a ValidationError
        with self.assertRaises(ValidationError) as context:
            MazeConfig.parser_file(filepath)

        self.assertIn("outside the bounds", str(context.exception))

    def test_negative_width_raises_validation_error(self):
        content = """
        width=-5  # Less than 0!
        height=10
        entry=0,0
        exit=9,9
        """
        filepath = self.create_temp_config(content)

        with self.assertRaises(ValidationError) as context:
            MazeConfig.parser_file(filepath)

        self.assertIn("Input should be greater than 0", str(context.exception))


if __name__ == "__main__":
    unittest.main()
