r"""Bridging Python streams and JVM ones.

2P-Kt reads and writes through JVM streams (`java.io.InputStream` and `java.io.OutputStream`, for
bytes) and through JVM readers and writers (`java.io.Reader` and `java.io.Writer`, for text). This
module converts Python streams into JVM ones, and vice versa:

- `ensure_input_stream`, `ensure_reader`, `ensure_output_stream` and `ensure_writer` turn paths,
  Python streams (e.g. `open(...)`, `sys.stdin`, `io.StringIO`, `io.BytesIO`) and JVM streams
  into the JVM stream, reader or writer wanted; text is encoded and decoded as UTF-8;
- Python binary streams are accepted wherever JVM code expects an `InputStream` or an
  `OutputStream`, and Python text streams wherever it expects a `Reader` or a `Writer`;
- JVM input streams are Python `io.IOBase`s: they can be read line by line, iterated over, and
  closed, as Python text streams.

Examples:
    >>> import io
    >>> stream = ensure_input_stream(io.BytesIO(b"first\nsecond\n"))
    >>> stream.readline()
    'first\n'
    >>> list(stream)
    ['second\n']
    >>> output = io.StringIO()
    >>> writer = ensure_writer(output)
    >>> writer.write("hello")
    >>> writer.flush()
    >>> output.getvalue()
    'hello'

See Also:
    `tuprolog.jvmutils`, for the other conversions between Python and the JVM.
"""

import codecs
from io import SEEK_SET, BufferedIOBase, IOBase, RawIOBase, TextIOBase
from os import PathLike, fspath

import java.io as _jio  # type: ignore
import java.nio.channels as _jnio_channels  # type: ignore
import java.nio.file as _jnio_file  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JArray, JByte, JConversion, JImplementationFor, JOverride

from tuprolog import logger
from tuprolog.jvmutils import customize_derived, jimplements

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
"""Java's stream of input bytes, `java.io.InputStream`.

Instances are Python `io.IOBase`s, readable line by line as text (UTF-8), and iterable over
their lines.
"""

Reader = _jio.Reader
"""Java's stream of input characters, `java.io.Reader` (see `ensure_reader`)."""

InputStreamReader = _jio.InputStreamReader
"""Java's `java.io.InputStreamReader`: a `Reader` decoding the bytes of an `InputStream`."""

BufferedReader = _jio.BufferedReader
"""Java's `java.io.BufferedReader`: a `Reader` buffering another one."""

Files = _jnio_file.Files
"""Java's `java.nio.file.Files` utility class, operating on files (see `open_file`)."""

Paths = _jnio_file.Paths
"""Java's `java.nio.file.Paths` utility class, creating file paths (e.g. `Paths.get("kb.pl")`)."""

OutputStream = _jio.OutputStream
"""Java's stream of output bytes, `java.io.OutputStream` (see `ensure_output_stream`)."""

Writer = _jio.Writer
"""Java's stream of output characters, `java.io.Writer` (see `ensure_writer`)."""

Channels = _jnio_channels.Channels
"""Java's `java.nio.channels.Channels` utility class, adapting byte channels into streams,
readers and writers."""

_ENCODING = "UTF-8"

_BINARY_STREAMS = (RawIOBase, BufferedIOBase)


@JImplementationFor("java.io.InputStream")
@customize_derived("close")
class _JvmInputStream:
    """Makes JVM input streams Python `io.IOBase`s, read as UTF-8 text.

    They are readable but neither seekable nor writable; reading lines buffers the stream, so
    lines and raw bytes should not be read from the same stream.
    """

    def __jclass_init__(cls):
        IOBase.register(cls)

    @JOverride
    def close(self):
        """Closes the stream."""
        self._closed = True
        self._close()

    @property
    def closed(self):
        """Whether the stream was closed via `close`."""
        if hasattr(self, "_closed"):
            return self._closed
        else:
            return False

    def fileno(self):
        """Raises `OSError`, as JVM streams have no file descriptor."""
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def flush(self):
        """Does nothing, as input streams have nothing to flush."""

    def isatty(self):
        """False: JVM streams are not seen as interactive."""
        return False

    def readable(self):
        """True: input streams can be read."""
        return True

    def seekable(self):
        """False: JVM input streams cannot be repositioned."""
        return False

    def writable(self):
        """False: input streams cannot be written."""
        return False

    def _buffer(self):
        if not hasattr(self, "_buffered"):
            self._buffered = BufferedReader(InputStreamReader(self))

    def readline(self, size=-1):
        """Reads a line of text, decoded as UTF-8.

        Args:
            size: The maximum amount of characters to read (no limit if negative or None).

        Returns:
            The line, including its trailing newline if read; an empty string at the end of the
            stream.
        """
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
        """Reads the remaining lines of text.

        Args:
            hint: If positive, no more lines are read once their total length reaches it.

        Returns:
            The list of the lines read.
        """
        lines, total = [], 0
        while line := self.readline():
            lines.append(line)
            total += len(line)
            if hint is not None and 0 < hint <= total:
                break
        return lines

    def __iter__(self):
        """Iterates over the remaining lines of text."""
        return iter(self.readline, "")

    def seek(self, offset: int, whence=SEEK_SET):
        """Raises `OSError`, as JVM input streams are not seekable."""
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def tell(self):
        """Raises `OSError`, as JVM input streams are not seekable."""
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def truncate(self, size=None):
        """Raises `OSError`, as input streams cannot be written."""
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")

    def writelines(self, lines):
        """Raises `OSError`, as input streams cannot be written."""
        raise OSError("This IOBase is backed by an instance of <java.io.InputStream>")


