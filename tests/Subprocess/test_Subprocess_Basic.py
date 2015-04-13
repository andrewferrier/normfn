import os

from freezegun import freeze_time
from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestSubprocessBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestSubprocessBasic, self).setUp()

    def test_no_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--no-prefix-date'])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix_dryrun(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--dry-run'])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix_cwd(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess(['blah.txt'], cwd=self.workingDir)
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_nodatemoveneeded(self):
        filename = os.path.join(self.workingDir, '2015-01-01-blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_nodatemoveneeded2(self):
        filename = os.path.join(self.workingDir, '2015-01-01T12-00-00-blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_nodatemoveneeded_partial(self):
        filename = os.path.join(self.workingDir, '2015-01-blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove_partial(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_datemove_partial(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-bling.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-blah-bling.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove_underscore(self):
        filename = os.path.join(self.workingDir, 'blah_2015_01_01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove2(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-01-bling.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah-bling.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove2_underscore(self):
        filename = os.path.join(self.workingDir, 'blah_2015_01_01_bling.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah_bling.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)
