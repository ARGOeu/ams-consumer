#!/bin/bash

declare -a paths

paths=("$HOME/my_work/srce/git.ams-consumer/ams-consumer/docker/pysitepkg/sitepkg32" \
	"$HOME/my_work/srce/git.ams-consumer/ams-consumer/docker/pysitepkg/sitepkg64")

for f in "${paths[@]}"
do
	PYTHONPATH="$PYTHONPATH:$f"
done

export PYTHONPATH
