from freezegun import freeze_time

import os

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestDirectFrozenTime(NormalizeFilenameTestCase):
    def setUp(self):
        super().setUp()

    def _create_config(self, max_years_ahead=5, max_years_behind=30):
        """Helper method to create a Config object for tests."""
        from importlib.util import module_from_spec, spec_from_loader
        import importlib.machinery
        
        module_path = self.getOriginalScriptPath()
        loader = importlib.machinery.SourceFileLoader("normfn", module_path)
        spec = spec_from_loader(os.path.basename(module_path), loader)
        normalize_filename = module_from_spec(spec)
        spec.loader.exec_module(normalize_filename)
        
        return normalize_filename.Config(
            max_years_ahead=max_years_ahead,
            max_years_behind=max_years_behind,
            undo_log_file=None,
        )

    @freeze_time("2015-02-03 10:11:12")
    def test_basicdateprefix(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--now"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-02-03-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-02-03 10:11:12")
    def test_basicdateprefix_add_time(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--add-time", "--now"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-02-03T10-11-12-blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-02-03 10:10:10")
    def test_ok_behind(self):
        filename = os.path.join(self.workingDir, "blah-1990-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1990-02-03-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-02-03 10:10:10")
    def test_ok_ahead(self):
        filename = os.path.join(self.workingDir, "blah-2019-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2019-02-03-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_behind(self):
        filename = os.path.join(self.workingDir, "blah-1970-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--now"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-05-blah-1970-02-03.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_ahead(self):
        filename = os.path.join(self.workingDir, "blah-2025-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--now"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-05-blah-2025-02-03.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:10:10")
    def test_ok_ahead_adjusted(self):
        testConfig = self._create_config(max_years_ahead=50)
        
        filename = os.path.join(self.workingDir, "blah-2025-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly(
            [filename], extraParams=["--now"], testConfig=testConfig
        )
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2025-02-03-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:10:10")
    def test_ok_behind_adjusted(self):
        testConfig = self._create_config(max_years_behind=50)
        
        filename = os.path.join(self.workingDir, "blah-1970-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly(
            [filename], extraParams=["--now"], testConfig=testConfig
        )
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1970-02-03-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_ahead_adjusted(self):
        testConfig = self._create_config(max_years_ahead=50)
        
        filename = os.path.join(self.workingDir, "blah-2200-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly(
            [filename], extraParams=["--now"], testConfig=testConfig
        )
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-05-blah-2200-02-03.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_behind_adjusted(self):
        testConfig = self._create_config(max_years_behind=50)
        
        filename = os.path.join(self.workingDir, "blah-1930-02-03.txt")
        self.touch(filename)
        error = self.invokeDirectly(
            [filename], extraParams=["--now"], testConfig=testConfig
        )
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-05-blah-1930-02-03.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    @freeze_time("2015-04-05 10:11:12")
    def test_addtime(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--add-time", "--now"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-05T10-11-12-blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)
