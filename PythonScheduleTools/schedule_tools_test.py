import unittest
import Services.FolderCheckerClass as FolderCheckerClass
import Services.CSVReaderClass as CSVReaderClass

class FolderCheckerTests(unittest.TestCase):
    """FolderChecker.py Unit Tests"""

    @classmethod
    def setUp(self):
        self.folder_checker = FolderCheckerClass.FolderChecker()

    def test_get_file_list(self):
        """get_file_list unit test"""
        # Arrange
        expected = ['test.pdf']
        # Act
        actual = self.folder_checker.get_file_list('TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_full_file_list(self):
        """get_full_file_list unit test"""
        # Arrange
        expected = ['TestData/Dockets/685543/Production/print\\test.pdf']
        # Act
        actual = self.folder_checker.get_full_file_list('TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_file_list_with_date(self):
        """get_file_list_with_date unit test"""
        # Arrange
        expected = [['Sun May  7 10:06:02 2017', 'test.pdf']]
        # Act
        actual = self.folder_checker.get_file_list_with_date(
            'TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_folder_list(self):
        """get_folder_list unit test"""
        # Arrange
        expected = ['672143', '684421', '685543', '687203', '689398']
        # Act
        actual = self.folder_checker.get_folder_list('TestData/Dockets')
        # Assert
        self.assertEqual(actual, expected)

    def test_find_folders(self):
        """find_folders unit test"""
        # Arrange
        expected = ['TestData/Dockets/672143', 'TestData/Dockets/684421']
        # Act
        actual = self.folder_checker.find_folders('TestData/Dockets', ['672143', '684421'])
        # Assert
        self.assertEqual(actual, expected)

    def test_folder_append(self):
        """folder_append unit test"""
        # Arrange
        expected = ['TestData/Dockets/672143']
        # Act
        actual = self.folder_checker.folder_append(['TestData/Dockets/'], '672143')
        # Assert
        self.assertEqual(actual, expected)

    def test_count_files(self):
        """count_files unit test"""
        # Arrange
        expected = [[
            'TestData/Dockets/685543/Production/print',
            1,
            [['Sun May  7 10:06:02 2017', 'test.pdf']]]]
        # Act
        actual = self.folder_checker.count_files(['TestData/Dockets/685543/Production/print'])
        # Assert
        self.assertEqual(actual, expected)

    def test_folder_exists(self):
        """folder_exists unit test"""
        # Arrange
        expected = True
        # Act
        actual = self.folder_checker.folder_exists('TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_files_containing(self):
        """get_files_containing unit test"""
        # Arrange
        expected = [['Sun May  7 10:06:45 2017', 'Test2.pdf']]
        # Act
        actual = self.folder_checker.get_files_containing(
            'TestData/Dockets/684421/Production/Print', "Test2")
        # Assert
        self.assertEqual(actual, expected)
    def test_get_folder_list_with_date(self):
        """get_folder_list_with_date"""
        # Arrange
        expected = [['Sun May  7 09:48:35 2017', 'Print']]
        # Act
        actual = self.folder_checker.get_folder_list_with_date("TestData/Dockets/672143/Production")
        # Assert
        self.assertEqual(actual, expected)

class CSVReaderTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.csv_rdr = CSVReaderClass.CSVReader()
        self.test_csv = 'TestData/ProofLog.csv'


    def test_find_in_csv(self):
        #Arrange
        expected = [['Tue May 16 10:55:02 2017', '690060_690060_FB 001_p1-8.pdf']]
        #Act
        actual = self.csv_rdr.find_in_csv(self.test_csv, '690060')
        #Assert
        self.assertEqual(actual, expected)