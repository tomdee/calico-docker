#!/bin/bash
echo "Removing extra packages"
apk del build-dependencies
rm -rf /var/cache/apk/*
rm -rf /build
rm -rf /tmp/* /var/tmp/*

