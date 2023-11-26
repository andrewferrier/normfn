import os.path

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestSubprocessArguments(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestSubprocessArguments, self).setUp()

    def test_no_basicdateprefix(self):
        (rc, output, error) = self.invokeAsSubprocess([], extraParams=['--help'], expectOutput=True)
        self.assertEqual(0, rc)
        self.assertEqual(0, self.directoryFileCount(self.workingDir))
        self.assertEqual('', error)

    def test_verbose(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--verbose'])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertRegex(error, 'moved to')

    def test_verbose_impliedby_dryrun(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--dry-run'])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertRegex(error, '(?i)not moving.*dry run')

    def test_recursive_current_directory(self):
        subWorkingDir = os.path.join(self.workingDir, 'subWorkingDir')
        filename = os.path.join(subWorkingDir, 'foobar.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess(['.'], extraParams=['--recursive', '-vv'], cwd=subWorkingDir)
        print(f"DEBUGPRINT[2]: test_Subprocess_Arguments.py:42: error={error}")
        print(f"DEBUGPRINT[1]: test_Subprocess_Arguments.py:42: output={output}")
        self.assertEqual(0, rc)
        self.assertEqual('', error)
        newsubWorkingDir = os.path.join(self.workingDir, self.getDatePrefix() + 'subWorkingDir')
        self.assertPathDoesntExist(filename)
        self.assertPathDoesntExist(subWorkingDir)
        self.assertPathExists(os.path.join(newsubWorkingDir, self.getDatePrefix() + 'foobar.txt'))
        self.assertEqual(1, self.directoryFileCount(newsubWorkingDir))

    def test_recursive_current_directory_interactive(self):
        subWorkingDir = os.path.join(self.workingDir, 'subWorkingDir')
        filename = os.path.join(subWorkingDir, 'foobar.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess(['.'], feedInput=b'ny',
                                                      extraParams=['--interactive', '--recursive'],
                                                      cwd=subWorkingDir, expectOutput=True)
        self.assertEqual(0, rc)
        self.assertEqual('', error)
        self.assertPathDoesntExist(filename)
        self.assertPathExists(subWorkingDir)
        self.assertPathExists(os.path.join(subWorkingDir, self.getDatePrefix() + 'foobar.txt'))
        self.assertEqual(1, self.directoryFileCount(subWorkingDir))

    def test_recursive_current_directory_interactive_with_dotfile(self):
        subWorkingDir = os.path.join(self.workingDir, 'subWorkingDir')
        filename = os.path.join(subWorkingDir, '.bar.txt')
        filename2 = os.path.join(subWorkingDir, 'foo.txt')
        self.touch(filename)
        self.touch(filename2)
        (rc, output, error) = self.invokeAsSubprocess(['.'], feedInput=b'ny',
                                                      extraParams=['--interactive', '--recursive'],
                                                      cwd=subWorkingDir, expectOutput=True)
        self.assertEqual(0, rc)
        self.assertEqual('', error)
        self.assertPathExists(filename)
        self.assertPathExists(subWorkingDir)
        self.assertPathDoesntExist(filename2)
        self.assertPathExists(os.path.join(subWorkingDir, self.getDatePrefix() + 'foo.txt'))
        self.assertEqual(2, self.directoryFileCount(subWorkingDir))

    def test_loads_of_files(self):
        TOTAL_FILES = 100
        filenames = [('filename' + str(i) + '.txt') for i in range(TOTAL_FILES)]
        for filename in filenames:
            self.touch(os.path.join(self.workingDir, filename))
        self.assertEqual(TOTAL_FILES, self.directoryFileCount(self.workingDir))
        (rc, output, error) = self.invokeAsSubprocess(filenames, extraParams=['-vv'])
        self.assertEqual(0, rc)
        self.assertNotRegex(error, 'exception')
        self.assertEqual(TOTAL_FILES, self.directoryFileCount(self.workingDir))
        for filename in filenames:
            self.assertPathDoesntExist(os.path.join(self.workingDir, filename))
            self.assertPathExists(os.path.join(self.workingDir, self.getDatePrefix() + filename))
