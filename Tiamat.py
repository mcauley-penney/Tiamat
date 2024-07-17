"""TODO."""

import asyncio
import threading
import tkinter as tk
import tkinter.ttk as ttk
from idlelib.config import idleConf
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

        self.main_font = (
            idleConf.GetOption("main", "EditorWindow", "font"),
            idleConf.GetOption("main", "EditorWindow", "font-size"),
        )
        self.theme = idleConf.GetOption("main", "Theme", "name2") or idleConf.GetOption(
            "main", "Theme", "name"
        )
        self.normal_background = idleConf.GetOption(
            "highlight", self.theme, "normal-background"
        )
        self.normal_foreground = idleConf.GetOption(
            "highlight", self.theme, "normal-foreground"
        )
        self.secondary_bg = idleConf.GetOption(
            "highlight", self.theme, "hilite-background"
        )
        self.secondary_fg = idleConf.GetOption(
            "highlight", self.theme, "hilite-foreground"
        )

        thread = threading.Thread(target=self.start_loop, args=(self.async_loop,))
        thread.start()

        self.init_widgets()

    def start_loop(self, loop):
        """TODO."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def init_widgets(self):
        """TODO."""
        panel = tk.Frame(self.editwin.top)
        panel.pack(side="left", fill="y", expand=False, padx=(0, 0), pady=(0, 0))

        self.top_bar = tk.Frame(panel, padx=5, pady=5)
        self.top_bar.pack(side="top", fill="x")

        self.title = ttk.Label(
            self.top_bar, text="Tiamat", justify=tk.LEFT, font=self.main_font
        )
        self.title.pack(side="left", fill="x")

        self.feed_box = tk.Frame(panel)
        self.feed_box.pack(side="bottom", fill="x")

        self.msg_canvas = tk.Canvas(panel, background=self.normal_background)
        self.msg_canvas.pack(side="left", fill="both", expand=True)

        self.msg_scrollbar = ttk.Scrollbar(
            panel, orient="vertical", command=self.msg_canvas.yview
        )
        self.msg_scrollbar.pack(side="right", fill="y")

        self.msg_canvas.configure(yscrollcommand=self.msg_scrollbar.set)

        self.messages_frame = tk.Frame(
            self.msg_canvas, background=self.normal_background, padx=10, pady=10
        )
        self.msg_window_id = self.msg_canvas.create_window(
            (0, 0), window=self.messages_frame, anchor="nw"
        )

        self.thinking_text = ttk.Label(
            self.messages_frame,
            background=self.normal_background,
            foreground=self.normal_foreground,
            font=(self.main_font[0], self.main_font[1], "italic"),
            text="Assistant is typing...",
            justify="left",
        )

        self.msg_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.msg_canvas.bind("<Configure>", self._on_canvas_resize)

        self.input_box = tk.Text(
            self.feed_box,
            height=4,
            width=50,
            padx=5,
            pady=5,
            borderwidth=0,
            highlightthickness=0,
            wrap="word",
            font=self.main_font,
            background=self.normal_background,
            foreground=self.normal_foreground,
        )
        self.input_box.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.input_box.bind("<Return>", self.handle_user_input)

        submit_btn = tk.Button(
            self.feed_box,
            command=self.handle_user_input,
            text="Send",
            padx=5,
            pady=5,
            background=self.normal_background,
            foreground=self.normal_foreground,
            font=self.main_font,
        )
        submit_btn.pack(side="right", padx=2, pady=0)

    def _on_mouse_wheel(self, event):
        self.msg_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_canvas_resize(self, event):
        self.msg_canvas.itemconfig(self.msg_window_id, width=event.width - 5)

    def show_thinking_text(self):
        self.thinking_text.pack(side="bottom", padx=5, pady=5, anchor="w")

    def hide_thinking_text(self):
        self.thinking_text.pack_forget()

    def handle_user_input(self, event=None):
        """TODO."""
        user_input = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)
        self.show_thinking_text()

        if user_input:
            coroutine = self.query_assistant(user_input)
            future = asyncio.run_coroutine_threadsafe(coroutine, self.async_loop)
            future.add_done_callback(self.handle_result)

        # prevent the default behavior of inserting a newline on return key press
        return "break"

    async def query_assistant(self, msg):
        """TODO."""
        payload = {"message": msg, "session_id": "test2"}
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
        self.hide_thinking_text()

        if response is None:
            print("ERROR: no response!")
        else:
            self.history.append(("Assistant", response))
            self.print_msg("Assistant", response)

    def print_msg(self, speaker, msg):
        """TODO."""
        msg = f"{speaker}\n{msg}\n\n"
        print(msg)

        outer_frame = tk.Frame(self.messages_frame, background=self.normal_background)
        outer_frame.pack(fill="x", padx=5, pady=5, expand=False)

        if speaker == "You":
            msg_background = "#5c8bd6"
            msg_foreground = "#ffffff"
            side = "e"
        else:
            msg_background = self.secondary_bg
            msg_foreground = self.secondary_fg
            side = "w"

        label = ttk.Label(
            outer_frame,
            text=msg,
            width=-40,
            padding=(5, 5),
            font=self.main_font,
            background=msg_background,
            foreground=msg_foreground,
            borderwidth=1,
            relief="solid",
        )
        label.pack(fill="none", anchor=side)

        self.messages_frame.update_idletasks()
        label.configure(wraplength=label.winfo_width() - 10)

        self.messages_frame.update_idletasks()
        self.msg_canvas.config(scrollregion=self.msg_canvas.bbox("all"))
        self.msg_canvas.yview_moveto(1)
