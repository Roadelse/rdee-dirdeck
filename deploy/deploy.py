#!/usr/bin/env python3
# coding=utf-8
# winexec=python

import platform
import sys
import os
import subprocess

__filedir__ = os.path.dirname(__file__)
try:
    sys.path.append(f"{__filedir__}/../../rdee-core/deploy/tools")
    import deployer
except:
    from tools import deployer


if __name__ == "__main__":
    projname = os.path.abspath(os.path.join(__filedir__, ".."))
    params = deployer.main(projname)

    exportdir = params["exportdir"]
    pypkgpath = os.path.join(exportdir, "pypkg", "dirdeck")

    os.makedirs(pypkgpath, exist_ok=True)
    if platform.system() == "Linux":
        deployer.shrun(f"ln -sf {projname}/src/wurial/bin/wurial.py {pypkgpath}", ensure_noerror=True)
    else:
        deployer.shrun(f"New-Item -ItemType SymbolicLink -Target {projname}/src/wurial/bin/wurial.py -Path {pypkgpath}/wurial.py -Force", shell="pwsh", ensure_noerror=True)
