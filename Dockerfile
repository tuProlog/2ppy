# The image of 2PPy: Python and 2PPy (whose JVM comes with jdk4py), running 2ppy TUI by default.
# It installs the wheel in dist/ (`uv run poe build-jars && uv build`); release.config.mjs builds
# and publishes it on each release. Its options can be set via TWOPPY_* environment variables
# (see `2ppy-tui --help`), e.g.: docker run -it --rm -e TWOPPY_QUERY="member(X, [1, 2])" <image>
FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/tuProlog/2ppy" \
      org.opencontainers.image.description="2PPy (tuProlog for Python), running 2ppy TUI by default" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1

# a bind mount, not a COPY: the wheel stays out of the image's layers
RUN --mount=type=bind,source=dist,target=/dist \
    pip install /dist/*.whl \
    && useradd --create-home --uid 1000 2ppy \
    && mkdir /work && chown 2ppy /work

USER 2ppy
WORKDIR /work
ENTRYPOINT ["2ppy-tui"]
