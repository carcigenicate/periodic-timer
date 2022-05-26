# Description

A simple self-resetting timer to remind you to drink water (or to do some action other periodically). To alert you, it flashes the taskbar icon of an open PowerShell terminal (by default). The window type can be changed by changing `TARGET_WINDOW_NAME`. I may add the ability to specify that name as an argument later.

There are no dependencies. It currently only works on Windows though, as it relies on the Windows API. It should work on any version of Python that support type hints

# Usage:

```powershell
python main.py <Number of minutes. Defaults to 15>
```