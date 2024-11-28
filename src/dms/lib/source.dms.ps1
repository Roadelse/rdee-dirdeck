

#@ Last-Update 2024-08-01 10:15:54

#@ Introduction
# The script implements serverl wrapper bash functions for calling dms.py
#@

#@ Prepare
$dmspy = "$PSScriptRoot\..\bin\dms.py"

#@ Main
#@ .General
function dms() {
    if ($args.Contains("goto")) {
        $rst = python $dmspy @args
        $rcode = $?
        Write-Output $rst
        if (-not $rcode) {
            return
        }
        Set-Location $rst
    }
    else {
        python $dmspy @args
    }
}

#@ .one-step-cut
function s() {
    param(
        [string]$name
    )
    dms save $name
}

function g() {
    param(
        [string]$path
    )

    if ($path -eq "list") {
        dms list
    } else {
        dms goto $path
    }
}


