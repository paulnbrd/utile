import sys
import utile.utils
import os


class DepsLoader:
    def __init__(self) -> None:
        sys.path.append(
            utile.utils.deps_dir
        )
