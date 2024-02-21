REM Install Git and update Scoop buckets
::Install Git and update Scoop buckets
scoop bucket add versions
scoop bucket add extras
scoop install git
scoop install main/gh
scoop install versions/windows-terminal-preview
scoop update


::Set desktop target and PATH additions (using Environment Variables)
$desktop = "C:\Users\WDAGUtilityAccount\Desktop"
$env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User")
$env:PATH += ";$desktop\micromamba;$desktop\Scoop\bin"

::Define the RunCommand function
function RunCommand($command) {
    Write-Host "Running command: $command"
    Invoke-Expression $command
}

::Install required packages
RunCommand "scoop install extras/mambaforge"
RunCommand "scoop install extras/okular"
RunCommand "scoop install extras/irfanview-lean"
RunCommand "scoop install extras/mpc-hc-fork"
RunCommand "scoop install main/sourcegraph-cli"
RunCommand "scoop install main/frp"
RunCommand "scoop install extras/carapace-bin"
RunCommand "scoop install versions/vscode-insiders"
RunCommand "scoop install main/yq"
RunCommand "scoop install main/jc"
RunCommand "scoop install main/eza"
RunCommand "scoop install extras/chatall"
RunCommand "scoop install main/fq"
RunCommand "scoop install main/zoxide"
RunCommand "scoop install main/nu"
RunCommand "scoop install main/windows-application-driver"
RunCommand "scoop install extras/texteditorpro"
RunCommand "scoop install main/miller"
RunCommand "scoop install main/clink"
RunCommand "scoop install main/clink-flex-prompt"
RunCommand "scoop bucket add nerd-fonts"
RunCommand "scoop install nerd-fonts/FiraMono-NF-Mono"
RunCommand "scoop install nerd-fonts/FiraCode-NF"
RunCommand "scoop install main/fx"
RunCommand "scoop install main/yedit"
RunCommand "scoop install main/bison"
RunCommand "scoop install main/hurl"
RunCommand "scoop install main/fselect"
RunCommand "scoop install main/rcc"
RunCommand "scoop install main/cheat"
RunCommand "scoop install main/navi"
::conclude scooping - left out (for space/time): msys2, chromedriver, googlechrome-canary, mingw, Selenium, x64dbg, gcc, caddy, ghidra
REM RunCommand "scoop install extras/ghidra"
REM RunCommand "scoop install extras/x64dbg"
REM RunCommand "scoop install extras/extraterm"
REM RunCommand "scoop install main/chromedriver"
REM RunCommand "scoop install versions/googlechrome-canary"
REM RunCommand "scoop install main/selenium"
REM RunCommand "scoop install main/caddy"
REM RunCommand "scoop install main/gcc"

$env:PATH += ";$desktopPath\micromamba;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User");

::Launch common applications
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
Start-Process "notepad.exe"
Start-Process "explorer.exe"
try {
    Start-Process "wt.exe" -Wait
} catch {
    Start-Process "powershell.exe"
}