"""TODO."""

import asyncio
import threading
import tkinter as tk
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
        panel = tk.Frame(self.editwin.top, bg="white")
        panel.pack(side="left", fill="y", expand=False, padx=(0, 0), pady=(0, 0))

        self.feed_box = tk.Frame(panel, borderwidth=2, relief="sunken")
        self.feed_box.pack(side="bottom", fill="x", padx=5, pady=5)

        self.msgfeed = tk.Text(
            panel,
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

        submit_btn = tk.Button(
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
        submit_btn.pack(side="right", padx=0, pady=1)

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
        payload = {"message": msg, "session_id": "IDLE"}
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

        self.msgfeed.config(state="normal")
        self.msgfeed.insert(tk.END, msg)

        self.msgfeed.config(state="disabled")
        self.msgfeed.see(tk.END)
