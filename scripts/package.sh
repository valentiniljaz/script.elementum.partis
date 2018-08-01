#!/bin/bash

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CURDIR/..
mkdir -p ./output
git archive --format zip --output ./output/script.elementum.partis.zip --prefix=script.elementum.partis/ master