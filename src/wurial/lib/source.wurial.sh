#!/bin/bash

#@ Last-Update @2024-10-28 14:22:52

#@ Introduction
# The script implements serverl wrapper bash functions for calling wurial.py
#@


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "The script can only be sourced rather than executed"
    exit 0
fi

if [[ -n "$1" && "$1" == "unload" ]]; then
    unset -f wurial path2wsl path2win path8sys
    unset __wurialpy
    return
fi

#@ Prepare
__wurial_file__=$(realpath "${BASH_SOURCE[0]}")
__wurial_filedir__=$(dirname $__wurial_file__)
__wurialpy=${__wurial_filedir__}/../bin/wurial.py
unset __wurial_file__ __wurial_filedir__

#@ Main
#@ .General
function wurial() {
    $__wurialpy $*
}

#@ .one-step-cut
function path2wsl() {
    $__wurialpy path2wsl $*
}

function path2win() {
    $__wurialpy path2win $*
}

function path8sys() {
    $__wurialpy path8sys $*
}
