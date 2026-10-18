from io import SEEK_SET, IOBase
from os import PathLike, fspath

import java.io as _jio  # type: ignore
import java.nio.file as _jnio_file  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JImplementationFor, JOverride

from tuprolog import logger
from tuprolog.jvmutils import customize_derived

__all__ = [
    "BufferedReader",
    "Files",
    "InputStream",
    "InputStreamReader",
    "Paths",
    "Reader",
    "ensure_input_steam",
    "open_file",
]


InputStream = _jio.InputStream

Reader = _jio.Reader

InputStreamReader = _jio.InputStreamReader

BufferedReader = _jio.BufferedReader

Files = _jnio_file.Files

Paths = _jnio_file.Paths


@JImplementationFor("java.io.InputStream")
@customize_derived("close")
class _JvmInputStream:
    def __jclass_init__(cls):
        IOBase.register(cls)

    @JOverride
    def close(self):
        self._closed = True
        self._close()

    @property
    def closed(self):
        if hasattr(self, "_closed"):
            return self._closed
        else:
            return False

    def fileno(self):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def flush(self):
        pass

    def isatty(self):
        return False

    def readable(self):
        return True

    def seekable(self):
        return False

    def writable(self):
        return False

    def _buffer(self):
        if not hasattr(self, "_buffered"):
            self._buffered = BufferedReader(InputStreamReader(self))

    def readline(self, size=-1):
        self._buffer()
        chars = []
        while size is None or size < 0 or len(chars) < size:
            char = self._buffered.read()
            if char < 0:
                break
            if 0xD800 <= char < 0xDC00:  # high surrogate: combine it with the following low one
                self._buffered.mark(1)
                low = self._buffered.read()
                if 0xDC00 <= low < 0xE000:
                    char = 0x10000 + ((char - 0xD800) << 10) + (low - 0xDC00)
                elif low >= 0:
                    self._buffered.reset()
            chars.append(chr(char))
            if char == ord("\n"):
                break
        return "".join(chars)

    def readlines(self, hint=-1):
        lines, total = [], 0
        while line := self.readline():
            lines.append(line)
            total += len(line)
            if hint is not None and 0 < hint <= total:
                break
        return lines

    def __iter__(self):
        return iter(self.readline, "")

    def seek(self, offset: int, whence=SEEK_SET):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def tell(self):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def truncate(self, size=None):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def writelines(self, lines):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")


def open_file(path: str) -> InputStream:
    return Files.newInputStream(Paths.get(path))


def ensure_input_steam(input: str | PathLike | InputStream) -> InputStream:
    if isinstance(input, (str, PathLike)):
        return open_file(fspath(input))
    elif isinstance(input, InputStream):
        return input
    else:
        raise TypeError(f"Invalid type: {type(input)}")


logger.debug("Configure JVM-specific IO extensions")
