# Resources for Developing in IDLE

## IDLE
### Internal Docs
1. how to write an extension module with an extension class: /usr/lib/python3.11/idlelib/extend.txt
2. an incomplete example extension module, with an example ZzDummy class: /usr/lib/python3.11/idlelib/zzdummy.py

### External Docs
1. https://docs.python.org/3/library/idle.html#extensions
2. https://realpython.com/python-idle/
3. https://idlex.sourceforge.net
4. https://stackoverflow.com/questions/65567057/how-can-i-get-started-developing-extensions-for-python-idle
5. https://stackoverflow.com/questions/77345697/making-extension-for-idle-to-change-its-right-click-menu


## TKinter
IDLE's GUI is done through tkinter.

### Customization
tkinter itself is highly configurable but is basic; you may have to put in a lot of work for an appearance. tkinter's `ttk` submodule uses styles to define how widgets look, so it may also take some work.

ttkbootstrap exists, which provides bootstrappable aesthetics
See
  1. https://www.youtube.com/watch?v=0tM-l_ZsxjU&t=5996s
  2. https://ttkbootstrap.readthedocs.io/en/latest/


## DocGPT
### Setup
- install dependencies using Poetry
- build database using `sudo docker-compose up`
  - if you receive an error related to `veth`, restart your machine
  - after running this, the docker container should be setup but also running. Leave it running

- put your tokens in `.env.example` and move the file to `.env`
  - OPENAI tokens are from Nich

- run `fetch_documents()` only on the first run to populate the database
  - You need to set up SSH keys in GitHub to actually fetch documents
    - Create SSH keys on your maching, give key to GitHub in settings

- then, uncomment only `run_api()` in main.py, so that the API gets up and running for clients

### API
- With the server running, see docs at http://127.0.0.1:8000/docs
