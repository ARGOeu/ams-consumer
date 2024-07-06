#!/bin/bash

VENV="/opt/ams-consumer/"
AMSCONSUMER_SOURCE="${HOME}/my_work/srce/git.ams-consumer/ams-consumer"

podman exec \
-t \
-u user \
-v "${HOME}":/mnt/ \
-v "${HOME}"/.ssh:/home/user/.ssh/ \
-v "${AMSCONSUMER_SOURCE}":/home/user/amsconsumer-source \
-v "${AMSCONSUMER_SOURCE}"/bin/:"${VENV}"/usr/bin/:ro,z \
-v "${AMSCONSUMER_SOURCE}"/pymod:"${VENV}"/lib/python3.9/site-packages:ro,z \
-i amsconsumer-r9 /bin/zsh
