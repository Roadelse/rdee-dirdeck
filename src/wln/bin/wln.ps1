<#
.SYNOPSIS
Windows implementation of Linux ln command
.DESCRIPTION
Creates hard or symbolic links in Windows, mimicking Linux ln command behavior

Not implemented yet:
    - $logical
    - $noDereference
    - $physical
    - $showVerbose
#>



param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Targets,

    [alias('f')][switch]$force,
    [alias('i')][switch]$interactive,
    [alias('L')][switch]$logical,
    [alias('n')][switch]$noDereference,
    [alias('P')][switch]$physical,
    [alias('r')][switch]$relative,
    [alias('s')][switch]$symbolic,
    [string]$suffix,
    [string]$targetDirectory,
    [alias('T')][switch]$noTargetDirectory,
    [alias('v')][switch]$showVerbose,
    [alias('b')][switch]$backup,
    [switch]$help,
    [switch]$version
)

$ErrorActionPreference = 'Stop'

# Version and help information
$MY_VERSION = "24.11.27"

function ShowHelp {
    @"
Usage: wln [OPTION]... TARGET LINK_NAME
  or:  wln [OPTION]... TARGET
  or:  wln [OPTION]... TARGET... DIRECTORY
  or:  wln [OPTION]... -t DIRECTORY TARGET...

Options:
  -b, --backup                  make a backup of each existing destination file, with suffix of ~
  -f, --force                   remove existing destination files
  -i, --interactive             prompt whether to remove destinations
  -L, --logical                 dereference TARGETs that are symbolic links
  -n, --no-dereference          treat LINK_NAME as a normal file if it is a symbolic link to a directory
  -P, --physical                make hard links directly to symbolic links
  -r, --relative                create symbolic links relative to link location
  -s, --symbolic                make symbolic links instead of hard links
  --suffix=SUFFIX               override the usual backup suffix
  --target-directory            specify the DIRECTORY in which to create the links
  -T, --no-target-directory     treat LINK_NAME as a normal file always
  -v, --showVerbose             print name of each linked file
      --help                    display this help and exit
      --version                 output version information and exit
"@
    exit 0
}

function ShowVersion {
    Write-Host "wln version $MY_VERSION"
    exit 0
}

function GetBackupName {
    param([string]$path)
    $backupSuffix = if ($suffix) { $suffix } else { "~" }
    return "${path}${backupSuffix}"
}

function MakeBackup {
    param([string]$path)
    $backupPath = GetBackupName $path
    if (Test-Path $path) {
        Copy-Item -Path $path -Destination $backupPath -Force
    }
}

function CreateLink {
    param(
        [string]$target,
        [string]$link
    )
    # echo "target=$target, link=$link"
    # Check if destination exists
    if (Test-Path $link) {
        if ($force) {
            Remove-Item -Path $link -Force
        }
        elseif ($interactive) {
            $response = Read-Host "File '$link' exists. Remove it? [y/N]"
            if ($response -ne "y" -and $response -ne "Y") {
                return
            }
            Remove-Item -Path $link -Force
        }
        elseif ($backup) {
            MakeBackup $link
            Remove-Item -Path $link -Force
        }
        else {
            Write-Error "File '$link' already exists"
            return
        }
    }

    # Create the link
    try {
        if ($symbolic) {
            # $linkType = if ((Get-Item $target).PSIsContainer) { "Directory" } else { "File" }
            # echo "[System.IO.Path]::GetRelativePath([System.IO.Path]::GetDirectoryName($link), $target)"
            $target_dir = [System.IO.Path]::GetDirectoryName($link)
            if ("" -eq $target_dir) {
                $target_dir = $pwd.Path
            }
            $targetPath = if ($relative) {
                [System.IO.Path]::GetRelativePath($target_dir, $target)
            }
            else {
                $target
            }
            New-Item -ItemType SymbolicLink -Path $link -Target $targetPath | Out-Null
        }
        else {
            New-Item -ItemType HardLink -Path $link -Target $target | Out-Null
        }
        
        if ($verbose) {
            "'$target' -> '$link'"
        }
    }
    catch {
        Write-Error "Failed to create link: $_"
    }
}

# Main logic
if ($help) { ShowHelp }
if ($version) { ShowVersion }

if ($Targets.Count -eq 0) {
    Write-Error "Missing target operand"
    exit 1
}

# Handle different usage forms
if ($targetDirectory) {
    # Form 4: ln -t DIRECTORY TARGET...
    foreach ($target in $Targets) {
        $linkName = Join-Path $targetDirectory (Split-Path $target -Leaf)
        CreateLink $target $linkName
    }
}
elseif ($Targets.Count -eq 1) {
    # Form 2: ln TARGET (create in current directory)
    $linkName = Split-Path $Targets[0] -Leaf
    CreateLink $Targets[0] $linkName
}
elseif ($Targets.Count -eq 2 -and !$noTargetDirectory -and (Test-Path $Targets[-1] -PathType Container)) {
    # Form 3: ln TARGET DIRECTORY
    $linkName = Join-Path $Targets[-1] (Split-Path $Targets[0] -Leaf)
    CreateLink $Targets[0] $linkName
}
elseif ($Targets.Count -eq 2) {
    # Form 1: ln TARGET LINK_NAME
    CreateLink $Targets[0] $Targets[1]
}
else {
    # Form 3: ln TARGET... DIRECTORY
    $directory = $Targets[-1]
    if (!(Test-Path $directory -PathType Container)) {
        Write-Error "Target '$directory' is not a directory"
        exit 1
    }
    
    $Targets[0..($Targets.Count - 2)] | ForEach-Object {
        $linkName = Join-Path $directory (Split-Path $_ -Leaf)
        CreateLink $_ $linkName
    }
}