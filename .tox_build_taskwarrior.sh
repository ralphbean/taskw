#!/usr/bin/env bash
if [ ! -d "$1/task" ]; then
    git clone https://git.tasktools.org/scm/tm/task.git $1/task
    cd $1/task
    git checkout $TASKWARRIOR
    # Use the 'release build' just to make things faster
    cmake -DCMAKE_BUILD_TYPE=release -DCMAKE_INSTALL_PREFIX:PATH=$1 .
    make
    make install
    cd $2
fi
