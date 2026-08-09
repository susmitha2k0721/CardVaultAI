import customtkinter as ctk
import os
from tkinter import messagebox
from database.database import clear_scan_history
import shutil
from tkinter import filedialog

class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Segoe UI", 28, "bold")
        ).pack(anchor="w", padx=20, pady=20)

        # Appearance
        appearance = ctk.CTkFrame(self)
        appearance.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            appearance,
            text="Appearance",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=15, pady=10)

        ctk.CTkOptionMenu(
            appearance,
            values=["Light", "Dark"],
            command=self.change_theme
        ).pack(anchor="w", padx=15, pady=10)

        # Application
        app_frame = ctk.CTkFrame(self)
        app_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            app_frame,
            text="Application",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=15, pady=10)

        ctk.CTkButton(
            app_frame,
            text="📂 Open Export Folder",
            command=self.open_exports
        ).pack(anchor="w", padx=15, pady=5)

        ctk.CTkButton(
            app_frame,
            text="🗑 Clear Scan History",
            fg_color="red",
            command=self.clear_history
        ).pack(anchor="w", padx=15, pady=5)
        ctk.CTkButton(
            app_frame,
            text="💾 Backup Database",
            command=self.backup_database
        ).pack(anchor="w", padx=15, pady=5)

        ctk.CTkButton(
            app_frame,
            text="📥 Restore Database",
            command=self.restore_database
        ).pack(anchor="w", padx=15, pady=5)

        # About
        about = ctk.CTkFrame(self)
        about.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            about,
            text="About",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=15, pady=10)

        ctk.CTkLabel(
            about,
            text="CardVault AI\nVersion 1.0\nDeveloped by Susmitha",
            justify="left"
        ).pack(anchor="w", padx=15, pady=10)

    def change_theme(self, mode):

        if mode == "Dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def open_exports(self):

        os.startfile("exports")

    def clear_history(self):

        answer = messagebox.askyesno(
            "Clear History",
            "Delete all scan history?"
        )

        if answer:

            clear_scan_history()

            messagebox.showinfo(
                "Success",
                "History cleared successfully."
            )
    def backup_database(self):

        destination = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database Files", "*.db")],
            initialfile="cardvault_backup.db"
        )

        if destination:

            shutil.copy(
                "database/cardvault.db",
                destination
            )

            messagebox.showinfo(
                "Backup Successful",
                "Database backup created successfully."
            )
    def restore_database(self):

        source = filedialog.askopenfilename(
            filetypes=[("Database Files", "*.db")]
        )

        if source:

            shutil.copy(
                source,
                "database/cardvault.db"
            )

            messagebox.showinfo(
                "Restore Successful",
                "Database restored successfully.\nPlease restart CardVault AI."
            )