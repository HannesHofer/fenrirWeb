#!/bin/sh

mkdir -p /var/cache/fenrir
if [ ${INTERFACE} ]; then
    echo "executing: fenrir --inputinterface ${INTERFACE}"
    fenrir --inputinterface ${INTERFACE} &
else
    fenrir &
fi