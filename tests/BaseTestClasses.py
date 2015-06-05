from datetime import datetime
from subprocess import Popen, PIPE
from contextlib import contextmanager
import inspect
import io
import logging
import os
import os.path
import pexpect
import shutil
import tempfile
import unittest


class NormalizeFilenameTestCase(unittest.TestCase):
    COMMAND = os.path.normpath(os.path.join(os.getcwd(), 'normalize-filename'))

    def setUp(self):
        self.workingDir = tempfile.mkdtemp(dir='/tmp')

    def getDatePrefix(self):
        return datetime.now().strftime("%Y-%m-%d-")

    def getDateAndTimePrefix(self):
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S-")

    def directoryFileCount(self, directory):
        return len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

    def getOriginalScriptPath(self):
        module_path = inspect.getfile(inspect.currentframe())
        module_path = os.path.join(os.path.dirname(os.path.dirname(module_path)), 'normalize-filename')

        return module_path

    def invokeDirectly(self, inputFiles, extraParams=[]):
        import importlib.machinery
        module_path = self.getOriginalScriptPath()
        loader = importlib.machinery.SourceFileLoader('normalize-filename', module_path)
        normalize_filename = loader.load_module()

        options = [module_path]

        options.extend(inputFiles)
        options.extend(extraParams)

        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        log = logging.getLogger('normalize-filename')
        log.propagate = False
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)

        self.timeInvoked = datetime.now()

        try:
            normalize_filename.main(options, None, handler)
        finally:
            self.timeCompleted = datetime.now()
            log.removeHandler(handler)
            handler.close()

        error = stream.getvalue()

        return error

    def invokeAsSubprocess(self, inputFiles, extraParams=[], feedInput=None, cwd=None, expectOutput=False):
        if cwd is None:
            cwd = self.workingDir

        options = [NormalizeFilenameTestCase.COMMAND]

        options.extend(inputFiles)

        options.extend(extraParams)

        if feedInput:
            p = Popen(options, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
        else:
            p = Popen(options, stdin=None, stdout=PIPE, stderr=PIPE, cwd=cwd)

        output, error = p.communicate(feedInput)
        p.wait()

        output = str(output, "utf-8")
        error = str(error, "utf-8")

        if expectOutput:
            self.assertNotEqual("", output)
        else:
            self.assertEqual("", output)

        return (p.returncode, output, error)

    @contextmanager
    def invokeAsPexpect(self, inputFiles, extraParams=[], expectedExitStatus=None, expectedOutputRegex=None):
        options = [NormalizeFilenameTestCase.COMMAND]
        options.extend(inputFiles)
        options.extend(extraParams)

        command = ' '.join(options)

        stream = io.BytesIO()

        child = pexpect.spawn(command)
        child.logfile_read = stream

        yield child

        child.expect(pexpect.EOF)
        child.close()

        if expectedExitStatus is not None:
            self.assertEqual(expectedExitStatus, child.exitstatus)

        if expectedOutputRegex is not None:
            self.assertRegex(str(child.logfile_read.getvalue(), 'utf-8'), expectedOutputRegex)

    def touch(self, fname):
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        open(fname, 'w').close()

    def writeFile(self, fname, contents):
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, 'w') as filename:
            filename.write(contents)

    def readFile(self, fname):
        with open(fname, 'r') as filename:
            return filename.read()

    def assertPathDoesntExist(self, path):
        self.assertFalse(os.path.exists(path))

    def assertPathExists(self, path):
        self.assertTrue(os.path.exists(path))

    def tearDown(self):
        shutil.rmtree(self.workingDir)
