# TODO:
# 1. Init conversational ability
#   - make it async, nonblocking
# 2. messages must be tracked and used as context
# 3. Panel should be responsive to main window
#   - color
#   - font
#   - toggle panel visibility
#
# Path:
# 1. connect agent
# 2. work on conversational ability


import aiohttp
import asyncio
from concurrent.futures import Future
import threading
import tkinter as tk


ENDPOINT = "http://127.0.0.1:8000/v1/assistant/prompt"
SYSTEM_PROMPT = ""


async def async_post(url, payload, headers):
    """Asynchronously send a POST request to the specified URL with the given payload."""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            data = await response.json()
            return data


class Tiamat:
    def __init__(self, editwin):
        self.editwin = editwin
        self.history = []

        self.async_loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.async_loop,))
        self.thread.start()

        self.init_widgets()

        # TODO: check health of assistant to make sure we may continue
        #  self.check_assistant_health()

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def init_widgets(self):
        self.panel = tk.Frame(self.editwin.top, bg="white")
        self.panel.pack(side="left", fill="y", expand=False, padx=(0, 0), pady=(0, 0))

        self.feed_box = tk.Frame(self.panel, borderwidth=2, relief="sunken")
        self.feed_box.pack(side="bottom", fill="x", padx=5, pady=5)

        self.msgfeed = tk.Text(
            self.panel,
            state="disabled",
            height=20,
            width=50,
            borderwidth=2,
            relief="sunken",
        )
        self.msgfeed.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.input_box = tk.Text(
            self.feed_box, height=2, width=50, borderwidth=0, highlightthickness=0
        )
        self.input_box.pack(side="left", fill="both", expand=True, padx=0, pady=1)
        self.input_box.bind("<Return>", self.handle_user_input)

        self.submit_btn = tk.Button(
            self.feed_box,
            command=self.handle_user_input,
            text="",
            background="white",
            height=2,
            width=1,
            foreground="gray",
            highlightcolor="white",
            highlightbackground="white",
            cursor="hand2",
            relief=tk.FLAT,
            font=("Arial", 30, "bold"),
        )
        self.submit_btn.pack(side="right", padx=0, pady=1)

    def handle_user_input(self, event=None):
        user_input = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)

        if user_input:
            coroutine = self.query_assistant(user_input)
            future = asyncio.run_coroutine_threadsafe(coroutine, self.async_loop)
            future.add_done_callback(self.handle_result)

        # prevent the default behavior of inserting a newline on return key press
        return "break"

    async def query_assistant(self, msg):
        payload = {"message": msg, "session_id": "IDLE"}
        headers = {"Content-Type": "application/json"}

        post_task = asyncio.create_task(async_post(ENDPOINT, payload, headers))

        self.history.append(("User", msg))
        self.print_msg("You", msg)

        response = await post_task

        answer: str = response["answer"]
        # check the response (optional)
        if answer is not None:
            print("Success:", answer)
            return answer
        else:
            print("An error occurred:", None)
            return None
    
    # This Function is not yet finished, and is not yet used
    # Function to send the system message to guardrail the responses
    async def system_query(self, msg):
        # set up the message structure
        payload = {"message": msg, "session_id": "IDLE"}
        headers = {"Content-Type": "application/json"}

        post_task = asyncio.create_task(async_post(ENDPOINT, payload, headers))
        
        # append the system message to the message history
        self.history.append(("System", msg))
        
        response = await post_task
        
        # may need to remove? Don't know exactly if we are expecting a response
        # for the system message,
        answer: str = response["answer"]
        # check the response (optional)
        if answer is not None:
            print("Success:", answer)
            return answer
        else:
            print("An error occurred:", None)
            return None


    def handle_result(self, future):
        response = future.result()

        if response is None:
            print("ERROR: no response!")
        else:
            self.history.append(("Assistant", response))
            self.print_msg("Assistant", response)

    def print_msg(self, speaker, msg):
        msg = f"{speaker}\n{msg}\n\n"
        print(msg)

        self.msgfeed.config(state="normal")
        self.msgfeed.insert(tk.END, msg)

        self.msgfeed.config(state="disabled")
        self.msgfeed.see(tk.END)


#  from idlelib.config import idleConf

#  def show_sidebar(self):
#      if not self.is_shown:
#          self.grid()
#          self.is_shown = True

#  def hide_sidebar(self):
#      if self.is_shown:
#          self.main_widget.grid_forget()
#          self.is_shown = False

#  def update_font(self):
#      font = idleConf.GetFont(self.text, "main", "EditorWindow")
#      self.sidebar_text["font"] = font

#  def update_colors(self):
#      """Update the sidebar text colors, usually after config changes."""
#      colors = idleConf.GetHighlight(idleConf.CurrentTheme(), "linenumber")
#      foreground = colors["foreground"]
#      background = colors["background"]
#      self.sidebar_text.config(
#          fg=foreground,
#          bg=background,
#          selectforeground=foreground,
#          selectbackground=background,
#          inactiveselectbackground=background,
#      )
