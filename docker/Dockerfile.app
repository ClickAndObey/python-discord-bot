FROM python:3.9-slim as build-base

ARG VERSION

COPY dist/ /dist/
RUN pip3 install /dist/clickandobey.discord.bot-${VERSION}-py3-none-any.whl

FROM python:3.9-slim

ENV VERSION=1.0.0
ENV PYTHON_VERSION=3.9

COPY --from=build-base /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/site-packages/
COPY --from=build-base /usr/local/bin/ /usr/local/bin/

COPY src/main/commands /commands

ENTRYPOINT ["run_bot"]