#!/bin/bash
export PYTHONPATH="./sat-search:./sat-stac"
time \
python3 __main__.py download $@
