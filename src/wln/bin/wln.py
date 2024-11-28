#!/usr/bin/env python3
# coding=utf-8

import platform
import sys
import os
import argparse
import subprocess

__realfiledir__ = os.path.dirname(os.path.realpath(__file__))
from wurial import Wurial


def call_wln_ps1(args):
    """
    Last Update: @2024-11-28 00:09:20
    ---------------------------------

    """
    items = []
    for it in args.items:
        wr = Wurial(it)
        if not wr.isWinItem():
            raise TypeError
        if wr.from_relative:
            items.append(it)
        else:
            items.append(wr.uri_win)

    wr_script = Wurial(__realfiledir__ + "/wln.ps1")
    arguments = ""
    if args.backup:
        arguments += " -backup "
        if args.suffix:
            arguments += f" -suffix {args.suffix} "

    if args.force:
        arguments += " -force "
    elif args.interactive:
        arguments += " -interactive "

    if args.no_dereference:
        arguments += " -noDereference "

    if args.symbolic:
        arguments += " -symbolic "
    else:
        if args.logical:
            arguments += " -logical "
        elif args.physical:
            arguments += " -physical "

    if args.relative:
        arguments += " -relative "

    if args.verbose:
        arguments += " -ShowVerbose "

    if args.version:
        arguments += " -Version "

    if args.target_directory:
        arguments += f" -targetDirectory {args.target_diectory}"

    if args.no_target_directory:
        arguments += " -noTargetDirectory "

    print(f"""pwsh.exe -Command "{wr_script.uri_win} {arguments} {' '.join(items)}" """)
    if not args.no_exec:
        ret = subprocess.run(f"""pwsh.exe -Command "{wr_script.uri_win} {arguments} {' '.join(items)}" """, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Windows links in WSL")
    parser.add_argument("items", nargs="+", help="items for sources and optional target at last")
    parser.add_argument("--backup", "-b", action="store_true", default=False, help="make a backup of each existing destination file")
    parser.add_argument("--force", "-f", action="store_true", default=False, help="remove existing destination files")
    parser.add_argument("--interactive", "-i", action="store_true", default=False, help="prompt whether to remove destinations")
    parser.add_argument("--logical", "-L", action="store_true", default=False, help=" dereference TARGETs that are symbolic links")
    parser.add_argument("--no-dereference", "-n", action="store_true", default=False, help="prompt whether to remove destinations")
    parser.add_argument("--physical", "-P", action="store_true", default=False, help="make hard links directly to symbolic links")
    parser.add_argument("--relative", "-r", action="store_true", default=False, help="with -s, create links relative to link location")
    parser.add_argument("--symbolic", "-s", action="store_true", default=False, help="make symbolic links instead of hard links")
    parser.add_argument("--suffix", "-S", help="override the usual backup suffix")
    parser.add_argument("--target-directory", "-t", help="specify the DIRECTORY in which to create the links")
    parser.add_argument("--no-target-directory", "-T", action="store_true", help="treat LINK_NAME as a normal file always")
    parser.add_argument("--verbose", "-v", action="store_true", help="print name of each linked file")
    parser.add_argument("--version", action="store_true", help="output version information and exit")
    parser.add_argument("--no-exec", action="store_true", help="(python only) Just print the command without execution")

    args = parser.parse_args()

    call_wln_ps1(args)
