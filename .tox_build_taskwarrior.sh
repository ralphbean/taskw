#!/usr/bin/env bash

set -e

TW_GIT_REPO="https://github.com/GothenburgBitFactory/taskwarrior.git"

if [ -z "$1" ]; then
  echo "envdir not specified"
  echo 'Usage: .tox_build_taskwarrior.sh "{envdir}" "{toxinidir}"'
  exit 1
fi

if [ ! -x "$1/bin/task" ]; then
    rm -rf "${1?}/task"
    # --branch is misleading - it also accepts tags
    # So we can do a shallow checkout of a specific tag:
    git clone --depth 1 "${TW_GIT_REPO?}" $1/task --branch ${TASKWARRIOR?}
    cd $1/task
    # Use the 'release build' just to make things faster
    # Note about prefix: we are in {envdir}/task, so our install prefix
    # is out level up (thus '..').
    cmake -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_PREFIX:PATH=.. .
    # Run parralell build as majority of environments these days would have at
    # least two CPUs.
    make -j2
    make install
    cd $2
fi
