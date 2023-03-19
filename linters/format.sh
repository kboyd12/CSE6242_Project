#!/bin/bash
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports src

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
black src

