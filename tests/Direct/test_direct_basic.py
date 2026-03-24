import datetime
import os

from tests.base_test_classes import NormalizeFilenameTestCase


class TestDirectBasic(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_basicdateprefix(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_nochangeneeded(self) -> None:
        filename = self.working_dir / "2015-01-01-blah.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertTrue(filename.exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_path_normalization(self) -> None:
        subdirectory = self.working_dir / "subdirectory"
        subdirectory.mkdir(exist_ok=True)
        self.invoke_directly([str(subdirectory) + "/"])
        self.assert_path_exists(
            self.working_dir / (self.get_date_prefix() + "subdirectory")
        )

    def test_standalone_directory(self) -> None:
        subdirectory = self.working_dir / "subdirectory"
        subdirectory.mkdir()
        self.invoke_directly([str(subdirectory)])
        self.assert_path_doesnt_exist(subdirectory)
        self.assert_path_exists(
            self.working_dir / (self.get_date_prefix() + "subdirectory")
        )

    def test_directoriesonly_nonrecursive(self) -> None:
        subdirectory = self.working_dir / "abc"
        subsubdirectory = subdirectory / "def"
        subsubdirectory.mkdir(parents=True, exist_ok=True)
        self.invoke_directly([str(subdirectory)])
        self.assert_path_doesnt_exist(subdirectory)
        self.assert_path_doesnt_exist(subsubdirectory)
        self.assert_path_exists(self.working_dir / (self.get_date_prefix() + "abc"))
        self.assert_path_exists(
            self.working_dir / (self.get_date_prefix() + "abc") / "def"
        )

    def test_directoriesonly_recursive(self) -> None:
        subdirectory = self.working_dir / "abc"
        subsubdirectory = subdirectory / "def"
        subsubdirectory.mkdir(parents=True, exist_ok=True)
        self.invoke_directly([str(subdirectory)], extra_params=["--recursive"])
        self.assert_path_doesnt_exist(subdirectory)
        self.assert_path_doesnt_exist(subsubdirectory)
        self.assert_path_exists(self.working_dir / (self.get_date_prefix() + "abc"))
        self.assert_path_exists(
            self.working_dir
            / (self.get_date_prefix() + "abc")
            / (self.get_date_prefix() + "def")
        )

    def test_directory_withfiles_norecursive(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / "blah_2015_01_01_bling.txt"
        filename_after = (
            self.working_dir
            / (self.get_date_prefix() + "subWorkingDir")
            / "blah_2015_01_01_bling.txt"
        )
        self.touch(filename)
        filename2 = sub_working_dir / "xyz-2015-03-04.txt"
        filename_2_after = (
            self.working_dir
            / (self.get_date_prefix() + "subWorkingDir")
            / "xyz-2015-03-04.txt"
        )
        self.touch(filename2)
        filename3 = sub_working_dir / "subWorkingDir2" / "abc-2015-03-04.txt"
        filename_3_after = (
            self.working_dir
            / (self.get_date_prefix() + "subWorkingDir")
            / "subWorkingDir2"
            / "abc-2015-03-04.txt"
        )
        self.touch(filename3)
        error = self.invoke_directly([str(sub_working_dir)])
        self.assert_path_doesnt_exist(sub_working_dir)
        self.assert_path_exists(
            self.working_dir / (self.get_date_prefix() + "subWorkingDir")
        )
        self.assert_path_doesnt_exist(filename)
        self.assert_path_doesnt_exist(filename2)
        self.assert_path_doesnt_exist(filename3)
        self.assert_path_exists(filename_after)
        self.assert_path_exists(filename_2_after)
        self.assert_path_exists(filename_3_after)
        self.assertEqual(
            2,
            self.directory_file_count(
                self.working_dir / (self.get_date_prefix() + "subWorkingDir")
            ),
        )
        self.assertEqual(
            1,
            self.directory_file_count(
                self.working_dir
                / (self.get_date_prefix() + "subWorkingDir")
                / "subWorkingDir2"
            ),
        )
        self.assertEqual("", error)

    def test_directory_withfiles_recursive(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / "blah_2015_01_01_bling.txt"
        self.touch(filename)
        filename2 = sub_working_dir / "xyz-2015-03-04.txt"
        self.touch(filename2)
        filename3 = sub_working_dir / "subWorkingDir2" / "abc-2015-03-04.txt"
        self.touch(filename3)
        error = self.invoke_directly(
            [str(sub_working_dir)], extra_params=["--recursive"]
        )
        newsub_working_dir = self.working_dir / (
            self.get_date_prefix() + "subWorkingDir"
        )
        self.assert_path_doesnt_exist(filename)
        self.assert_path_exists(newsub_working_dir / "2015-01-01-blah_bling.txt")
        self.assert_path_doesnt_exist(filename2)
        self.assert_path_exists(newsub_working_dir / "2015-03-04-xyz.txt")
        self.assert_path_doesnt_exist(filename3)
        self.assert_path_exists(
            newsub_working_dir
            / (self.get_date_prefix() + "subWorkingDir2")
            / "2015-03-04-abc.txt"
        )
        self.assertEqual(2, self.directory_file_count(newsub_working_dir))
        self.assertEqual(
            1,
            self.directory_file_count(
                newsub_working_dir / (self.get_date_prefix() + "subWorkingDir2")
            ),
        )
        self.assertEqual("", error)

    def test_ridiculousdate1(self) -> None:
        filename = self.working_dir / "blah-2100-01-01.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (
                self.working_dir / (self.get_date_prefix() + "blah-2100-01-01.txt")
            ).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ridiculousdate2(self) -> None:
        filename = self.working_dir / "blah-1899-01-01.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (
                self.working_dir / (self.get_date_prefix() + "blah-1899-01-01.txt")
            ).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_invaliddate1(self) -> None:
        filename = self.working_dir / "blah-1998-20-01.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (
                self.working_dir / (self.get_date_prefix() + "blah-1998-20-01.txt")
            ).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_invaliddate2(self) -> None:
        filename = self.working_dir / "blah-1998-01-41.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "1998-01-blah-41.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_invaliddate3(self) -> None:
        filename = self.working_dir / "blah-1998-01-35.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "1998-01-blah-35.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_invaliddate4(self) -> None:
        filename = self.working_dir / "blah-1998-13-35.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (
                self.working_dir / (self.get_date_prefix() + "blah-1998-13-35.txt")
            ).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_basic_compressed_datemove(self) -> None:
        filename = self.working_dir / "blah-20150101.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-01-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_basic_invalid_compressed_nodatemove(self) -> None:
        filename = self.working_dir / "blah-20153101.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah-20153101.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_basic_compressed_withspace(self) -> None:
        filename = self.working_dir / "blah 20150101.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-01-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_single_digit_day(self) -> None:
        filename = self.working_dir / "blah-2015-01-2.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_single_digit_month(self) -> None:
        filename = self.working_dir / "blah-2015-3-02.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-03-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_two_single_digits(self) -> None:
        filename = self.working_dir / "blah-2015-3-2.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-03-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_two_single_digits_extra(self) -> None:
        filename = self.working_dir / "blah-2015-3-2-xyz.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-03-02-blah-xyz.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_full_month_name(self) -> None:
        filename = self.working_dir / "Blah 25 January 2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-25-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_full_month_name2(self) -> None:
        filename = self.working_dir / "Blah 25 March 2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-03-25-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_abbr_month_name(self) -> None:
        filename = self.working_dir / "Blah 25 Jan 2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-25-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_month_name_year_reversed(self) -> None:
        filename = self.working_dir / "Blah May 2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-05-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_day_month_name_year(self) -> None:
        filename = self.working_dir / "Blah46_002004_XYZ_20_November_2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / "2015-11-20-Blah46_002004_XYZ.txt").exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_abbr_month_insensitive_name(self) -> None:
        filename = self.working_dir / "Blah 25 jan 2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-25-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_abbr_month_insensitive_hyphen_name(self) -> None:
        filename = self.working_dir / "Blah_25-feb-2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-02-25-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_abbr_month_underscore_name(self) -> None:
        filename = self.working_dir / "Blah_18-jun-25.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2025-06-18-Blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ensure_common_date_separator_used(self) -> None:
        filename = self.working_dir / "T 1234 2023-11-22.pdf"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2023-11-22-T 1234.pdf").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ensure_common_time_separator_used(self) -> None:
        filename = self.working_dir / "ABC 2023-11-05T12-13_08.pdf"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2023-11-05T12-13-ABC _08.pdf").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_earliest(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
            ),
        )
        error = self.invoke_directly([str(filename)], extra_params=["--earliest"])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "1980-01-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_oldest(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
            ),
        )
        error = self.invoke_directly([str(filename)], extra_params=["--oldest"])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "1980-01-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_earliest_default(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
            ),
        )
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "1980-01-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_latest(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
            ),
        )
        error = self.invoke_directly([str(filename)], extra_params=["--latest"])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_newest(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
            ),
        )
        error = self.invoke_directly([str(filename)], extra_params=["--newest"])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_now(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        os.utime(
            filename,
            (
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
                datetime.datetime(1980, 1, 2, 3, 4, 5, tzinfo=datetime.UTC).timestamp(),
            ),
        )
        error = self.invoke_directly([str(filename)], extra_params=["--now"])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_screenshot(self) -> None:
        filename = self.working_dir / "Screen Shot 2015-04-21 at 13.50.45.png"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / "2015-04-21T13-50-45-Screen Shot.png").exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_photo(self) -> None:
        filename = self.working_dir / "Photo 03-04-2015 12 34 56.png"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-04-03T12-34-56-Photo.png").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_photo_dropbox(self) -> None:
        filename = self.working_dir / "Photo 03-04-2015, 12 34 56.png"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-04-03T12-34-56-Photo.png").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_video(self) -> None:
        filename = self.working_dir / "Video 03-04-2015 12 34 56.mov"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-04-03T12-34-56-Video.mov").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_IMG(self) -> None:  # noqa: N802
        filename = self.working_dir / "IMG_20150506_123456.png"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-05-06T12-34-56-IMG.png").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_VID(self) -> None:  # noqa: N802
        filename = self.working_dir / "VID_20150506_123456.mpg"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-05-06T12-34-56-VID.mpg").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_photo_format2(self) -> None:
        filename = self.working_dir / "Photo-2015-04-03-12-34-56.png"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-04-03T12-34-56-Photo.png").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_photo_format2_invalidhour(self) -> None:
        filename = self.working_dir / "Photo-2015-04-03-99-34-56.png"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-04-03-Photo-99-34-56.png").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_underscore(self) -> None:
        filename = self.working_dir / "2008_11_08_15_35_02.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2008-11-08T15-35-02.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_spaces(self) -> None:
        filename = self.working_dir / "2008 11 08 15 35 02 xyz.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2008-11-08T15-35-02 xyz.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_dots(self) -> None:
        filename = self.working_dir / "blah 02.04.2015.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-04-02-blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_exclude_startswith_period(self) -> None:
        filename = self.working_dir / ".blah-2015_01_01.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertTrue(filename.exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_exclude_startswith_period_all(self) -> None:
        filename = self.working_dir / ".blah-2015_01_01.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)], extra_params=["--all"])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2015-01-01-.blah.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_exclude_icon(self) -> None:
        if os.name == "nt":
            self.skipTest("Not valid on Windows")
        else:
            filename = self.working_dir / "Icon\r"
            self.touch(filename)
            error = self.invoke_directly([str(filename)])
            self.assertTrue(filename.exists())
            self.assertFalse(
                (self.working_dir / (self.get_date_prefix() + "Icon")).exists()
            )
            self.assertEqual(1, self.directory_file_count(self.working_dir))
            self.assertEqual("", error)

    def test_exclude_lock(self) -> None:
        filename = self.working_dir / "blah.lck"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertTrue(filename.exists())
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah.lck")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_exclude_lock_nomatch(self) -> None:
        filename = self.working_dir / "blah.lck.blah"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.lck.blah")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_exclude_git_file(self) -> None:
        filename = self.working_dir / ".git" / "bling" / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertTrue(filename.exists())
        self.assertFalse(
            (
                self.working_dir
                / ".git"
                / "bling"
                / (self.get_date_prefix() + "blah.txt")
            ).exists()
        )
        self.assertEqual(
            1, self.directory_file_count(self.working_dir / ".git" / "bling")
        )
        self.assertEqual("", error)

    def test_exclude_nongit_file(self) -> None:
        filename = self.working_dir / "xyz" / "bling" / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (
                self.working_dir
                / "xyz"
                / "bling"
                / (self.get_date_prefix() + "blah.txt")
            ).exists()
        )
        self.assertEqual(
            1, self.directory_file_count(self.working_dir / "xyz" / "bling")
        )
        self.assertEqual("", error)

    def test_exclude_subgit_file(self) -> None:
        filename = self.working_dir / "xyz" / ".git" / "bling" / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertTrue(filename.exists())
        self.assertFalse(
            (
                self.working_dir
                / "xyz"
                / ".git"
                / "bling"
                / (self.get_date_prefix() + "blah.txt")
            ).exists()
        )
        self.assertEqual(
            1,
            self.directory_file_count(self.working_dir / "xyz" / ".git" / "bling"),
        )
        self.assertEqual("", error)

    def test_standardeuropeandate(self) -> None:
        filename = self.working_dir / "European XYZ 16052014.pptx"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2014-05-16-European XYZ.pptx").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_basicdateprefix_dryrun(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)], extra_params=["--dry-run"])
        self.assertTrue(filename.exists())
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertRegex(error, "(?i)not moving.*dry run")

    def test_realworld_failure1_now_fixed(self) -> None:
        filename = self.working_dir / "Overview 3.0 May 2016.pptx"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2016-05-Overview 3.0.pptx").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_zero_month(self) -> None:
        filename = self.working_dir / "Overview 5-0-2016.pptx"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue(
            (
                self.working_dir / (self.get_date_prefix() + "Overview 5-0-2016.pptx")
            ).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_21st(self) -> None:
        filename = self.working_dir / "foobar 21st January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-21-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_2nd(self) -> None:
        filename = self.working_dir / "foobar 2nd January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-02-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_3rd(self) -> None:
        filename = self.working_dir / "foobar 3rd January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-03-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_22nd(self) -> None:
        filename = self.working_dir / "foobar 22nd January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-22-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_invalid_22st(self) -> None:
        filename = self.working_dir / "foobar 22st January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        # File should be renamed to dated version since no valid date pattern was found
        # It falls back to using file timestamp
        self.assertFalse(filename.exists())
        # Should get a date prefix from file timestamp, with "22st" preserved
        renamed_files = [
            f
            for f in self.working_dir.iterdir()
            if "foobar 22st January 2026.txt" in str(f)
        ]
        self.assertEqual(1, len(renamed_files))
        self.assertTrue("22st" in str(renamed_files[0]))
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_11th(self) -> None:
        filename = self.working_dir / "foobar 11th January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-11-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_12th(self) -> None:
        filename = self.working_dir / "foobar 12th January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-12-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_13th(self) -> None:
        filename = self.working_dir / "foobar 13th January 2026.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        self.assertTrue((self.working_dir / "2026-01-13-foobar.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_not_in_date_context_21stone(self) -> None:
        filename = self.working_dir / "21stone thing.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        # Should be renamed with date prefix from file timestamp, keeping "21stone"
        renamed_files = [
            f for f in self.working_dir.iterdir() if "21stone thing.txt" in str(f)
        ]
        self.assertEqual(1, len(renamed_files))
        self.assertTrue("21stone" in str(renamed_files[0]))
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_not_in_date_context_13th_listing(self) -> None:
        filename = self.working_dir / "13th listing.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        # Should be renamed with date prefix from file timestamp, keeping "13th listing"
        renamed_files = [
            f for f in self.working_dir.iterdir() if "13th listing.txt" in str(f)
        ]
        self.assertEqual(1, len(renamed_files))
        self.assertTrue("13th listing" in str(renamed_files[0]))
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_mixed_context(self) -> None:
        filename = self.working_dir / "13th listing - 22nd december 2025.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        # Should parse "22nd december 2025" and keep "13th listing"
        self.assertTrue((self.working_dir / "2025-12-22-13th listing -.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_ordinal_date_with_suffix_content(self) -> None:
        filename = self.working_dir / "21st January 2026 - foo.txt"
        self.touch(filename)
        error = self.invoke_directly([str(filename)])
        self.assertFalse(filename.exists())
        # Should parse the date and preserve the suffix after the dash
        self.assertTrue((self.working_dir / "2026-01-21 - foo.txt").exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)
