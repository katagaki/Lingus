FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

RUN echo "deb https://deb.debian.org/debian/ bookworm contrib" >> /etc/apt/sources.list && \
    apt update && \
    echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    apt -y install --no-install-recommends libreoffice openjdk-17-jre \
    fontconfig ttf-mscorefonts-installer fonts-ipafont && \
    apt clean

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync --frozen --compile-bytecode --verbose && \
    uv cache clean
RUN uv run docling-tools models download layout

COPY lingus ./lingus
COPY app.py ./

CMD ["uv", "run", "app.py"]