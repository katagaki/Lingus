FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

RUN apt update && \
    apt -y install --no-install-recommends libreoffice libreoffice-core libreoffice-common libreoffice-java-common \
    libreoffice-calc libreoffice-impress libreoffice-writer \
    default-jre && \
    apt clean

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --compile-bytecode --verbose && \
    uv cache clean
RUN uv run docling-tools models download layout

COPY app.py ./
COPY docs ./docs

CMD ["uv", "run", "app.py"]