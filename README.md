# readme

+ A versatile toolkit from the Roadelse series, specializing in file system management and organization.
+ Switch to `branch:rdee` if rdee style deployment is wanted

## Content

### wurial

+ Compatible URI for Window and Linux (WSL)
+ Serve as an executable with bash wrapper, but also listed in python package

### dms

+ Directory management system for quick cd
+ Serve as an executable with ncessary bash wrapper
+ Can go across between Windows and WSL via importing wurial

### wln

+ wln.ps1
    - A powershell script mimicking `ln` options on Linux
+ wln.py
    - A python wrapper for wln.ps1, which supports creating Windows links in WSL2 using `ln` options

### jsync

+ jsync
    - Project-level rsync wrapper 
+ jlink
    - Link only files and create necessary directories 
