# Application shortcut files that appear on the desktop
## Structure of a .desktop File
```
[Desktop Entry]
Type=Application
Name=Firefox Web Browser
Exec=firefox
Icon=firefox
Terminal=false

```
* use `chmod +x ~/Desktop/myapp.desktop`

## Other basics
* save .desktop file in ~/Desktop for making it available for desktop
* for making application shortcut to available in apps menu make .desktop file in `/usr/share/applications` for system-wide availability or `~/.local/share/applications` for user specific
* You can copy a .desktop file from these locations to your desktop to make them available in desktop
  * for system-wide launchers: /usr/share/applications/*.desktop

  * for user-specific launchers: ~/.local/share/applications/*.desktop


