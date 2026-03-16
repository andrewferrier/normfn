import logging
import sys
from io import TextIOBase
from typing import cast

from normfn.core import main as _main
from normfn.exceptions import FatalError


def main() -> None:
    logger = logging.getLogger("normfn")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    syserrhandler: logging.StreamHandler[TextIOBase] = logging.StreamHandler(
        stream=cast("TextIOBase", sys.stderr)
    )
    syserrhandler.setLevel(logging.WARNING)
    syserrformatter = logging.Formatter("%(levelname)s: %(message)s")
    syserrhandler.setFormatter(syserrformatter)
    logger.addHandler(syserrhandler)

    try:
        _main(sys.argv, syserrhandler)
    except FatalError as error:
        logger.error(error.value)
        sys.exit(2)


if __name__ == "__main__":
    main()
