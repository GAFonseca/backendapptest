import unittest
import os
import csv


class TestCSVFormat(unittest.TestCase):
    def test_csv_columns(self):
        csv_filename = 'data/movielist.csv'
        expected_columns = ['year', 'title', 'studios', 'producers', 'winner']

        self.assertTrue(os.path.isfile(csv_filename), f"CSV file '{csv_filename}' not found")

        with open(csv_filename, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)

            self.assertEqual(header, expected_columns, f"CSV file '{csv_filename}' has incorrect columns")


if __name__ == '__main__':
    unittest.main()
