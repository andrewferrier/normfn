import datetime
import os

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestDirectBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super().setUp()

    def test_basicdateprefix(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_nochangeneeded(self):
        filename = os.path.join(self.workingDir, "2015-01-01-blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_path_normalization(self):
        subdirectory = os.path.join(self.workingDir, "subdirectory")
        os.makedirs(subdirectory, exist_ok=True)
        self.invokeDirectly([subdirectory + "/"])
        self.assertPathExists(
            os.path.join(self.workingDir, self.getDatePrefix() + "subdirectory")
        )

    def test_standalone_directory(self):
        subdirectory = os.path.join(self.workingDir, "subdirectory")
        os.makedirs(subdirectory)
        self.invokeDirectly([subdirectory])
        self.assertPathDoesntExist(subdirectory)
        self.assertPathExists(
            os.path.join(self.workingDir, self.getDatePrefix() + "subdirectory")
        )

    def test_directoriesonly_nonrecursive(self):
        subdirectory = os.path.join(self.workingDir, "abc")
        subsubdirectory = os.path.join(self.workingDir, "abc", "def")
        os.makedirs(subsubdirectory, exist_ok=True)
        self.invokeDirectly([subdirectory])
        self.assertPathDoesntExist(subdirectory)
        self.assertPathDoesntExist(subsubdirectory)
        self.assertPathExists(
            os.path.join(self.workingDir, self.getDatePrefix() + "abc")
        )
        self.assertPathExists(
            os.path.join(self.workingDir, self.getDatePrefix() + "abc", "def")
        )

    def test_directoriesonly_recursive(self):
        subdirectory = os.path.join(self.workingDir, "abc")
        subsubdirectory = os.path.join(self.workingDir, "abc", "def")
        os.makedirs(subsubdirectory, exist_ok=True)
        self.invokeDirectly([subdirectory], extraParams=["--recursive"])
        self.assertPathDoesntExist(subdirectory)
        self.assertPathDoesntExist(subsubdirectory)
        self.assertPathExists(
            os.path.join(self.workingDir, self.getDatePrefix() + "abc")
        )
        self.assertPathExists(
            os.path.join(
                self.workingDir,
                self.getDatePrefix() + "abc",
                self.getDatePrefix() + "def",
            )
        )

    def test_directory_withfiles_norecursive(self):
        subWorkingDir = os.path.join(self.workingDir, "subWorkingDir")
        filename = os.path.join(subWorkingDir, "blah_2015_01_01_bling.txt")
        filenameAfter = os.path.join(
            self.workingDir,
            self.getDatePrefix() + "subWorkingDir",
            "blah_2015_01_01_bling.txt",
        )
        self.touch(filename)
        filename2 = os.path.join(subWorkingDir, "xyz-2015-03-04.txt")
        filename2After = os.path.join(
            self.workingDir,
            self.getDatePrefix() + "subWorkingDir",
            "xyz-2015-03-04.txt",
        )
        self.touch(filename2)
        filename3 = os.path.join(subWorkingDir, "subWorkingDir2", "abc-2015-03-04.txt")
        filename3After = os.path.join(
            self.workingDir,
            self.getDatePrefix() + "subWorkingDir",
            "subWorkingDir2",
            "abc-2015-03-04.txt",
        )
        self.touch(filename3)
        error = self.invokeDirectly([subWorkingDir])
        self.assertPathDoesntExist(os.path.join(subWorkingDir))
        self.assertPathExists(
            os.path.join(self.workingDir, self.getDatePrefix() + "subWorkingDir")
        )
        self.assertPathDoesntExist(os.path.join(filename))
        self.assertPathDoesntExist(os.path.join(filename2))
        self.assertPathDoesntExist(os.path.join(filename3))
        self.assertPathExists(os.path.join(filenameAfter))
        self.assertPathExists(os.path.join(filename2After))
        self.assertPathExists(os.path.join(filename3After))
        self.assertEqual(
            2,
            self.directoryFileCount(
                os.path.join(self.workingDir, self.getDatePrefix() + "subWorkingDir")
            ),
        )
        self.assertEqual(
            1,
            self.directoryFileCount(
                os.path.join(
                    self.workingDir,
                    self.getDatePrefix() + "subWorkingDir",
                    "subWorkingDir2",
                )
            ),
        )
        self.assertEqual("", error)

    def test_directory_withfiles_recursive(self):
        subWorkingDir = os.path.join(self.workingDir, "subWorkingDir")
        filename = os.path.join(subWorkingDir, "blah_2015_01_01_bling.txt")
        self.touch(filename)
        filename2 = os.path.join(subWorkingDir, "xyz-2015-03-04.txt")
        self.touch(filename2)
        filename3 = os.path.join(subWorkingDir, "subWorkingDir2", "abc-2015-03-04.txt")
        self.touch(filename3)
        error = self.invokeDirectly([subWorkingDir], extraParams=["--recursive"])
        newsubWorkingDir = os.path.join(
            self.workingDir, self.getDatePrefix() + "subWorkingDir"
        )
        self.assertPathDoesntExist(filename)
        self.assertPathExists(
            os.path.join(newsubWorkingDir, "2015-01-01-blah_bling.txt")
        )
        self.assertPathDoesntExist(filename2)
        self.assertPathExists(os.path.join(newsubWorkingDir, "2015-03-04-xyz.txt"))
        self.assertPathDoesntExist(filename3)
        self.assertPathExists(
            os.path.join(
                newsubWorkingDir,
                self.getDatePrefix() + "subWorkingDir2",
                "2015-03-04-abc.txt",
            )
        )
        self.assertEqual(2, self.directoryFileCount(newsubWorkingDir))
        self.assertEqual(
            1,
            self.directoryFileCount(
                os.path.join(newsubWorkingDir, self.getDatePrefix() + "subWorkingDir2")
            ),
        )
        self.assertEqual("", error)

    def test_ridiculousdate1(self):
        filename = os.path.join(self.workingDir, "blah-2100-01-01.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, self.getDatePrefix() + "blah-2100-01-01.txt"
                )
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ridiculousdate2(self):
        filename = os.path.join(self.workingDir, "blah-1899-01-01.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, self.getDatePrefix() + "blah-1899-01-01.txt"
                )
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_invaliddate1(self):
        filename = os.path.join(self.workingDir, "blah-1998-20-01.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, self.getDatePrefix() + "blah-1998-20-01.txt"
                )
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_invaliddate2(self):
        filename = os.path.join(self.workingDir, "blah-1998-01-41.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1998-01-blah-41.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_invaliddate3(self):
        filename = os.path.join(self.workingDir, "blah-1998-01-35.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1998-01-blah-35.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_invaliddate4(self):
        filename = os.path.join(self.workingDir, "blah-1998-13-35.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, self.getDatePrefix() + "blah-1998-13-35.txt"
                )
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_basic_compressed_datemove(self):
        filename = os.path.join(self.workingDir, "blah-20150101.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-01-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_basic_invalid_compressed_nodatemove(self):
        filename = os.path.join(self.workingDir, "blah-20153101.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, self.getDatePrefix() + "blah-20153101.txt"
                )
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_basic_compressed_withspace(self):
        filename = os.path.join(self.workingDir, "blah 20150101.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-01-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_single_digit_day(self):
        filename = os.path.join(self.workingDir, "blah-2015-01-2.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_single_digit_month(self):
        filename = os.path.join(self.workingDir, "blah-2015-3-02.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-03-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_two_single_digits(self):
        filename = os.path.join(self.workingDir, "blah-2015-3-2.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-03-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_two_single_digits_extra(self):
        filename = os.path.join(self.workingDir, "blah-2015-3-2-xyz.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-03-02-blah-xyz.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_full_month_name(self):
        filename = os.path.join(self.workingDir, "Blah 25 January 2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-25-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_full_month_name2(self):
        filename = os.path.join(self.workingDir, "Blah 25 March 2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-03-25-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_abbr_month_name(self):
        filename = os.path.join(self.workingDir, "Blah 25 Jan 2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-25-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_month_name_year_reversed(self):
        filename = os.path.join(self.workingDir, "Blah May 2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-05-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_day_month_name_year(self):
        filename = os.path.join(
            self.workingDir, "Blah46_002004_XYZ_20_November_2015.txt"
        )
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-11-20-Blah46_002004_XYZ.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_abbr_month_insensitive_name(self):
        filename = os.path.join(self.workingDir, "Blah 25 jan 2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-25-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_abbr_month_insensitive_hyphen_name(self):
        filename = os.path.join(self.workingDir, "Blah_25-feb-2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-02-25-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_abbr_month_underscore_name(self):
        filename = os.path.join(self.workingDir, "Blah_18-jun-25.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2025-06-18-Blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ensure_common_date_separator_used(self):
        filename = os.path.join(self.workingDir, "T 1234 2023-11-22.pdf")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2023-11-22-T 1234.pdf"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ensure_common_time_separator_used(self):
        filename = os.path.join(self.workingDir, "ABC 2023-11-05T12-13_08.pdf")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2023-11-05T12-13-ABC _08.pdf")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_earliest(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
            ),
        )
        error = self.invokeDirectly([filename], extraParams=["--earliest"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1980-01-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_oldest(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
            ),
        )
        error = self.invokeDirectly([filename], extraParams=["--oldest"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1980-01-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_earliest_default(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
            ),
        )
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "1980-01-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_latest(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
            ),
        )
        error = self.invokeDirectly([filename], extraParams=["--latest"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_newest(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
            ),
        )
        error = self.invokeDirectly([filename], extraParams=["--newest"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_now(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
            ),
        )
        error = self.invokeDirectly([filename], extraParams=["--now"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_screenshot(self):
        filename = os.path.join(
            self.workingDir, "Screen Shot 2015-04-21 at 13.50.45.png"
        )
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-21T13-50-45-Screen Shot.png")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_photo(self):
        filename = os.path.join(self.workingDir, "Photo 03-04-2015 12 34 56.png")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-03T12-34-56-Photo.png")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_photo_dropbox(self):
        filename = os.path.join(self.workingDir, "Photo 03-04-2015, 12 34 56.png")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-03T12-34-56-Photo.png")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_video(self):
        filename = os.path.join(self.workingDir, "Video 03-04-2015 12 34 56.mov")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-03T12-34-56-Video.mov")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_IMG(self):
        filename = os.path.join(self.workingDir, "IMG_20150506_123456.png")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-05-06T12-34-56-IMG.png"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_VID(self):
        filename = os.path.join(self.workingDir, "VID_20150506_123456.mpg")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-05-06T12-34-56-VID.mpg"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_photo_format2(self):
        filename = os.path.join(self.workingDir, "Photo-2015-04-03-12-34-56.png")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-03T12-34-56-Photo.png")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_photo_format2_invalidhour(self):
        filename = os.path.join(self.workingDir, "Photo-2015-04-03-99-34-56.png")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2015-04-03-Photo-99-34-56.png")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_underscore(self):
        filename = os.path.join(self.workingDir, "2008_11_08_15_35_02.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2008-11-08T15-35-02.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_spaces(self):
        filename = os.path.join(self.workingDir, "2008 11 08 15 35 02 xyz.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2008-11-08T15-35-02 xyz.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_dots(self):
        filename = os.path.join(self.workingDir, "blah 02.04.2015.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-04-02-blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_exclude_startswith_period(self):
        filename = os.path.join(self.workingDir, ".blah-2015_01_01.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_exclude_startswith_period_all(self):
        filename = os.path.join(self.workingDir, ".blah-2015_01_01.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--all"])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-01-01-.blah.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_exclude_icon(self):
        if os.name == "nt":
            self.skipTest("Not valid on Windows")
        else:
            filename = os.path.join(self.workingDir, "Icon\r")
            self.touch(filename)
            error = self.invokeDirectly([filename])
            self.assertTrue(os.path.exists(filename))
            self.assertFalse(
                os.path.exists(
                    os.path.join(self.workingDir, self.getDatePrefix() + "Icon")
                )
            )
            self.assertEqual(1, self.directoryFileCount(self.workingDir))
            self.assertEqual("", error)

    def test_exclude_lock(self):
        filename = os.path.join(self.workingDir, "blah.lck")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.lck")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_exclude_lock_nomatch(self):
        filename = os.path.join(self.workingDir, "blah.lck.blah")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.lck.blah")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_exclude_git_file(self):
        filename = os.path.join(self.workingDir, ".git", "bling", "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.workingDir, ".git", "bling", self.getDatePrefix() + "blah.txt"
                )
            )
        )
        self.assertEqual(
            1, self.directoryFileCount(os.path.join(self.workingDir, ".git", "bling"))
        )
        self.assertEqual("", error)

    def test_exclude_nongit_file(self):
        filename = os.path.join(self.workingDir, "xyz", "bling", "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, "xyz", "bling", self.getDatePrefix() + "blah.txt"
                )
            )
        )
        self.assertEqual(
            1, self.directoryFileCount(os.path.join(self.workingDir, "xyz", "bling"))
        )
        self.assertEqual("", error)

    def test_exclude_subgit_file(self):
        filename = os.path.join(self.workingDir, "xyz", ".git", "bling", "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.workingDir,
                    "xyz",
                    ".git",
                    "bling",
                    self.getDatePrefix() + "blah.txt",
                )
            )
        )
        self.assertEqual(
            1,
            self.directoryFileCount(
                os.path.join(self.workingDir, "xyz", ".git", "bling")
            ),
        )
        self.assertEqual("", error)

    def test_standardeuropeandate(self):
        filename = os.path.join(self.workingDir, "European XYZ 16052014.pptx")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2014-05-16-European XYZ.pptx")
            )
        )
        self.assertEqual(1, self.directoryFileCount(os.path.join(self.workingDir)))
        self.assertEqual("", error)

    def test_basicdateprefix_dryrun(self):
        filename = os.path.join(self.workingDir, "blah.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=["--dry-run"])
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "blah.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertRegex(error, "(?i)not moving.*dry run")

    def test_realworld_failure1_now_fixed(self):
        filename = os.path.join(self.workingDir, "Overview 3.0 May 2016.pptx")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2016-05-Overview 3.0.pptx"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_zero_month(self):
        filename = os.path.join(self.workingDir, "Overview 5-0-2016.pptx")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workingDir, self.getDatePrefix() + "Overview 5-0-2016.pptx"
                )
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_21st(self):
        filename = os.path.join(self.workingDir, "foobar 21st January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-21-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_2nd(self):
        filename = os.path.join(self.workingDir, "foobar 2nd January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-02-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_3rd(self):
        filename = os.path.join(self.workingDir, "foobar 3rd January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-03-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_22nd(self):
        filename = os.path.join(self.workingDir, "foobar 22nd January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-22-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_invalid_22st(self):
        """Test that invalid ordinal suffix 22st is left intact"""
        filename = os.path.join(self.workingDir, "foobar 22st January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        # File should be renamed to dated version since no valid date pattern was found
        # It falls back to using file timestamp
        self.assertFalse(os.path.exists(filename))
        # Should get a date prefix from file timestamp, with "22st" preserved
        renamed_files = [
            f
            for f in os.listdir(self.workingDir)
            if "foobar 22st January 2026.txt" in f
        ]
        self.assertEqual(1, len(renamed_files))
        self.assertTrue("22st" in renamed_files[0])
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_non_ordinal_still_works(self):
        """Ensure non-ordinal dates still work"""
        filename = os.path.join(self.workingDir, "foobar 21 January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-21-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_11th(self):
        """Test special case 11th (not 11st)"""
        filename = os.path.join(self.workingDir, "foobar 11th January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-11-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_12th(self):
        """Test special case 12th (not 12nd)"""
        filename = os.path.join(self.workingDir, "foobar 12th January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-12-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_13th(self):
        """Test special case 13th (not 13rd)"""
        filename = os.path.join(self.workingDir, "foobar 13th January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-13-foobar.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_not_in_date_context_21stone(self):
        """Test that '21stone' is preserved when not part of a date"""
        filename = os.path.join(self.workingDir, "21stone thing.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        # Should be renamed with date prefix from file timestamp, keeping "21stone"
        renamed_files = [
            f for f in os.listdir(self.workingDir) if "21stone thing.txt" in f
        ]
        self.assertEqual(1, len(renamed_files))
        self.assertTrue("21stone" in renamed_files[0])
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_not_in_date_context_13th_listing(self):
        """Test that '13th listing' is preserved when not part of a date"""
        filename = os.path.join(self.workingDir, "13th listing.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        # Should be renamed with date prefix from file timestamp, keeping "13th listing"
        renamed_files = [
            f for f in os.listdir(self.workingDir) if "13th listing.txt" in f
        ]
        self.assertEqual(1, len(renamed_files))
        self.assertTrue("13th listing" in renamed_files[0])
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_mixed_context(self):
        """Test ordinal in non-date context with actual date in filename"""
        filename = os.path.join(
            self.workingDir, "13th listing - 22nd december 2025.txt"
        )
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        # Should parse "22nd december 2025" and keep "13th listing"
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, "2025-12-22-13th listing -.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_with_suffix_content(self):
        """Test ordinal date at start with suffix content after dash"""
        filename = os.path.join(self.workingDir, "21st January 2026 - foo.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        # Should parse the date and preserve the suffix after the dash
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-21 - foo.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_ordinal_date_with_prefix(self):
        """Test ordinal date with prefix content before the date"""
        filename = os.path.join(self.workingDir, "abc 21st January 2026.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        # Should parse the date and move prefix to after the date
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2026-01-21-abc.txt"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)
