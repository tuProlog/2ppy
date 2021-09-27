from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
from java.io import InputStream, Reader, InputStreamReader, BufferedReader
# noinspection PyUnresolvedReferences
from java.nio.file import Files, Paths
from io import IOBase, SEEK_SET
from typing import Union


@jpype.JImplementationFor("java.io.InputStream")
class _JvmInputStream:
    def __jclass_init__(cls):
        IOBase.register(cls)

    @jpype.JOverride
    def close(self):
        self._closed = True
        self.close_()

    @property
    def closed(self):
        if hasattr(self, '_closed'):
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
        if not hasattr(self, '_buffered'):
            self._buffered = BufferedReader(InputStreamReader(self))

    def readline(self, size=-1):
        self._buffer()
        self._buffered.readLine()

    def readlines(self, hint=-1):
        self._buffer()
        stream = self._buffered.read.lines()
        if hint >= 0:
            stream = stream.limit(hint)
        return list(stream)

    def seek(self, offset: int, whence=SEEK_SET):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def tell(self):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def truncate(self, size=None):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def writelines(self):
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")


def open_file(path: str) -> InputStream:
    return Files.newInputStream(Paths.get(path))


def ensure_input_steam(input: Union[str, InputStream]) -> InputStream:
    if isinstance(input, str):
        return open_file(input)
    elif isinstance(input, InputStream):
        return input
    else:
        raise TypeError("Invalid type: " + type(input))


logger.debug("Configure JVM-specific IO extensions")
