#!/usr/bin/env python3
# coding=utf-8

"""
Windows URI And Linux (also WsL) toolkit, acting as python library and executable script simultaneouly
"""

from __future__ import annotations

import sys
import platform
import os
import os.path
import re
import warnings
import argparse


class Wurial:
    """
    URI for Window and Linux (including WSL and pure Linux)
    """

    def __init__(self, uri):
        self.system = platform.system()
        assert self.system in ("Windows", "Linux"), f"Unexpected system: {self.system}"

        self.uri_win = ""
        self.uri_linux = ""
        # print(f"{uri=}")
        self.from_relative: bool = False if (uri.startswith("/") or re.match(r'[C-X]:\\', uri)) else True
        if isinstance(uri, str):
            # print(f"{uri=}")
            uri_norm = Wurial.norm_path(uri)
            # print(f"{uri_norm=}")
            if uri_norm.startswith("/"):
                self.uri_linux = uri_norm
                self.uri_win = Wurial.path2win(uri_norm)
            elif re.match(r"[A-Z]:\\", uri_norm):
                self.uri_win = uri_norm
                self.uri_linux = Wurial.path2wsl(uri_norm)

        elif isinstance(uri, Wurial):
            self.uri_win = uri.ssuri_win
            self.uri_linux = uri.uri_linux
        else:
            raise TypeError(f"Unknwon argument::uri type: {type(uri)}")

    @property
    def uri(self):
        """
        Last Update: 2024-07-30 17:24:06
        ---------------------------------------------------
        """
        if self.system == "Windows":
            return self.uri_win
        else:
            return self.uri_linux

    @property
    def abspath(self):
        return self.uri

    @property
    def basename(self):
        return os.path.basename(self.uri)

    def join(self, rhs: str, sep: str = '/'):
        rhs_parts = rhs.split(sep)
        self.uri_linux += '/' + '/'.join(rhs_parts)
        if self.uri_win:
            self.uri_win += "\\" + "\\".join(rhs_parts)
        return self

    def exists(self) -> bool:
        """
        Last Update: 2024-07-30 17:29:56
        ---------------------------------------------------
        """
        return os.path.exists(self.uri)

    def directory(self) -> Wurial:
        """
        Get parent wurial object

        :return: wurial instance
        """
        return Wurial(os.path.dirname(self.uri))

    def ensure_dir(self) -> Wurial:
        """
        Get nearest directory, i.e., self.directory() for file and itself for directory
        """
        if self.isfile():
            return self.directory()
        return self

    def islink(self, require_valid: bool = False):
        """
        Last Update: 2024-07-30 23:15:02
        ---------------------------------------------------
        """
        rst = os.path.islink(self.uri)
        if not rst:
            return False

        if require_valid:
            wr = self.get_link_target()
            return wr.exists()
        else:
            return True

    def get_link_target(self, strict: bool = False):
        if self.islink():
            return Wurial(os.path.realpath(self.uri))
        else:
            if strict:
                warnings.warn("self is not a link")
            return self

    def isfile(self):
        return os.path.isfile(self.uri)

    def isdir(self):
        return os.path.isdir(self.uri)

    def isshortcut(self):
        """
        Check if the uri denotes to a shortcut link via extension
        Not very strict but may work at most of conditions
        """
        return self.uri_linux.endswith(".lnk")

    def issolid(self):
        return self.exists() and not self.islink() and not self.isshortcut()

    def getsize(self, unit: str = "B", follow_link: bool = False):
        if self.isdir():
            raise NotImplementedError("Wurial::getsize only support file now")
        obj = self
        if self.islink():
            if follow_link:
                obj = self.get_link_target()
                if not obj.exists():
                    return 0
            else:
                return 0

        filesize = os.path.getsize(obj.uri)
        if unit == "B":
            return filesize
        elif unit == "KB":
            return filesize / 1024
        elif unit == "MB":
            return filesize / (1024**2)
        else:
            raise NotImplementedError(f"Unknown unit by now: {unit}")

    def isWinItem(self):
        if self.uri_win:
            return True
        return False

    @staticmethod
    def norm_path(path: str):
        """
        Last Update: 2024-07-30 16:40:43
        ---------------------------------------------------
        Normalize the given path into a simplified full path
        ● Do not check existence
        ● Work for both absolute path and relative path
        ● Work for both Linux/Windows uri in any system

        :param path: target path, including both absolute path and relative path
        :return: normalized path
        """

        # @ Prepare
        if path.startswith("/"):
            systemT = "Linux"
        elif re.match(r"[A-Z]:", path):
            systemT = "Windows"
        else:
            systemT = platform.system()
            path = os.path.join(os.path.abspath(os.path.curdir), path)
        assert systemT in ("Windows", "Linux"), f"Unexpected system: {systemT}"

        # @ Main
        segments = re.split(r"\\|/", path)
        nodelist = []
        for seg in segments:
            if seg == "." or seg == "":
                continue
            elif seg == "..":
                if not nodelist:
                    raise RuntimeError("Cannot resolve parent node for root node")
                nodelist.pop(-1)
            else:
                if systemT == "windows" and not nodelist:
                    if not re.match(r'[A-Z]:$', seg):
                        raise RuntimeError("Illegal root node for Windows path")
                nodelist.append(seg)

        # @ Post-Process
        if systemT == "Windows":
            if not nodelist:
                raise RuntimeError("Cannot use none-path in windows")
            elif not re.match(r"[A-Z]:", nodelist[0]):
                raise RuntimeError("Disk symbol missing in Windows uri")
            return "\\".join(nodelist)
        else:
            if not nodelist:
                return "/"
            return "/" + "/".join(nodelist)

    @staticmethod
    def path2win(path: str, strict: bool = False):
        """
        Last Update: 2024-07-30 17:20:24
        ---------------------------------------------------
        :param path: target path to be converted, normalized automatically even no need for converting
        :param strict: Whether raise an error for illgeal path
        """
        uriN = Wurial.norm_path(path)
        if re.match(r"[A-Z]:", uriN):
            return uriN

        if not uriN.startswith("/mnt/"):
            if strict:
                raise RuntimeError(f"Cannot convert this path to windows uri: {path}")
            return ""

        uriW = uriN[5].upper() + ":" + uriN[6:].replace("/", "\\")
        return uriW

    @staticmethod
    def path2wsl(path: str):
        """
        Last Update: 2024-07-30 17:20:27
        ---------------------------------------------------
        :param path: target path to be converted, normalized automatically even no need for converting
        """
        uriN = Wurial.norm_path(path)
        if uriN.startswith("/"):
            return uriN

        if not re.match(r"[A-Z]:", uriN):
            raise RuntimeError(f"Cannot convert this path to wsl uri: {path}")

        uriL = "/mnt/" + uriN[0].lower() + uriN[2:].replace("\\", "/")

        return uriL

    @staticmethod
    def path8sys(path: str):
        """
        Retrieve path by current system
        """
        wr = Wurial(path)
        uri = wr.uri
        if not uri:
            raise RuntimeError(f"Error! Cannot resolve {path} in {wr.system}")
        return uri


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Selecting target action and corresponding arguments")
    subparsers = parser.add_subparsers(dest='action', help='Select target actions')

    parser_path2wsl = subparsers.add_parser("path2wsl", help="convert path to linux-path, remain itself if it is already a Linux-path")
    parser_path2wsl.add_argument("path", help="target path to be converted")

    parser_path2win = subparsers.add_parser("path2win", help="convert path to windows-path, remain itself if it is already a Windows-path")
    parser_path2win.add_argument("path", help="target path to be converted")

    parser_path8sys = subparsers.add_parser("path8sys", help="convert path to linux-path, remain itself if it is already a Linux-path")
    parser_path8sys.add_argument("path", help="target path to be converted")

    args = parser.parse_args()

    if args.action == "path2wsl":
        print(Wurial.path2wsl(args.path))
    elif args.action == "path2win":
        print(Wurial.path2win(args.path))
    elif args.action == "path8sys":
        print(Wurial.path8sys(args.path))
    else:
        raise NotImplementedError
