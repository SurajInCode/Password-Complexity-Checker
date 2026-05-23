# Password strength checker / evaluator by Suraj
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import pyperclip

from checker import PasswordAnalysis, evaluate_password_strength, generate_password

ICON_PATH = Path(__file__).resolve().parent / "files" / "pic.ico"
DEBOUNCE_MS = 200


class PasswordApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._debounce_after_id: str | None = None
        self._setup_window()
        self._configure_styles()
        self._build_widgets()
        self._bind_events()

    def _setup_window(self) -> None:
        self.root.title("Password Strength Evaluator")
        self.root.geometry("650x480")
        self.root.configure(bg="#212121")
        if ICON_PATH.is_file():
            try:
                self.root.iconbitmap(ICON_PATH)
            except tk.TclError:
                pass

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("default")
        style.configure(
            "Blue.Horizontal.TProgressbar",
            troughcolor="#333333",
            background="#1E90FF",
        )
        style.configure(
            "Red.Horizontal.TProgressbar",
            troughcolor="#333333",
            background="#FF073A",
        )
        style.configure(
            "Orange.Horizontal.TProgressbar",
            troughcolor="#333333",
            background="#FFA500",
        )
        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor="#333333",
            background="#39FF14",
        )

    def _build_widgets(self) -> None:
        self.main_frame = tk.Frame(self.root, bg="#212121")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        label_pwd = tk.Label(
            self.main_frame,
            text="Enter the password:",
            bg="#212121",
            fg="white",
            font=("Helvetica", 14),
        )
        label_pwd.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        self.entry_pwd = tk.Entry(
            self.main_frame,
            show="*",
            font=("Helvetica", 12),
            bg="#333333",
            fg="white",
            insertbackground="white",
        )
        self.entry_pwd.grid(row=0, column=1, padx=5, pady=5, sticky="we", columnspan=2)

        self.toggle_btn = tk.Button(
            self.main_frame,
            text="Show",
            command=self._toggle_password_visibility,
            bg="#8A2BE2",
            fg="black",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            borderwidth=2,
        )
        self.toggle_btn.grid(row=0, column=3, padx=5, pady=5, sticky="we")

        self.btn_check = tk.Button(
            self.main_frame,
            text="Check",
            command=self.verify_password,
            bg="#39FF14",
            fg="black",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            borderwidth=2,
        )
        self.btn_check.grid(row=1, column=0, pady=10, padx=5, sticky="we")

        self.btn_generate = tk.Button(
            self.main_frame,
            text="Generate Password",
            command=self._generate_password,
            bg="#1E90FF",
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            borderwidth=2,
        )
        self.btn_generate.grid(row=1, column=1, pady=10, padx=5, sticky="we")

        self.btn_copy = tk.Button(
            self.main_frame,
            text="Copy Password",
            command=self._copy_to_clipboard,
            bg="#FFFF33",
            fg="black",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            borderwidth=2,
        )
        self.btn_copy.grid(row=1, column=2, pady=10, padx=5, sticky="we")

        self.btn_clear = tk.Button(
            self.main_frame,
            text="Clear",
            command=self._clear_entry,
            bg="#FF073A",
            fg="black",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT,
            borderwidth=2,
        )
        self.btn_clear.grid(row=1, column=3, pady=10, padx=5, sticky="we")

        self.text_output = tk.Text(
            self.main_frame,
            height=10,
            width=60,
            state="disabled",
            font=("Helvetica", 10),
            bg="#333333",
            fg="white",
            relief=tk.FLAT,
            borderwidth=2,
        )
        self.text_output.grid(row=2, column=0, columnspan=4, pady=10)

        self.progress_meter = ttk.Progressbar(
            self.main_frame,
            orient=tk.HORIZONTAL,
            length=450,
            mode="determinate",
            value=0,
            maximum=100,
            style="Blue.Horizontal.TProgressbar",
        )
        self.progress_meter.grid(row=3, column=0, columnspan=4, pady=12)

        label_signature = tk.Label(
            self.root,
            text="By SurajInCode",
            font=("Helvetica", 12, "bold"),
            bg="#212121",
            fg="green",
        )
        label_signature.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

        self._add_hover_effects()

    def _add_hover_effects(self) -> None:
        buttons = [
            (self.btn_check, "#39FF14", "#7CFC00"),
            (self.btn_generate, "#1E90FF", "#00BFFF"),
            (self.btn_copy, "#FFFF33", "#FFD700"),
            (self.btn_clear, "#FF073A", "#FF6347"),
            (self.toggle_btn, "#8A2BE2", "#9370DB"),
        ]
        for btn, normal_color, glow_color in buttons:
            btn.bind(
                "<Enter>",
                lambda _e, b=btn, c=normal_color, g=glow_color: self._on_enter(b, c, g),
            )
            btn.bind(
                "<Leave>",
                lambda _e, b=btn, c=normal_color: self._on_leave(b, c),
            )

    def _bind_events(self) -> None:
        self.entry_pwd.bind("<KeyRelease>", self._on_key_release)

    def _on_key_release(self, _event: tk.Event) -> None:
        if self._debounce_after_id is not None:
            self.root.after_cancel(self._debounce_after_id)
        self._debounce_after_id = self.root.after(DEBOUNCE_MS, self.verify_password)

    def verify_password(self) -> None:
        analysis = evaluate_password_strength(self.entry_pwd.get())
        self._show_analysis(analysis)

    def _show_analysis(self, analysis: PasswordAnalysis) -> None:
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", analysis.report)
        self.text_output.config(state="disabled")

        self.progress_meter.configure(style=analysis.bar_style)
        self._animate_progress(analysis.progress, 0)

    def _generate_password(self) -> None:
        pwd = generate_password(length=16, use_specials=True)
        self.entry_pwd.delete(0, "end")
        self.entry_pwd.insert(0, pwd)
        self.verify_password()

    def _copy_to_clipboard(self) -> None:
        pwd = self.entry_pwd.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Nothing to copy", "Enter or generate a password first.")

    def _clear_entry(self) -> None:
        self.entry_pwd.delete(0, "end")
        self.verify_password()

    def _toggle_password_visibility(self) -> None:
        if self.entry_pwd.cget("show") == "":
            self.entry_pwd.config(show="*")
            self.toggle_btn.config(text="Show")
        else:
            self.entry_pwd.config(show="")
            self.toggle_btn.config(text="Hide")

    def _animate_progress(self, target: float, current: float) -> None:
        if abs(target - current) > 1:
            self.progress_meter["value"] = current
            step = (target - current) / 10
            self.root.after(
                50,
                lambda: self._animate_progress(target, current + step),
            )
        else:
            self.progress_meter["value"] = target

    @staticmethod
    def _on_enter(btn: tk.Button, color: str, glow_color: str) -> None:
        btn.configure(background=color, foreground=glow_color, borderwidth=2)

    @staticmethod
    def _on_leave(btn: tk.Button, color: str) -> None:
        btn.configure(background=color, foreground="black", borderwidth=2)


def main() -> None:
    root = tk.Tk()
    PasswordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
