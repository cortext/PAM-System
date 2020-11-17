FROM python:3
MAINTAINER Juan Pablo <gnupablo@portonmail.com>

ARG APP_NAME=pam
ENV APP_NAME=${APP_NAME}

ARG USER_ID="10001"
ARG GROUP_ID="app"
ARG HOME="/app"

ENV HOME=${HOME}
RUN groupadd --gid ${USER_ID} ${GROUP_ID} && \
    useradd --create-home --uid ${USER_ID} --gid ${GROUP_ID} --home-dir /app ${GROUP_ID}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        file        \
        gcc         \
        libwww-perl && \
    apt-get autoremove -y && \
    apt-get clean

RUN pip install --upgrade pip

WORKDIR ${HOME}

ADD requirements requirements/
RUN pip install -r requirements/requirements.txt

ADD . ${HOME}/${APP_NAME}
ENV PATH $PATH:${HOME}/${APP_NAME}/bin

RUN pip install -e ${HOME}/${APP_NAME}

RUN chown -R ${USER_ID}:${GROUP_ID} ${HOME}
USER ${USER_ID}

ENTRYPOINT ["entrypoint"]
