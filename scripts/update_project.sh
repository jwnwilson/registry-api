#! /bin/bash

set -e

if ! [ -x "$(command -v cruft)" ]
then
    echo "cruft could not be found, please install globally or in a virtual env"
    echo "https://cruft.github.io/cruft/#installation"
    exit
fi

cruft update
