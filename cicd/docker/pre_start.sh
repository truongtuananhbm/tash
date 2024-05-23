#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=./pre_start_backend.py
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    python3 "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi