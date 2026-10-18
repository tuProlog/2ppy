"""Tests for `tuprolog.jvmioutils`."""

from io import IOBase

import jpype
import pytest

from tuprolog.jvmioutils import (
    BufferedReader,
    Files,
    InputStream,
    InputStreamReader,
    Paths,
    Reader,
    ensure_input_steam,
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
    assert isinstance(ensure_input_steam(path), InputStream)


def test_ensure_input_stream_from_stream(stream):
    assert ensure_input_steam(stream) is stream


@pytest.mark.parametrize("value", [42, None, b"bytes"])
def test_ensure_input_stream_rejects_other_types(value):
    with pytest.raises(TypeError, match="Invalid type"):
        ensure_input_steam(value)


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
