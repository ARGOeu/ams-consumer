#!/bin/bash

VENV="/opt/ams-consumer"
AMSCONSUMER_SOURCE="${HOME}/my_work/srce/git.ams-consumer/ams-consumer"

podman run \
--security-opt label=disable \
--userns=keep-id \
-e "DISPLAY=unix$DISPLAY" \
--log-driver k8s-file \
--log-opt max-size=10m \
-v /dev/log:/dev/log \
-v /etc/localtime:/etc/localtime \
-h amsconsumer-r9 \
--net host \
--name amsconsumer-r9 \
\
-v "${HOME}":/mnt/ \
-v "${HOME}"/.ssh:/home/user/.ssh/ \
-v "${AMSCONSUMER_SOURCE}":/home/user/amsconsumer-source \
\
-v "${AMSCONSUMER_SOURCE}"/bin/:"${VENV}"/usr/bin:ro \
-v "${AMSCONSUMER_SOURCE}"/pymod/:"${VENV}"/lib/python3.9/site-packages/argo_ams_consumer:ro \
-v "${AMSCONSUMER_SOURCE}"/init/ams-consumer@.service:/usr/lib/systemd/system/ams-consumer@.service \
-v "${AMSCONSUMER_SOURCE}"/init/ams-consumers.target:/usr/lib/systemd/system/ams-consumers.target \
\
-v "${AMSCONSUMER_SOURCE}"/poetry.lock:${VENV}/poetry.lock \
-v "${AMSCONSUMER_SOURCE}"/pyproject.toml:${VENV}/pyproject.toml \
\
-u root \
--rm -ti \
localhost/ams-consumer-r9
