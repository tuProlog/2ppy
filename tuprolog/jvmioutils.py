import codecs
from io import SEEK_SET, BufferedIOBase, IOBase, RawIOBase, TextIOBase
from os import PathLike, fspath

import java.io as _jio  # type: ignore
import java.nio.channels as _jnio_channels  # type: ignore
import java.nio.file as _jnio_file  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JArray, JByte, JConversion, JImplementationFor, JImplements, JOverride

from tuprolog import logger
from tuprolog.jvmutils import customize_derived

__all__ = [
    "BufferedReader",
    "Channels",
    "Files",
    "InputStream",
    "InputStreamReader",
    "OutputStream",
    "Paths",
    "PythonByteChannel",
    "Reader",
    "Writer",
    "ensure_input_steam",
    "ensure_input_stream",
    "ensure_output_stream",
    "ensure_reader",
    "ensure_writer",
    "open_file",
]


InputStream = _jio.InputStream

Reader = _jio.Reader

InputStreamReader = _jio.InputStreamReader

BufferedReader = _jio.BufferedReader

Files = _jnio_file.Files

Paths = _jnio_file.Paths

OutputStream = _jio.OutputStream

Writer = _jio.Writer

Channels = _jnio_channels.Channels

_ENCODING = "UTF-8"

_BINARY_STREAMS = (RawIOBase, BufferedIOBase)


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


@JImplements(
    "java.nio.channels.ReadableByteChannel", "java.nio.channels.WritableByteChannel", deferred=True
)
class PythonByteChannel:
    """A JVM byte channel reading from, or writing to, a Python stream.

    Text streams are encoded and decoded as UTF-8, binary ones are passed through.
    Closing the channel leaves the stream open, as the stream belongs to its Python owner.
    """

    def __init__(self, stream: IOBase):
        self._stream = stream
        self._text = isinstance(stream, TextIOBase)
        self._pending = b""
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._open = True

    def _next_chunk(self, size: int) -> bytes | None:
        if self._text:  # lines keep interactive streams responsive
            return self._stream.readline().encode("utf-8")  # type: ignore[attr-defined]
        read = getattr(self._stream, "read1", self._stream.read)  # type: ignore[attr-defined]
        return read(size)

    @JOverride
    def read(self, buffer):
        size = buffer.remaining()
        if size == 0:
            return 0
        if not self._pending:
            chunk = self._next_chunk(size)
            if chunk is None:  # non-blocking stream with no data available
                return 0
            if not chunk:
                return -1
            self._pending = chunk
        data, self._pending = self._pending[:size], self._pending[size:]
        buffer.put(JArray(JByte)(data))
        return len(data)

    @JOverride
    def write(self, buffer):
        size = buffer.remaining()
        data = JByte[size]
        buffer.get(data)
        payload = memoryview(data).tobytes()
        if self._text:
            self._stream.write(self._decoder.decode(payload))  # type: ignore[attr-defined]
        else:
            self._stream.write(payload)  # type: ignore[attr-defined]
        return size

    @JOverride
    def isOpen(self):
        return self._open

    @JOverride
    def close(self):
        self._open = False


def open_file(path: str) -> InputStream:
    return Files.newInputStream(Paths.get(path))


def _invalid(value) -> TypeError:
    return TypeError(f"Invalid type: {type(value)}")


def ensure_input_stream(input: str | PathLike | IOBase | InputStream) -> InputStream:
    """Turns a path, a Python stream, or a JVM input stream into a JVM input stream."""
    if isinstance(input, (str, PathLike)):
        return open_file(fspath(input))
    elif isinstance(input, InputStream):
        return input
    elif isinstance(input, IOBase):
        return Channels.newInputStream(PythonByteChannel(input))
    else:
        raise _invalid(input)


ensure_input_steam = ensure_input_stream  # backward-compatible misspelling


def ensure_reader(input: str | PathLike | IOBase | InputStream | Reader) -> Reader:
    """Turns a path, a Python stream, or a JVM input stream or reader into a JVM reader."""
    if isinstance(input, Reader):
        return input
    elif isinstance(input, IOBase) and not isinstance(input, InputStream):
        return Channels.newReader(PythonByteChannel(input), _ENCODING)
    else:
        return InputStreamReader(ensure_input_stream(input), _ENCODING)


def ensure_output_stream(output: IOBase | OutputStream) -> OutputStream:
    """Turns a Python stream, or a JVM output stream, into a JVM output stream."""
    if isinstance(output, OutputStream):
        return output
    elif isinstance(output, IOBase):
        return Channels.newOutputStream(PythonByteChannel(output))
    else:
        raise _invalid(output)


def ensure_writer(output: IOBase | OutputStream | Writer) -> Writer:
    """Turns a Python stream, or a JVM output stream or writer, into a JVM writer.

    The writer buffers what it is given: flush it to reach the stream.
    """
    if isinstance(output, Writer):
        return output
    elif isinstance(output, OutputStream):
        return _jio.OutputStreamWriter(output, _ENCODING)
    elif isinstance(output, IOBase):
        return Channels.newWriter(PythonByteChannel(output), _ENCODING)
    else:
        raise _invalid(output)


# Python streams are accepted wherever the JVM expects streams (binary) or readers and writers (text)
for _binary in _BINARY_STREAMS:
    JConversion("java.io.InputStream", instanceof=_binary)(lambda _, obj: ensure_input_stream(obj))
    JConversion("java.io.OutputStream", instanceof=_binary)(
        lambda _, obj: ensure_output_stream(obj)
    )
JConversion("java.io.Reader", instanceof=TextIOBase)(lambda _, obj: ensure_reader(obj))
JConversion("java.io.Writer", instanceof=TextIOBase)(lambda _, obj: ensure_writer(obj))


logger.debug("Configure JVM-specific IO extensions")