@jimplements(
    "java.nio.channels.ReadableByteChannel", "java.nio.channels.WritableByteChannel", deferred=True
)
class PythonByteChannel:
    """A JVM byte channel reading from, or writing to, a Python stream.

    Text streams are encoded and decoded as UTF-8, binary ones are passed through.
    Closing the channel leaves the stream open, as the stream belongs to its Python owner.
    Text streams are read line by line, so that interactive streams (e.g. `sys.stdin`) give
    their input as soon as a line is entered.

    Args:
        stream: The Python stream to read from, or to write to.

    Examples:
        >>> import io
        >>> PythonByteChannel(io.BytesIO(b"bytes")).isOpen()
        True
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
    def read(self, buffer) -> int:
        """Reads bytes from the stream into a JVM `java.nio.ByteBuffer`.

        Returns:
            The number of bytes read, 0 if a non-blocking stream has no data yet, or -1 at the
            end of the stream.
        """
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
    def write(self, buffer) -> int:
        """Writes the bytes remaining in a JVM `java.nio.ByteBuffer` to the stream.

        Returns:
            The number of bytes written.
        """
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
        """Whether the channel was not closed."""
        return self._open

    @JOverride
    def close(self):
        """Closes the channel, leaving the stream open."""
        self._open = False


def open_file(path: str) -> InputStream:
    """Opens a file for reading, as a JVM input stream.

    Args:
        path: The path of the file.

    Returns:
        The input stream, to be closed by the caller.

    Raises:
        java.nio.file.NoSuchFileException: If the file does not exist.
    """
    return Files.newInputStream(Paths.get(path))


def _invalid(value) -> TypeError:
    return TypeError(f"Invalid type: {type(value)}")


def ensure_input_stream(input: str | PathLike | IOBase | InputStream) -> InputStream:
    """Turns a path, a Python stream, or a JVM input stream into a JVM input stream.

    Args:
        input: A path (a string or a path-like object) of a file to open, a Python stream (text
            streams are encoded as UTF-8), or a JVM input stream, returned as it is. Strings are
            always paths, never the text to read.

    Returns:
        The JVM input stream.

    Raises:
        TypeError: If `input` is none of the above.

    Examples:
        >>> import io
        >>> ensure_input_stream(io.StringIO("text")).readline()
        'text'
    """
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
    """Turns a path, a Python stream, or a JVM input stream or reader into a JVM reader.

    Args:
        input: A JVM reader, returned as it is, a Python stream, or anything
            `ensure_input_stream` accepts. Bytes are decoded as UTF-8.

    Returns:
        The JVM reader.

    Raises:
        TypeError: If `input` is none of the above.

    Examples:
        >>> import io
        >>> chr(ensure_reader(io.StringIO("hi")).read())
        'h'
    """
    if isinstance(input, Reader):
        return input
    elif isinstance(input, IOBase) and not isinstance(input, InputStream):
        return Channels.newReader(PythonByteChannel(input), _ENCODING)
    else:
        return InputStreamReader(ensure_input_stream(input), _ENCODING)


def ensure_output_stream(output: IOBase | OutputStream) -> OutputStream:
    """Turns a Python stream, or a JVM output stream, into a JVM output stream.

    Args:
        output: A Python stream (text streams receive the bytes decoded as UTF-8), or a JVM
            output stream, returned as it is.

    Returns:
        The JVM output stream.

    Raises:
        TypeError: If `output` is none of the above.

    Examples:
        >>> import io
        >>> buffer = io.BytesIO()
        >>> ensure_output_stream(buffer).write(65)
        >>> buffer.getvalue()
        b'A'
    """
    if isinstance(output, OutputStream):
        return output
    elif isinstance(output, IOBase):
        return Channels.newOutputStream(PythonByteChannel(output))
    else:
        raise _invalid(output)


def ensure_writer(output: IOBase | OutputStream | Writer) -> Writer:
    """Turns a Python stream, or a JVM output stream or writer, into a JVM writer.

    The writer buffers what it is given: flush it to reach the stream.

    Args:
        output: A JVM writer, returned as it is, a JVM output stream, or a Python stream. Text is
            encoded as UTF-8.

    Returns:
        The JVM writer.

    Raises:
        TypeError: If `output` is none of the above.
    """
    if isinstance(output, Writer):
        return output
    elif isinstance(output, OutputStream):
        return _jio.OutputStreamWriter(output, _ENCODING)
    elif isinstance(output, IOBase):
        return Channels.newWriter(PythonByteChannel(output), _ENCODING)
    else:
        raise _invalid(output)


# Python streams are accepted wherever the JVM expects streams (binary) or readers and writers
# (text)
for _binary in _BINARY_STREAMS:
    JConversion("java.io.InputStream", instanceof=_binary)(lambda _, obj: ensure_input_stream(obj))
    JConversion("java.io.OutputStream", instanceof=_binary)(
        lambda _, obj: ensure_output_stream(obj)
    )
JConversion("java.io.Reader", instanceof=TextIOBase)(lambda _, obj: ensure_reader(obj))
JConversion("java.io.Writer", instanceof=TextIOBase)(lambda _, obj: ensure_writer(obj))


logger.debug("Configure JVM-specific IO extensions")
