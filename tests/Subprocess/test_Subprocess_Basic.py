import os
import re

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestSubprocessBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestSubprocessBasic, self).setUp()

    def test_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix_dryrun(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--dry-run'])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix_cwd(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess(['blah.txt'], cwd=self.workingDir)
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_nodatemoveneeded(self):
        filename = os.path.join(self.workingDir, '2015-01-01-blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_nodatemoveneeded2(self):
        filename = os.path.join(self.workingDir, '2015-01-01T12-00-00-blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_nodatemoveneeded_partial(self):
        filename = os.path.join(self.workingDir, '2015-01-blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove_partial(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_datemove_partial(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-bling.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-blah-bling.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove_underscore(self):
        filename = os.path.join(self.workingDir, 'blah_2015_01_01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove2(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-01-bling.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah-bling.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove2_underscore(self):
        filename = os.path.join(self.workingDir, 'blah_2015_01_01_bling.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah_bling.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix_interactive_yes(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], feedInput=b'y', extraParams=['--interactive'], expectOutput=True)
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertRegex(output, 'Move ' + re.escape(filename) + '.*')
        self.assertEqual('', error)

    def test_basicdateprefix_interactive_no(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], feedInput=b'n', extraParams=['--interactive'], expectOutput=True)
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertRegex(output, 'Move ' + re.escape(filename) + '.*')
        self.assertEqual('', error)

    def test_basicdateprefix_interactive_oneyesoneno(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        filename2 = os.path.join(self.workingDir, 'blah2.txt')
        self.touch(filename)
        self.touch(filename2)
        (rc, output, error) = self.invokeAsSubprocess([filename, filename2], feedInput=b'yn', extraParams=['--interactive'],
                                                      expectOutput=True)
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(filename2))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah2.txt')))
        self.assertEqual(2, self.directoryFileCount(self.workingDir))
        self.assertRegex(output, '(?is)Move ' + re.escape(filename) + ".*Move " + re.escape(filename2) + '.*')
        self.assertEqual('', error)

    def test_basicdateprefix_interactive_oneyesquit(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        filename2 = os.path.join(self.workingDir, 'blah2.txt')
        filename3 = os.path.join(self.workingDir, 'blah3.txt')
        self.touch(filename)
        self.touch(filename2)
        self.touch(filename3)
        (rc, output, error) = self.invokeAsSubprocess([filename, filename2, filename3],
                                                      feedInput=b'yqy', extraParams=['--interactive'],
                                                      expectOutput=True)
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(filename2))
        self.assertTrue(os.path.exists(filename3))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah2.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah3.txt')))
        self.assertEqual(3, self.directoryFileCount(self.workingDir))
        self.assertRegex(output, '(?is)Move ' + re.escape(filename) + '.*Move ' + re.escape(filename2) + '.*')
        self.assertEqual('', error)
