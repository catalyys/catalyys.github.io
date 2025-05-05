#!/bin/bash

SOURCE_FILE="/etc/bind/named.conf"
NFS_MOUNT="/mnt/backup"
DEST_DIR="$NFS_MOUNT/bind"
STAGE="{{ env }}"

DEST_FILE="${STAGE}_$(basename "$SOURCE_FILE")"

mkdir -p "$DEST_DIR"
chmod 700 "$DEST_DIR"

rsync -a --no-owner --no-group "$SOURCE_FILE" "$DEST_DIR/$DEST_FILE"
