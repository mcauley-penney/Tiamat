# Developing and Running Tiamat

## Activating the Extension
1. The extension must be listed and enabled in the `config-extensions.def` file in `idlelib`, e.g. `/usr/lib/python3.12/idlelib/config-extensions.def`. The below text snippet should provide this:

```
[Tiamat]
enable= True
```

2. The extension must then be activated through IDLE. In IDLE, navigate `window` -> `Extensions`. The extension should be listed there. If so, click the `enable` button. If not, there is a likely an issue with step 1 above.
3. The extension will not work without starting its backend, which is currently DocGPT. See the DocGPT documentation for this.
4. IDLE should be restarted for all of this to function together. Close out of IDLE and reopen it.
