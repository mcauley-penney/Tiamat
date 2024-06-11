# Developing and Running the Extension

## Setting up IDLE to Use the Extension

1. The extension must be listed and enabled in the `config-extensions.def` file in `idlelib`, e.g. `/usr/lib/python3.12/idlelib/config-extensions.def`. The below text snippet should provide this:

```
[Tiamat]
enable= True
```

2. The extension must then be activated through IDLE. In IDLE, navigate `window` -> `Extensions`. The extension should be listed there. If so, click the `enable` button. If not, there is a likely an issue with step 1 above.
1. The extension will not work without starting its backend, which is currently DocGPT. See the DocGPT documentation for this.
1. IDLE should be restarted for all of this to function together. Close out of IDLE and reopen it.

### Gotchas

1. the idlelib is per-interpreter. If you have multiple versions of Python installed, you need to make sure that your third-party libraries are installed for the version you want to use, that the extension is placed in the correct idlelib, and that you are using the correct IDLE version. For example, if you want to use 3.12 and have 3.11 installed as well, make sure that aiohttp is installed for 3.12, Tiamat is in 3.12's idlelib, and that you are using the IDLE executable that corresponds to 3.12.

## Starting the Extension

1. Start the docker containers for DocGPT
1. Start DocGPT
1. with the extension already activated in IDLE's settings, Start IDLE
