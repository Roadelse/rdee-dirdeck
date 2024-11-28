# wln.Tests.ps1

BeforeAll {
    # 设置测试环境
    $script:testDir = "$PSScriptRoot\wln_test"
    $script:scriptPath = "$PSScriptRoot\..\src\wln\bin\wln.ps1"
    
    # 创建测试目录
    New-Item -ItemType Directory -Path $testDir -Force
    
    # 创建测试文件
    "Test Content 1" | Out-File "$testDir\f1"
    "Test Content 2" | Out-File "$testDir\f2"
    New-Item -ItemType Directory -Path "$testDir\d1" -Force
}

Describe "wln.ps1 Basic Functionality" {
    BeforeEach {
        # 每个测试前清理链接文件
        Remove-Item "$testDir\*" -Recurse -Force
        "Test Content 1" | Out-File "$testDir\f1"
        "Test Content 2" | Out-File "$testDir\f2"
        New-Item -ItemType Directory -Path "$testDir\d1" -Force
    }

    Context "Form 1: Create link with specific name" {
        It "Should create symbolic link with specified name" {
            $source = "$testDir\f1"
            $link = "$testDir\f1l"
            
            & $scriptPath -s $source $link
            
            Test-Path $link | Should -Be $true
            (Get-Item $link).LinkType | Should -Be "SymbolicLink"
        }

        It "Should create hard link with specified name" {
            $source = "$testDir\f1"
            $link = "$testDir\f3"
            
            & $scriptPath $source $link
            
            Test-Path $link | Should -Be $true
            (Get-Item $link).LinkType | Should -Be "HardLink"
        }
    }

    Context "Form 2: Create link in current directory" {
        It "Should create link in current directory with source name" {
            Push-Location $testDir\d1
            try {
                & $scriptPath -s "..\f1"
                Test-Path "f1" | Should -Be $true
                (Get-Item "f1").LinkType | Should -Be "SymbolicLink"

            }
            finally {
                Pop-Location
            }
        }
    }

    Context "Form 3: Create links in target directory" {
        It "Should create multiple links in target directory" {
            $source1 = "$testDir\f1"
            $source2 = "$testDir\f2"
            $targetDir = "$testDir\d1"
            
            & $scriptPath -s $source1 $source2 $targetDir
            
            Test-Path "$targetDir\f1" | Should -Be $true
            Test-Path "$targetDir\f2" | Should -Be $true
        }
    }

    Context "Form 4: Create links using -t option" {
        It "Should create links in specified directory using -t" {
            $source1 = "$testDir\f1"
            $source2 = "$testDir\f2"
            $targetDir = "$testDir\d1"
            
            & $scriptPath -s -targetDirectory $targetDir $source1 $source2
            
            Test-Path "$targetDir\f1" | Should -Be $true
            Test-Path "$targetDir\f2" | Should -Be $true
        }
    }
}

Describe "wln.ps1 Option Tests" {
    BeforeEach {
        Remove-Item "$testDir\*" -Recurse -Force
        "Test Content 1" | Out-File "$testDir\f1"
        "Test Content 2" | Out-File "$testDir\f2"
        New-Item -ItemType Directory -Path "$testDir\d1" -Force
    }

    Context "Backup options" {
        It "Should create backup with -b option" {
            $source = "$testDir\f1"
            $link = "$testDir\f2"
            
            & $scriptPath -b $source $link
            
            Test-Path "${link}~" | Should -Be $true
        }

        It "Should create backup with custom suffix" {
            $source = "$testDir\f1"
            $link = "$testDir\f2"
            
            & $scriptPath -b -suffix ".bak" $source $link
            
            Test-Path "${link}.bak" | Should -Be $true
        }
    }


    Context "Relative links" {
        It "Should create relative symbolic link with -r option" {
            $source = "$testDir\f1"
            $link = "$testDir\d1\f1l"
            
            & $scriptPath -s -r $source $link
            
            Test-Path $link | Should -Be $true
            (Get-Item $link).LinkType | Should -Be "SymbolicLink"
            # 验证是相对路径（这需要根据具体实现调整）
            $target = (Get-Item $link).Target
            $target | Should -Not -BeLike "$testDir*"
        }
    }
}

Describe "wln.ps1 Error Handling" {
    It "Should show error for non-existent source" {
        $source = "$testDir\nonexistent.txt"
        $link = "$testDir\link1.txt"
        
        { & $scriptPath $source $link } | Should -Throw
    }

    It "Should show error when no arguments provided" {
        { & $scriptPath 2>&1 } | Should -Throw
    }
}

AfterAll {
    # 清理测试环境
    Remove-Item -Path $testDir -Recurse -Force -ErrorAction SilentlyContinue
}