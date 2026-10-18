"""Tests for `tuprolog.jvmioutils`."""

import io
from io import IOBase

import jpype
import pytest

from tuprolog.jvmioutils import (
    BufferedReader,
    Files,
    InputStream,
    InputStreamReader,
    OutputStream,
    Paths,
    PythonByteChannel,
    Reader,
    Writer,
    ensure_input_steam,
    ensure_input_stream,
    ensure_output_stream,
    ensure_reader,
    ensure_writer,
    open_file,
)

ByteArrayInputStream = jpype.JClass("java.io.ByteArrayInputStream")

CONTENT = "first line\nsecond line\nthird line"


@pytest.fixture
def path(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text(CONTENT, newline="\n")
    return str(file)


@pytest.fixture
def stream(path):
    return open_file(path)


def test_definitions():
    assert InputStream == jpype.JClass("java.io.InputStream")
    assert Reader == jpype.JClass("java.io.Reader")
    assert InputStreamReader == jpype.JClass("java.io.InputStreamReader")
    assert BufferedReader == jpype.JClass("java.io.BufferedReader")
    assert Files == jpype.JClass("java.nio.file.Files")
    assert Paths == jpype.JClass("java.nio.file.Paths")


def test_open_file(stream):
    assert isinstance(stream, InputStream)
    assert bytes(stream.readAllBytes()).decode() == CONTENT


def test_open_missing_file(tmp_path):
    with pytest.raises(Exception, match="NoSuchFileException"):
        open_file(str(tmp_path / "missing.txt"))


def test_ensure_input_stream_from_path(path):
    assert isinstance(ensure_input_stream(path), InputStream)


def test_ensure_input_stream_from_stream(stream):
    assert ensure_input_stream(stream) is stream


@pytest.mark.parametrize("value", [42, None, b"bytes"])
def test_ensure_input_stream_rejects_other_types(value):
    with pytest.raises(TypeError, match="Invalid type"):
        ensure_input_stream(value)


# --- InputStream as Python IOBase -----------------------------------------------------------------


def test_input_stream_is_an_iobase(stream):
    assert isinstance(stream, IOBase)


def test_input_stream_capabilities(stream):
    assert stream.readable()
    assert not stream.writable()
    assert not stream.seekable()
    assert not stream.isatty()
    assert stream.flush() is None


@pytest.mark.parametrize(
    "operation",
    [
        lambda s: s.fileno(),
        lambda s: s.seek(0),
        lambda s: s.tell(),
        lambda s: s.truncate(),
        lambda s: s.truncate(0),
        lambda s: s.writelines(["x"]),
    ],
)
def test_input_stream_unsupported_operations(stream, operation):
    with pytest.raises(OSError):
        operation(stream)


def test_input_stream_initially_open(stream):
    assert not stream.closed


def test_input_stream_closed_after_close(stream):
    stream.close()
    assert stream.closed


def test_input_stream_readline(stream):
    assert stream.readline() == "first line\n"
    assert stream.readline() == "second line\n"
    assert stream.readline() == "third line"
    assert stream.readline() == ""


def test_input_stream_readline_with_size(stream):
    assert stream.readline(5) == "first"
    assert stream.readline() == " line\n"


def test_input_stream_readlines(stream):
    assert stream.readlines() == ["first line\n", "second line\n", "third line"]


def test_input_stream_readlines_with_hint(stream):
    assert stream.readlines(1) == ["first line\n"]
    assert stream.readlines() == ["second line\n", "third line"]


def test_input_stream_iteration(stream):
    assert list(stream) == ["first line\n", "second line\n", "third line"]


def test_input_stream_unicode():
    stream = ByteArrayInputStream("città\n".encode())
    assert stream.readline() == "città\n"


def test_input_stream_supplementary_characters():
    stream = ByteArrayInputStream("a😀b\n😀\n".encode())
    assert stream.readline(2) == "a😀"
    assert stream.readline() == "b\n"
    assert stream.readline() == "😀\n"


def test_empty_input_stream():
    stream = ByteArrayInputStream(b"")
    assert stream.readline() == ""
    assert stream.readlines() == []
    assert list(stream) == []


# --- Python streams as JVM streams, readers and writers ------------------------------------------

TEXT = "plain, accented: è€, astral: 😀\nsecond line\n"


def read_all(reader) -> str:
    buffered = BufferedReader(reader)
    lines = []
    while (line := buffered.readLine()) is not None:
        lines.append(str(line))
    return "\n".join(lines) + "\n"


def read_bytes(stream) -> bytes:
    return bytes(b & 0xFF for b in stream.readAllBytes())


def test_misspelled_alias_is_kept():
    assert ensure_input_steam is ensure_input_stream


@pytest.mark.parametrize("stream", [io.StringIO(TEXT), io.BytesIO(TEXT.encode())])
def test_ensure_input_stream_from_python_streams(stream):
    jvm = ensure_input_stream(stream)
    assert isinstance(jvm, InputStream)
    assert read_bytes(jvm).decode() == TEXT


@pytest.mark.parametrize("stream", [io.StringIO(TEXT), io.BytesIO(TEXT.encode())])
def test_ensure_reader_from_python_streams(stream):
    reader = ensure_reader(stream)
    assert isinstance(reader, Reader)
    assert read_all(reader) == TEXT


def test_ensure_reader_from_paths_and_jvm_objects(path):
    assert read_all(ensure_reader(path)).startswith("first line\n")
    assert read_all(ensure_reader(open_file(path))).startswith("first line\n")
    reader = InputStreamReader(open_file(path))
    assert ensure_reader(reader) is reader


def test_ensure_output_stream_to_python_streams():
    binary, text = io.BytesIO(), io.StringIO()
    for target in (binary, text):
        stream = ensure_output_stream(target)
        assert isinstance(stream, OutputStream)
        stream.write(TEXT.encode())
        stream.flush()
    assert binary.getvalue() == TEXT.encode()
    assert text.getvalue() == TEXT


def test_text_output_decodes_split_characters():
    text = io.StringIO()
    stream = ensure_output_stream(text)
    for byte in "€".encode():
        stream.write(byte)
    assert text.getvalue() == "€"


def test_ensure_writer_to_python_streams():
    binary, text = io.BytesIO(), io.StringIO()
    for target in (binary, text):
        writer = ensure_writer(target)
        assert isinstance(writer, Writer)
        writer.write(TEXT)
        writer.flush()
    assert binary.getvalue() == TEXT.encode()
    assert text.getvalue() == TEXT


def test_ensure_writer_from_jvm_objects():
    target = jpype.JClass("java.io.ByteArrayOutputStream")()
    writer = ensure_writer(target)
    writer.write("è")
    writer.flush()
    assert bytes(b & 0xFF for b in target.toByteArray()).decode() == "è"
    assert ensure_writer(writer) is writer
    assert ensure_output_stream(target) is target


@pytest.mark.parametrize("function", [ensure_output_stream, ensure_writer])
@pytest.mark.parametrize("value", [42, None, "path"])
def test_ensure_output_rejects_other_types(function, value):
    with pytest.raises(TypeError, match="Invalid type"):
        function(value)


def test_python_streams_convert_implicitly():
    # binary streams where the JVM expects streams, text ones where it expects readers or writers
    assert read_all(InputStreamReader(io.BytesIO(TEXT.encode()))) == TEXT
    assert read_all(BufferedReader(io.StringIO(TEXT))) == TEXT
    text = io.StringIO()
    writer = jpype.JClass("java.io.PrintWriter")(text)
    writer.write("è")
    writer.flush()
    assert text.getvalue() == "è"


def test_closing_the_jvm_side_leaves_python_streams_open():
    stream = io.StringIO(TEXT)
    ensure_reader(stream).close()
    assert not stream.closed


def test_channel_reads_lines_lazily():
    lines = iter(["first\n", "second\n", ""])

    class Interactive(io.TextIOBase):
        def readline(self, size=-1):
            return next(lines)

    channel = PythonByteChannel(Interactive())
    buffer = jpype.JClass("java.nio.ByteBuffer").allocate(64)
    assert channel.read(buffer) == len("first\n")
    assert channel.read(buffer) == len("second\n")
    assert channel.read(buffer) == -1


def test_channel_on_non_blocking_streams_without_data():
    class NonBlocking(io.RawIOBase):
        def readable(self):
            return True

        def read(self, size=-1):
            return None

    channel = PythonByteChannel(NonBlocking())
    assert channel.read(jpype.JClass("java.nio.ByteBuffer").allocate(8)) == 0
    assert channel.isOpen()
    channel.close()
    assert not channel.isOpen()
