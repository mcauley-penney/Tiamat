"""TODO."""

import asyncio
import threading
import tkinter as tk
from tkinter import ttk
import aiohttp


ENDPOINT = "http://127.0.0.1:8000/v1/assistant/prompt"

async def async_post(url, payload, headers):
    """Asynchronously send a POST request to the specified URL with the given payload."""
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            data = await response.json()
            return data


class Tiamat:
    """TODO."""

    def __init__(self, editwin):
        self.editwin = editwin
        self.history = []

        self.async_loop = asyncio.new_event_loop()

        thread = threading.Thread(target=self.start_loop, args=(self.async_loop,))
        thread.start()

        self.init_widgets()

    def start_loop(self, loop):
        """TODO."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def init_widgets(self):
        """TODO."""

        panel = ttk.Frame(self.editwin.top, style="TFrame")
        panel.pack(side="left", fill="y", expand=False, padx=(0, 0), pady=(0, 0))

        self.top_bar = ttk.Frame(panel, style="TFrame")
        self.top_bar.pack(side="top", fill="x", padx=5, pady=5)

        self.title = ttk.Label(self.top_bar, style="TLabel", text="Tiamat", justify=tk.LEFT, font="Arial")
        self.title.pack(side="left", fill="x")

        self.feed_box = ttk.Frame(panel, style="TFrame")
        self.feed_box.pack(side="bottom", fill="x", padx=5, pady=5)

        self.msg_canvas = tk.Canvas(panel)
        self.msg_canvas.pack(side="left", fill="both", expand=True)

        self.msg_scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.msg_canvas.yview)
        self.msg_scrollbar.pack(side="right", fill="y")

        self.msg_canvas.configure(yscrollcommand=self.msg_scrollbar.set)

        self.messages_frame = ttk.Frame(self.msg_canvas)
        self.msg_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")


        self.msg_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.input_box = tk.Text(
            self.feed_box, 
            height=4, 
            width=50,
            padx=5,
            pady=5, 
            borderwidth=0, 
            highlightthickness=0, 
            wrap="word", 
            font="Arial 12"
        )
        self.input_box.pack(side="left", fill="both", expand=True, padx=0, pady=1)
        self.input_box.bind("<Return>", self.handle_user_input)

        submit_btn = ttk.Button(
            self.feed_box,
            command=self.handle_user_input,
            text="Send",
            padding=(10, 20),
            style="SendButton.TButton"
        )
        submit_btn.pack(side="right", padx=0, pady=1)

    def _on_mouse_wheel(self, event):
        self.msg_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def handle_user_input(self, event=None):
        """TODO."""
        user_input = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)

        if user_input:
            coroutine = self.query_assistant(user_input)
            future = asyncio.run_coroutine_threadsafe(coroutine, self.async_loop)
            future.add_done_callback(self.handle_result)

        # prevent the default behavior of inserting a newline on return key press
        return "break"

    async def query_assistant(self, msg):
        """TODO."""
        payload = {"message": msg, "session_id": "test"}
        headers = {"Content-Type": "application/json"}

        post_task = asyncio.create_task(async_post(ENDPOINT, payload, headers))

        self.history.append(("User", msg))
        self.print_msg("You", msg)

        response = await post_task
        answer: str = response["answer"]

        return answer

    def handle_result(self, future):
        """TODO."""
        response = future.result()

        if response is None:
            print("ERROR: no response!")
        else:
            self.history.append(("Assistant", response))
            self.print_msg("Assistant", response)

    def print_msg(self, speaker, msg):
        """TODO."""
        msg = f"{speaker}\n{msg}\n\n"
        print(msg)

        if speaker == "You":
            msg_background = "#5c8bd6"
            msg_foreground = "#ffffff"
        else:
            msg_background = "#afb9c9"
            msg_foreground = "#000000"

        label = ttk.Label(self.messages_frame, text=msg, width=-50, wraplength=400, padding=(5, 5), font="Arial 12", background=msg_background, foreground=msg_foreground)
        label.pack(side="top", fill="none", pady=5)

        self.messages_frame.update_idletasks()
        self.msg_canvas.config(scrollregion=self.msg_canvas.bbox("all"))
        self.msg_canvas.yview_moveto(1)
