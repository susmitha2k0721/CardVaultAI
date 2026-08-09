import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import os
from datetime import datetime

from database.database import (
    get_scan_history,
    clear_scan_history,
    delete_scan_history
)

class HistoryPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=20,
            pady=20
        )
        title = ctk.CTkLabel(
            header,
            text="📜 Scan History",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(side="left")
        ctk.CTkButton(
            header,
            text="🗑 Clear History",
            fg_color="red",
            hover_color="#B91C1C",
            command=self.clear_history
        ).pack(side="right")

        self.history_frame = ctk.CTkScrollableFrame(
            self
        )

        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_history()

    def load_history(self):

        # Clear old history cards
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        rows = get_scan_history()

        if not rows:
            ctk.CTkLabel(
                self.history_frame,
                text="No Scan History Available",
                font=("Segoe UI", 16)
            ).pack(pady=30)
            return

        for row in rows:

            # Skip empty history records
            if not row[1]:
                continue

            card = ctk.CTkFrame(
                self.history_frame,
                corner_radius=12,
                border_width=1,
                border_color="#D1D5DB"
            )

            card.pack(fill="x", padx=10, pady=8)

            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=15)

            # Left: Thumbnail
            left = ctk.CTkFrame(content, width=140, height=90)
            left.pack(side="left", padx=(0, 15))
            left.pack_propagate(False)

            if row[2] and os.path.exists(row[2]):
                img = Image.open(row[2])
                img.thumbnail((120, 80))
                photo = ImageTk.PhotoImage(img)

                img_label = tk.Label(left, image=photo)
                img_label.image = photo
                img_label.pack(expand=True)
            else:
                ctk.CTkLabel(left, text="No Image").pack(expand=True)

            # Right: Details
            right = ctk.CTkFrame(content, fg_color="transparent")
            right.pack(side="left", fill="both", expand=True)

            formatted_date = datetime.strptime(
                row[4],
                "%Y-%m-%d %H:%M:%S"
            ).strftime("%d %b %Y   %I:%M %p")

            ctk.CTkLabel(
                right,
                text=row[1],
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                right,
                text=f"📅 {formatted_date}",
                font=("Segoe UI", 14)
            ).pack(anchor="w", pady=(5, 15))

            button_frame = ctk.CTkFrame(right, fg_color="transparent")
            button_frame.pack(anchor="w")

            ctk.CTkButton(
                button_frame,
                text="👁 View Scan",
                width=120,
                command=lambda r=row: self.view_scan(r)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                button_frame,
                text="🗑 Delete",
                width=100,
                fg_color="red",
                command=lambda sid=row[0]: self.delete_history_item(sid)
            ).pack(side="left", padx=5)
    def clear_history(self):
        answer = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all scan history?"
        )

        if answer:

            clear_scan_history()

            messagebox.showinfo(
                "Success",
                "Scan History Cleared Successfully."
            )

        # Reload history
            self.load_history()
    def delete_history_item(self, scan_id):

        answer = messagebox.askyesno(
            "Delete Scan",
            "Are you sure you want to delete this scan history item?"
        )

        if answer:

            delete_scan_history(scan_id)

            messagebox.showinfo(
                "Success",
                "Scan history deleted successfully."
            )

            self.load_history()
    def view_scan(self, row):

        window = tk.Toplevel(self)
        window.title("Scanned Card")
        window.geometry("900x600")

        title = tk.Label(
            window,
            text="Scanned Card Details",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=10)

        main = tk.Frame(window)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Left side - Image
        left = tk.Frame(main)
        left.pack(side="left", padx=20)

        if row[2] and os.path.exists(row[2]):

            img = Image.open(row[2])
            img.thumbnail((350, 250))

            photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(left, image=photo)
            img_label.image = photo
            img_label.pack()

        else:

            tk.Label(
                left,
                text="No Image Available"
            ).pack()

        # Right side - OCR
        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        formatted_date = datetime.strptime(
            row[4],
            "%Y-%m-%d %H:%M:%S"
            ).strftime("%d %b %Y   %I:%M %p")

        tk.Label(
            right,
            text=f"👤 {row[1]}",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            right,
            text=f"📅 {formatted_date}",
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(0,10))

        tk.Label(
            right,
            text="OCR Extracted Text",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        text_box = tk.Text(
            right,
            width=45,
            height=20,
            wrap="word"
        )

        text_box.pack(fill="both", expand=True)

        text_box.insert("1.0", row[3])

        text_box.config(state="disabled")

        tk.Button(
            window,
            text="Close",
            command=window.destroy
        ).pack(pady=10)