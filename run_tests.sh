#!/bin/bash

TEST_FILE=$1

cd /opt/buzzfeed/pensieve
export PYTHONPATH=/opt/buzzfeed/pensieve


if [ -z "$TEST_FILE" ]
then
    nosetests "tests/integration/"
else
    nosetests --logging-level=INFO --nologcapture --nocapture -v --with-id "tests/integration/$TEST_FILE"
fi
