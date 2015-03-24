from datetime import datetime
from subprocess import Popen, PIPE
import os
import os.path
import shutil
import tempfile
import unittest


class NormalizeFilenameTestCase(unittest.TestCase):
    COMMAND = os.path.normpath(os.path.join(os.getcwd(), 'normalize-filename'))

    def setUp(self):
        self.workingDir = tempfile.mkdtemp(dir='/tmp')

    def getDatePrefix(self):
        return datetime.now().strftime("%Y-%m-%d-")

    def directoryCount(self, directory):
        return len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

    def invokeAsSubprocess(self, inputFiles, extraParams=[], cwd=None):
        if cwd is None:
            cwd = self.workingDir

        options = [NormalizeFilenameTestCase.COMMAND]

        options.extend(inputFiles)

        options.extend(extraParams)

        p = Popen(options, stdout=PIPE, stderr=PIPE, cwd=cwd)

        output, error = p.communicate()
        p.wait()

        output = str(output, "utf-8")
        error = str(error, "utf-8")

        self.assertEqual("", output)

        return (p.returncode, output, error)

    def touch(self, fname):
        open(fname, 'w').close()

    def tearDown(self):
        shutil.rmtree(self.workingDir)
