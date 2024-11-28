

#@ Last-Update 2024-08-01 10:11:10

#@ Introduction
# The script implements serverl wrapper powershell functions for calling wurial.py
#@


#@ Prepare
$__wurialpy = "$PSScriptRoot/wurial.py"


#@ Main
function wurial() {
    python $__wurialpy @args
}

function path2wsl() {
    param(
        [string]$path
    )
    python $__wurialpy path2wsl $path
}

function path2win() {
    param(
        [string]$path
    )
    python $__wurialpy path2win $path
}

function path8sys() {
    param(
        [string]$path
    )
    python $__wurialpy path8sys $path
}


