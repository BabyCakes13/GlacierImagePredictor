#!/bin/bash
export PYTHONPATH="./sat-search:./sat-stac"
time \
    python3 gits/__main__.py process "$@"
