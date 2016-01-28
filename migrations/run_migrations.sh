#!/bin/sh

find . -name '*.sql' | xargs cat | mysql -u error_scarer -perror_scarer error_scarer
