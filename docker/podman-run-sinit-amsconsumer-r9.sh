#!/bin/bash

AMSCONSUMER_SOURCE="${HOME}/my_work/srce/git.ams-consumer/ams-consumer"

podman run \
--security-opt label=disable \
--userns=keep-id \
-e "DISPLAY=unix$DISPLAY" \
--log-driver k8s-file \
--log-opt max-size=10m \
-v /dev/log:/dev/log \
-v /etc/localtime:/etc/localtime \
\
-v "${HOME}":/mnt/ \
-v "${HOME}"/.ssh:/home/user/.ssh/ \
-v "${AMSCONSUMER_SOURCE}":/home/user/amsconsumer-source \
\
-h amsconsumer-r9 \
--net host \
--name amsconsumer-r9 \
-u root \
--rm -ti \
localhost/ams-consumer-r9
