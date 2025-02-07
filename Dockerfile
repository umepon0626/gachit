FROM python:slim AS rye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN \
  --mount=type=cache,target=/var/lib/apt/lists \
  --mount=type=cache,target=/var/cache/apt/archives \
  apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl git

WORKDIR /workspace
ENV PYTHONPATH="/workspace/gachit/src:$PYTHONPATH"
ENV RYE_HOME="/workspace/.rye"
ENV PATH="${RYE_HOME}/shims:${PATH}"


# 動作検証用のディレクトリの作成
COPY ./playground /workspace/playground
WORKDIR /workspace/playground
RUN git init && \
  git config user.email "git@example.com" && \
  git config user.name "test" && \
  git add . && \
  git commit -m "Initial commit"

WORKDIR /workspace

RUN mkdir -p /workspace/gachit
WORKDIR /workspace/gachit
# RYE_INSTALL_OPTIONはビルドに必要です。
# 参照: https://github.com/mitsuhiko/rye/issues/246
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash

# Dockerのキャッシュを利用するために、依存関係のダウンロードを別のステップとして行います。
# バインドマウントを利用して一部のファイルをこのレイヤーにコピーすることを避けます。
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=type=bind,source=requirements.lock,target=requirements.lock \
  --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
  --mount=type=bind,source=.python-version,target=.python-version \
  --mount=type=bind,source=README.md,target=README.md \
  rye sync --no-lock

RUN . .venv/bin/activate

ENV IS_TESTING_ENVIRONMENT=1
