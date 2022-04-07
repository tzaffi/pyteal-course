#!/usr/bin/env bash

set -e # die on error

python ./create_signature.py ./build/ "$@"
