#!/bin/bash

NFS_MOUNT="/mnt/backup"
STAGE="{{ env }}"
DEST_DIR="$NFS_MOUNT/bind/$STAGE"

mkdir -p "$DEST_DIR"
chmod 700 "$DEST_DIR"

rsync -a --no-owner --no-group "/etc/bind/named.conf" "$DEST_DIR/"
rsync -a --no-owner --no-group "/var/lib/bind/" "$DEST_DIR/"
