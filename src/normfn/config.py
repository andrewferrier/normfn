import dataclasses
import os
import tomllib
import types
import typing
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from normfn.exceptions import FatalError


@dataclass
class Config:
    max_years_ahead: int = 5
    max_years_behind: int = 30
    # None = not configured (use default path); "" = disabled
    undo_log_file: str | None = field(default=None)


_VALID_KEYS = frozenset(f.name for f in dataclasses.fields(Config))

TEMPLATE_CONFIG: Final[str] = """\
# normfn configuration file
# All keys are optional. Uncomment and change the ones you want to override.

# Consider years further ahead from now than this not to be valid years in
# filenames. Must be a positive integer.
# max_years_ahead = 5

# Consider years further behind from now than this not to be valid years in
# filenames. Must be a positive integer.
# max_years_behind = 30

# Path to the shell script used to record undo commands. Set to an empty
# string ("") to disable undo logging entirely.
# Defaults to $XDG_STATE_HOME/normfn-undo.log.sh
#   (i.e. ~/.local/state/normfn-undo.log.sh if XDG_STATE_HOME is not set).
# undo_log_file = ""
"""


def get_default_config_path() -> Path:
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME") or str(
        Path("~").expanduser() / ".config"
    )
    return Path(xdg_config_home) / "normfn" / "normfn.toml"


def resolve_undo_log_file(config: Config) -> Path | None:
    if config.undo_log_file is None:
        home = Path("~").expanduser()
        xdg_state_home = Path(
            os.environ.get("XDG_STATE_HOME") or home / ".local" / "state"
        )
        return xdg_state_home / "normfn-undo.log.sh"
    if config.undo_log_file == "":
        return None
    return Path(config.undo_log_file)


def _validate_and_apply_config(toml_data: dict[str, object], path: Path) -> Config:
    target_config = Config()
    hints = typing.get_type_hints(Config)

    for key, val in toml_data.items():
        hint = hints[key]
        if hint is int:
            if not isinstance(val, int):
                msg = f"Config key '{key}' must be an integer (in {path})"
                raise FatalError(msg)
            if val <= 0:
                msg = f"Config key '{key}' must be a positive integer (in {path})"
                raise FatalError(msg)
            setattr(target_config, key, val)
        elif typing.get_origin(hint) is types.UnionType and str in typing.get_args(
            hint
        ):
            if not isinstance(val, str):
                msg = f"Config key '{key}' must be a string (in {path})"
                raise FatalError(msg)
            setattr(target_config, key, val)

    return target_config


def load_config(config_path: Path | None = None) -> Config:
    path = config_path if config_path is not None else get_default_config_path()

    if not path.exists():
        return Config()

    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        msg = f"Invalid TOML in config file {path}: {e}"
        raise FatalError(msg) from e

    invalid_keys = set(data.keys()) - _VALID_KEYS
    if invalid_keys:
        msg = f"Unknown key(s) in config file {path}: {', '.join(sorted(invalid_keys))}"
        raise FatalError(msg)

    return _validate_and_apply_config(data, path)


def create_template_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE_CONFIG)
