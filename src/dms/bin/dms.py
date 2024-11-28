#!/usr/bin/env python3
# coding=utf-8

"""
The script implements the Directory-Management-System (DMS) in both Linux and Windows-WSL via python.
It relies on wurial.py to support windows-wsl paths simultaneously
"""


# @ Prepare
# @ .import
# @ ..STL-libs
import sys
import os
import argparse
import json
import warnings
# @ ..Local-libs

__realfiledir__ = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{__realfiledir__}/../../wurial/bin")
from wurial import Wurial


def save_dir(key: str, path: str):
    wr = Wurial(path)
    wr = wr.ensure_dir()
    namedirs[key] = wr.uri_linux
    with open(dms_dat_jsf, "w") as f:
        json.dump(namedirs, f)


def goto_dir(key: str):
    if not namedirs:
        print(rf"\033[31mError!\033[0m There is no dma data json file ({dms_dat_jsf}) now, save first then goto")
        sys.exit(101)
    if key not in namedirs:
        print(rf"\033[31mError!\033[0m You are using an undefined key! {key}")
        print("---------------Current keys---------------")
        list_dir()
        sys.exit(101)
    wr = Wurial(namedirs[key])
    if not wr.uri:
        print(namedirs)
        print(wr.uri_linux)
        print(wr.uri_win)
        raise RuntimeError(f"Cannot goto target directory ({namedirs[key]}), usually because the path denotes to pure Linux but you are in Windows")
    print(wr.uri)


def list_dir(nocolor: bool = False):
    if not namedirs:
        print("No records now")
        return

    for k, v in namedirs.items():
        if nocolor:
            print(f"{k:<20}{v}")
        else:
            print(f"\033[33m{k:<20}\033[0m{v}")


def del_dir(key: str):
    if key == "main":
        warnings.warn("You cannot del the main record")
        return

    if key in namedirs:
        del namedirs[key]

        with open(dms_dat_jsf, "w") as f:
            json.dump(namedirs, f)


def clear_dir():
    os.remove(dms_dat_jsf)


def find_dir(pattern: str, nocolor: bool = False):
    for k, v in namedirs.items():
        if pattern in k or pattern in v:
            if nocolor:
                print(f"{k:<8}{v}")
            else:
                k2 = k.replace(pattern, f"\033[32m{pattern}\033[0m")
                v2 = v.replace(pattern, f"\033[32m{pattern}\033[0m")
                print(f"{k2:<17}{v2}")  # @ exp | 17 = 8 + 9, where 9 denotes to ANSI Color code characters


if __name__ == "__main__":
    global namedirs

    parser = argparse.ArgumentParser(description="""directory management system, mainly used to fast navigation across Linux, Windows & WSL""")
    parser.add_argument("--dmsdat", default=None, help="Select dms data json file manually")
    parser.add_argument("--nocolor", action="store_true", help="Turn off colorful output")

    subparsers = parser.add_subparsers(dest='action', help='Select target actions')

    parser_save = subparsers.add_parser("save", help="save current working directory")
    parser_goto = subparsers.add_parser("goto", help="goto target directory via key")
    parser_list = subparsers.add_parser("list", help="list saved key:directory records")
    parser_clear = subparsers.add_parser("clear", help="clear all records")
    parser_del = subparsers.add_parser("del", help="delete one record")
    parser_find = subparsers.add_parser("find", help="find target records")

    parser_save.add_argument("key", nargs="?", default="main", help="key to store directory")
    parser_save.add_argument("path", nargs="?", default=".", help="directory to be stored")

    parser_goto.add_argument("key", nargs="?", default="main", help="key to store directory")

    parser_del.add_argument("key", help="delete target record by key")

    parser_find.add_argument("pattern", help="pattern to be searched")

    args = parser.parse_args()

    if args.dmsdat:
        dms_dat_jsf = Wurial.path8sys(args.dmsdat)
    else:
        dms_dat_jsf = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".dms-data.json")

    if not os.path.exists(dms_dat_jsf):
        namedirs = {}
    else:
        try:
            with open(dms_dat_jsf, "r") as f:
                namedirs = json.load(f)
        except:
            raise RuntimeError(f"Fail to load {dms_dat_jsf} as json")

    if args.action == "save":
        save_dir(args.key, args.path)
    elif args.action == "goto":
        goto_dir(args.key)
    elif args.action == "list":
        list_dir(nocolor=args.nocolor)
    elif args.action == "del":
        del_dir(args.key)
    elif args.action == "clear":
        clear_dir()
    elif args.action == "find":
        find_dir(args.pattern, nocolor=args.nocolor)
    elif args.action is None:
        print(dms_dat_jsf)
        print("-----------------------------------------")
        list_dir(args.nocolor)
    else:
        raise NotImplementedError
