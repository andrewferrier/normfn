from pathlib import Path

import pytest

from normfn.config import Config, load_config, resolve_undo_log_file
from normfn.exceptions import FatalError
from tests.base_test_classes import NormfnTestCase


class TestDirectConfig(NormfnTestCase):
    def test_load_config_absent(self, tmp_path: Path) -> None:
        config = load_config(tmp_path / "nonexistent.toml")
        assert config.max_years_ahead == 5
        assert config.max_years_behind == 30
        assert config.undo_log_file is None

    def test_load_config_empty_file(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("")
        config = load_config(config_file)
        assert config.max_years_ahead == 5
        assert config.max_years_behind == 30
        assert config.undo_log_file is None

    def test_load_config_max_years_ahead(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("max_years_ahead = 10\n")
        config = load_config(config_file)
        assert config.max_years_ahead == 10

    def test_load_config_max_years_behind(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("max_years_behind = 20\n")
        config = load_config(config_file)
        assert config.max_years_behind == 20

    def test_load_config_undo_log_file(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text('undo_log_file = "/some/path/undo.sh"\n')
        config = load_config(config_file)
        assert config.undo_log_file == "/some/path/undo.sh"

    def test_load_config_undo_log_file_empty_string(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text('undo_log_file = ""\n')
        config = load_config(config_file)
        assert config.undo_log_file == ""

    def test_load_config_invalid_toml(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("not valid toml = [[\n")
        with pytest.raises(FatalError, match="Invalid TOML"):
            load_config(config_file)

    def test_load_config_unknown_key(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("unknown_key = 42\n")
        with pytest.raises(FatalError, match="Unknown key"):
            load_config(config_file)

    def test_load_config_max_years_ahead_not_int(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text('max_years_ahead = "not_an_int"\n')
        with pytest.raises(FatalError, match="must be an integer"):
            load_config(config_file)

    def test_load_config_max_years_ahead_zero(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("max_years_ahead = 0\n")
        with pytest.raises(FatalError, match="must be a positive integer"):
            load_config(config_file)

    def test_load_config_max_years_behind_negative(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("max_years_behind = -1\n")
        with pytest.raises(FatalError, match="must be a positive integer"):
            load_config(config_file)

    def test_load_config_undo_log_file_not_string(self, tmp_path: Path) -> None:
        config_file = tmp_path / "normfn.toml"
        config_file.write_text("undo_log_file = 42\n")
        with pytest.raises(FatalError, match="must be a string"):
            load_config(config_file)

    def test_resolve_undo_log_file_none_returns_default(self) -> None:
        config = Config()
        result = resolve_undo_log_file(config)
        assert result is not None
        assert result.name == "normfn-undo.log.sh"

    def test_resolve_undo_log_file_empty_returns_none(self) -> None:
        config = Config(undo_log_file="")
        result = resolve_undo_log_file(config)
        assert result is None

    def test_resolve_undo_log_file_path_returns_path(self) -> None:
        config = Config(undo_log_file="/some/path.sh")
        result = resolve_undo_log_file(config)
        assert result == Path("/some/path.sh")

    def test_config_flag_loads_specified_file(self) -> None:
        custom_config = self.working_dir / "custom.toml"
        custom_undo = self.working_dir / "custom-undo.sh"
        custom_config.write_text(f'undo_log_file = "{custom_undo}"\n')
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        self.invoke_directly([filename], extra_params=["--config", str(custom_config)])
        assert custom_undo.exists()

    def test_initialize_config_creates_file(self) -> None:
        self.config_file.unlink()
        self.invoke_directly([], extra_params=["--initialize-config"])
        assert self.config_file.exists()
        contents = self.config_file.read_text()
        assert "max_years_ahead" in contents
        assert "max_years_behind" in contents
        assert "undo_log_file" in contents

    def test_initialize_config_fails_if_exists(self) -> None:
        with pytest.raises(FatalError, match="already exists"):
            self.invoke_directly([], extra_params=["--initialize-config"])

    def test_initialize_config_creates_parent_dirs(self) -> None:
        new_cfg_path = self.working_dir / "newcfg" / "normfn.toml"
        self.invoke_directly(
            [],
            extra_params=["--initialize-config", "--config", str(new_cfg_path)],
        )
        assert new_cfg_path.exists()
