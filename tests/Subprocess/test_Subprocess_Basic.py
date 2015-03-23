import os

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestBasic, self).setUp()

    def test_nochanges(self):
        filename = os.path.join(self.workingDir, 'xyz.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists('2015-01-01-blah.txt'))
        self.assertEqual('', output)
        self.assertEqual('', error)
