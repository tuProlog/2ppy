"""Input and output channel stores."""

from tuprolog.solve.channel import (
    InputStore,
    OutputStore,
    input_channel,
    input_store,
    output_channel,
    output_store,
    std_err,
    std_in,
    std_out,
    warn,
)


def keys(store) -> set[str]:
    return {str(k) for k in store.keySet()}


def test_input_store_default():
    store = input_store()
    assert isinstance(store, InputStore)
    assert InputStore.STDIN in keys(store)


def test_input_store_with_stdin():
    store = input_store(input_channel("abc"))
    assert store.std_in.read() == "a"
    assert store.current.read() == "b"


def test_input_store_with_channels_only():
    store = input_store(channels={"foo": input_channel("x")})
    assert {"stdin", "foo"} <= keys(store)
    assert store["foo"].read() == "x"


def test_input_store_with_stdin_and_channels():
    store = input_store(input_channel("s"), {"foo": input_channel("x"), "bar": std_in()})
    assert {"stdin", "foo", "bar"} <= keys(store)
    assert store.std_in.read() == "s"


def test_output_store_default():
    store = output_store()
    assert isinstance(store, OutputStore)
    assert {OutputStore.STDOUT, OutputStore.STDERR} <= keys(store)


def test_output_store_with_custom_standard_channels():
    out, err, warnings = [], [], []
    store = output_store(
        output_channel(out.append), output_channel(err.append), output_channel(warnings.append)
    )
    store.std_out.write("o")
    store.std_err.write("e")
    store.warnings.write("w")
    assert (out, err, warnings) == (["o"], ["e"], ["w"])


def test_output_store_with_stderr_only():
    err: list[str] = []
    store = output_store(stderr=output_channel(err.append))
    store.std_err.write("e")
    assert err == ["e"]


def test_output_store_with_warnings_only():
    warnings: list[str] = []
    store = output_store(warnings=output_channel(warnings.append))
    store.warnings.write("w")
    assert warnings == ["w"]


def test_output_store_with_channels_only():
    written: list[str] = []
    store = output_store(channels={"foo": output_channel(written.append)})
    assert {"stdout", "stderr", "foo"} <= keys(store)
    store["foo"].write("x")
    assert written == ["x"]


def test_output_store_with_stdout_and_channels():
    out, foo = [], []
    store = output_store(output_channel(out.append), channels={"foo": output_channel(foo.append)})
    store.std_out.write("o")
    store["foo"].write("f")
    assert (out, foo) == (["o"], ["f"])


def test_standard_channels():
    for channel in [std_out(), std_err(), warn()]:
        assert not channel.is_closed
    assert not std_in().is_closed
