#!/bin/bash

#@ Last-Update 2024-08-01 10:15:54

#@ Introduction
# The script implements serverl wrapper bash functions for calling dms.py
#@

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "The script can only be sourced rather than executed"
    exit 0
fi

if [[ -n "$1" && "$1" == "unload" ]]; then
    unset -f wurial path2wsl path2win path8sys
    unset __dmspy
    return
fi

#@ Prepare
__dms_file__=$(realpath "${BASH_SOURCE[0]}")
__dms_filedir__=$(dirname $__dms_file__)
__dmspy=$(realpath ${__dms_filedir__}/../bin/dms.py)
unset __dms_file__ __dms_filedir__

#@ Main
#@ .General
function dms() {
    if [[ "$*" =~ (^| )goto($| ) ]]; then
        rst=$($__dmspy $*)
        rcode=$?
        echo -e "$rst"  #@ exp | use -e to color-print, use "" to display line-break correctly
        if [[ $rcode -ne 0 ]]; then
            echo -e "Error! Failed to goto"
            return
        fi
        cd $rst
    else
        $__dmspy $*
    fi
}

#@ .one-step-cut
function s() {
    dms save $*
}

function g() {
    if [[ -n "$1" && "$1" == "list" ]]; then
        dms list
        return
    fi
    dms goto $*
}
