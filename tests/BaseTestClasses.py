from contextlib import contextmanager
from datetime import datetime
from importlib.util import module_from_spec, spec_from_loader
import inspect
import io
import logging
import os
import os.path
import shutil
from stat import S_IRUSR, S_IWUSR, S_IXUSR
from subprocess import PIPE, Popen, call
import tempfile
import unittest

import pexpect


class NormalizeFilenameTestCase(unittest.TestCase):
    COMMAND = os.path.normpath(os.path.join(os.getcwd(), "normfn"))

    def setUp(self):
        self.workingDir = tempfile.mkdtemp()

    def _create_test_config_file(self, config_dir, undo_log_file_path=None, max_years_ahead=5, max_years_behind=30):
        """Helper method to create a test config file with default values."""
        normfn_config_dir = os.path.join(config_dir, "normfn")
        os.makedirs(normfn_config_dir, exist_ok=True)
        
        config_file = os.path.join(normfn_config_dir, "normfn.toml")
        
        with open(config_file, "w") as f:
            f.write(f'max-years-ahead = {max_years_ahead}\n')
            f.write(f'max-years-behind = {max_years_behind}\n')
            if undo_log_file_path is None:
                f.write('undo-log-file = ""\n')
            else:
                f.write(f'undo-log-file = "{undo_log_file_path}"\n')
        
        return config_file

    def getDatePrefix(self, postfixDash=True):
        if postfixDash is True:
            return datetime.now().strftime("%Y-%m-%d-")
        else:
            return datetime.now().strftime("%Y-%m-%d")

    def directoryFileCount(self, directory):
        return len(
            [
                item
                for item in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, item))
            ]
        )

    def directoryDirCount(self, directory):
        return len(
            [
                item
                for item in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, item))
            ]
        )

    def getOriginalScriptPath(self):
        module_path = inspect.getfile(inspect.currentframe())
        module_path = os.path.join(
            os.path.dirname(os.path.dirname(module_path)), "normfn"
        )

        return module_path

    def invokeDirectly(self, inputFiles, extraParams=[], configOverrides=None):
        import importlib.machinery

        module_path = self.getOriginalScriptPath()
        loader = importlib.machinery.SourceFileLoader("normfn", module_path)
        spec = spec_from_loader(os.path.basename(module_path), loader)
        normalize_filename = module_from_spec(spec)
        spec.loader.exec_module(normalize_filename)

        # Create a temporary config file
        with tempfile.TemporaryDirectory() as temp_config_dir:
            if configOverrides:
                self._create_test_config_file(temp_config_dir, **configOverrides)
            else:
                # Default: disable undo log
                self._create_test_config_file(temp_config_dir)
            
            # Set XDG_CONFIG_HOME to use our temp config
            original_env = os.environ.get("XDG_CONFIG_HOME")
            os.environ["XDG_CONFIG_HOME"] = temp_config_dir

            options = [module_path]

            options.extend(inputFiles)
            options.extend(extraParams)

            stream = io.StringIO()
            handler = logging.StreamHandler(stream)
            log = logging.getLogger("normfn")
            log.propagate = False
            log.setLevel(logging.DEBUG)
            log.addHandler(handler)

            try:
                normalize_filename.main(options, handler)
            finally:
                # Restore original XDG_CONFIG_HOME
                if original_env is None:
                    os.environ.pop("XDG_CONFIG_HOME", None)
                else:
                    os.environ["XDG_CONFIG_HOME"] = original_env
                log.removeHandler(handler)
                handler.close()

            error = stream.getvalue()

            return error

    def invokeAsSubprocess(
        self,
        inputFiles,
        extraParams=[],
        feedInput=None,
        cwd=None,
        expectOutput=False,
        useUndoFile=False,
    ):
        if cwd is None:
            cwd = self.workingDir

        # Create temporary directories for config and undo log
        with tempfile.TemporaryDirectory() as temp_config_dir:
            undo_log_file_path = os.path.join(temp_config_dir, "undo.log.sh") if useUndoFile else None
            self._create_test_config_file(temp_config_dir, undo_log_file_path)

            if os.name == "nt":
                options = ["python", NormalizeFilenameTestCase.COMMAND]
            else:
                options = [NormalizeFilenameTestCase.COMMAND]

            options.extend(inputFiles)
            options.extend(extraParams)

            # Set XDG_CONFIG_HOME to point to our temp directory
            env = os.environ.copy()
            env["XDG_CONFIG_HOME"] = temp_config_dir

            if feedInput:
                p = Popen(options, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env)
            else:
                p = Popen(options, stdin=None, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env)

            output, error = p.communicate(feedInput)
            p.wait()

            output = str(output, "utf-8")
            error = str(error, "utf-8")

            if expectOutput:
                self.assertNotEqual("", output)
            else:
                self.assertEqual("", output)

            undo_log_file_contents = []
            if useUndoFile and undo_log_file_path and os.path.exists(undo_log_file_path):
                with open(undo_log_file_path) as undo_log_file_read:
                    undo_log_file_contents = undo_log_file_read.readlines()

            if useUndoFile:
                return (p.returncode, output, error, undo_log_file_contents)
            else:
                return (p.returncode, output, error)

    def executeUndoCommands(self, commands):
        maxReturnCode = 0
        reversed_commands = commands
        reversed_commands.reverse()
        for command in reversed_commands:
            command = command.rstrip("\n\r")
            maxReturnCode = max(maxReturnCode, call(command, shell=True))
        return maxReturnCode

    @contextmanager
    def invokeAsPexpect(
        self,
        inputFiles,
        extraParams=[],
        expectedExitStatus=None,
        expectedOutputRegex=None,
    ):
        # Create temporary directories for config
        with tempfile.TemporaryDirectory() as temp_config_dir:
            self._create_test_config_file(temp_config_dir)

            options = [NormalizeFilenameTestCase.COMMAND]
            options.extend(inputFiles)
            options.extend(extraParams)

            command = " ".join(options)

            stream = io.BytesIO()

            # Set XDG_CONFIG_HOME environment variable for the child process
            env = os.environ.copy()
            env["XDG_CONFIG_HOME"] = temp_config_dir

            child = pexpect.spawn(command, env=env)
            child.logfile_read = stream

            yield child

            child.expect(pexpect.EOF)
            child.close()

            if expectedExitStatus is not None:
                self.assertEqual(expectedExitStatus, child.exitstatus)

            if expectedOutputRegex is not None:
                self.assertRegex(
                    str(child.logfile_read.getvalue(), "utf-8"), expectedOutputRegex
                )

    def touch(self, fname):
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        open(fname, "w").close()

    def remove_dir_write_permissions(self, fname):
        os.chmod(fname, S_IRUSR | S_IXUSR)

    def writeFile(self, fname, contents):
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, "w") as filename:
            filename.write(contents)

    def readFile(self, fname):
        with open(fname) as filename:
            return filename.read()

    def assertPathDoesntExist(self, path):
        self.assertFalse(os.path.exists(path))

    def assertPathExists(self, path):
        self.assertTrue(os.path.exists(path))

    def isRoot(self):
        return os.geteuid() == 0

    def tearDown(self):
        # Give everything write permissions before rmtree'ing.
        for root, dirs, files in os.walk(self.workingDir):
            dirs_and_files = dirs + files
            for dir_and_file in dirs_and_files:
                os.chmod(os.path.join(root, dir_and_file), S_IRUSR | S_IWUSR | S_IXUSR)

        shutil.rmtree(self.workingDir)
