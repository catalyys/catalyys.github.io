#!/bin/bash

NFS_MOUNT="/mnt/backup"
STAGE="{{ env }}"
DEST_DIR="$NFS_MOUNT/docker/$STAGE"

mkdir -p "$DEST_DIR"
chmod 700 "$DEST_DIR"

rsync -a --no-owner --no-group "/opt/docker/nginx" "$DEST_DIR/"
