import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd

from src.extract.scripts import read_and_insert_files_from_directory


class TestReadAndInsertFiles(unittest.TestCase):

    def setUp(self):
        """Setup a test environment for each test case."""
        # Mock session for testing
        self.session = MagicMock()

        # Mock data to insert (adjusted for space-delimited and quoted format)
        self.mock_data = {
            'line_number': [1, 2, 3],
            'character': ['THREEPIO', 'THREEPIO', 'HAN SOLO'],
            'dialogue': ["Did you hear that? They've shut down the main reactor.",
                         "We're doomed!",
                         "I’ve got a bad feeling about this."],
            'script_name': ['file1.txt', 'file1.txt', 'file1.txt'],
        }

        # Mock directory and file path for testing
        self.mock_directory = './tests/mock'
        os.makedirs(self.mock_directory, exist_ok=True)

        # Write mock data to file for testing
        with open(os.path.join(self.mock_directory, 'file1.txt'), 'w') as f:
            f.write('This is a header line\n')  # Line to be skipped
            f.write('"1" "THREEPIO" "Did you hear that? They\'ve shut down the main reactor."\n')
            f.write('"2" "THREEPIO" "We\'re doomed!"\n')
            f.write('"3" "HAN SOLO" "I’ve got a bad feeling about this."\n')

    def tearDown(self):
        """Clean up after each test."""
        self.session.close()
        # Clean up the mock directory
        for filename in os.listdir(self.mock_directory):
            file_path = os.path.join(self.mock_directory, filename)
            os.remove(file_path)
        os.rmdir(self.mock_directory)

    @patch('os.listdir')
    @patch('pandas.read_csv')
    def test_read_and_insert_files_from_directory(self, mock_read_csv, mock_listdir):
        """Test read_and_insert_files_from_directory function."""

        # Mock the listdir to return a list of files
        mock_listdir.return_value = ['file1.txt']

        # Mock the pandas read_csv function to return a DataFrame
        mock_read_csv.return_value = pd.DataFrame(self.mock_data)

        # Mock the session's add and commit methods to avoid actual database interaction
        self.session.add.return_value = None
        self.session.commit.return_value = None

        # Run the function we're testing
        read_and_insert_files_from_directory(self.mock_directory, self.session)

        # Assert that read_csv was called with the correct file paths
        mock_read_csv.assert_called_with(os.path.join(self.mock_directory, 'file1.txt'), delimiter=" ", quotechar='"',
                                         header=None, skiprows=1, escapechar='\\')

        # Assert that add was called for each row in the DataFrame (3 rows in mock_data)
        self.assertEqual(self.session.add.call_count, 3)

        # Assert commit was called once after inserting all records
        self.session.commit.assert_called_once()

        # Verify the data was inserted into the database (using actual session query)
        # Check that the session's add method was called with the expected arguments
        call_args_list = self.session.add.call_args_list
        self.assertEqual(len(call_args_list), 3)  # We inserted 3 rows
        print(call_args_list[0][0][0].line_number)
        # Verify the data for the first record
        script_data = call_args_list[0][0][0]  # The first call to session.add
        print(script_data)
        self.assertEqual(script_data.line_number, 1)
        self.assertEqual(script_data.character, "THREEPIO")
        self.assertEqual(script_data.dialogue, "Did you hear that? They've shut down the main reactor.")
        self.assertEqual(script_data.script_name, 'file1.txt')

        # Verify the data for the second record
        script_data = call_args_list[1][0][0]  # The second call to session.add
        self.assertEqual(script_data.line_number, 2)
        self.assertEqual(script_data.character, "THREEPIO")
        self.assertEqual(script_data.dialogue, "We're doomed!")
        self.assertEqual(script_data.script_name, 'file1.txt')

        # Verify the data for the third record
        script_data = call_args_list[2][0][0]  # The third call to session.add
        self.assertEqual(script_data.line_number, 3)
        self.assertEqual(script_data.character, "HAN SOLO")
        self.assertEqual(script_data.dialogue, "I’ve got a bad feeling about this.")
        self.assertEqual(script_data.script_name, 'file1.txt')


if __name__ == '__main__':
    unittest.main()
