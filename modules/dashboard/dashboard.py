import customtkinter as ctk
from database.database import (
    get_total_contacts,
    get_total_scans,
    get_recent_contacts,
    get_today_scans,
    get_duplicate_count
)
from database.database import export_contacts_excel
from tkinter import messagebox

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # =========================
        # Header
        # =========================

        # ==================================
        # TOP HEADER BAR
        # ==================================

        top_bar = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=12
        )
        top_bar.pack(fill="x", padx=20, pady=(15, 10))
        title = ctk.CTkLabel(
            top_bar,
            text="📊 Dashboard",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(side="left", padx=20, pady=15)
        profile_frame = ctk.CTkFrame(
            top_bar,
            fg_color="transparent"
        )
        profile_frame.pack(side="right", padx=20)
        ctk.CTkButton(
            profile_frame,
            text="🔔",
            width=40,
            command=lambda: messagebox.showinfo(
                "Notifications",
                "No new notifications."
            )
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            profile_frame,
            text="⚙",
            width=40,
            command=lambda: self.app.show_page("settings")
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            profile_frame,
            text="👤",
            width=40,
            command=lambda: messagebox.showinfo(
                "Profile",
                "Name: Susmitha\nApplication: CardVault AI\nVersion: 1.0"
            )
        ).pack(side="left", padx=5)
        banner = ctk.CTkFrame(
            self,
            height=120
        )
        banner.pack(
            fill="x",
            padx=20,
            pady=10
        )
        welcome = ctk.CTkLabel(
            banner,
            text="Welcome Back, Susmitha 👋",
            font=("Segoe UI", 26, "bold")
        )
        welcome.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )
        message = ctk.CTkLabel(
            banner,
            text="Manage business cards with intelligent OCR and analytics.",
            font=("Segoe UI", 14)
        )
        message.pack(
            anchor="w",
            padx=20
        )
        total_contacts = get_total_contacts()
        total_scans = get_total_scans()
        today_scans = get_today_scans()
        recent_contacts = get_recent_contacts()
        duplicates = get_duplicate_count()

        # =========================
        # Statistics Cards
        # =========================

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=15)

        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.contacts_value = self.create_card(
            cards_frame, 0, "👥 Contacts", str(total_contacts)
        )

        self.scans_value = self.create_card(
            cards_frame, 1, "📷 Scans", str(total_scans)
        )

        self.duplicates_value = self.create_card(
            cards_frame,
            2,
            "⚠ Duplicates",
            str(duplicates)
        )
        self.today_value = self.create_card(
            cards_frame, 3, "📅 Today", str(today_scans)
        )

        # =========================
        # Main Section
        # =========================

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)

        # Quick Actions

        quick_actions = ctk.CTkFrame(content_frame)
        quick_actions.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        quick_title = ctk.CTkLabel(
            quick_actions,
            text="⚡ Quick Actions",
            font=("Segoe UI", 20, "bold")
        )
        quick_title.pack(anchor="w", padx=20, pady=15)

        ctk.CTkButton(
            quick_actions,
            text="📷 Scan New Card",
            height=40,
            command=lambda: self.app.show_page("scanner")
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            quick_actions,
            text="👥 View Contacts",
            height=40,
            command=lambda: self.app.show_page("contacts")
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            quick_actions,
            text="📤 Export Data",
            height=40,
            command=export_contacts_excel
        ).pack(fill="x", padx=20, pady=8)

        # Recent Activity

        self.activity_frame = ctk.CTkFrame(content_frame)
        self.activity_frame.grid(row=0, column=1, sticky="nsew")

        activity_title = ctk.CTkLabel(
            self.activity_frame,
            text="👥 Recent Contacts",
            font=("Segoe UI", 20, "bold")
        )
        activity_title.pack(anchor="w", padx=20, pady=15)
        for contact in recent_contacts:
            label = ctk.CTkLabel(
                self.activity_frame,
                text=f"👤 {contact[0]}",
                anchor="w",
                font=("Segoe UI", 14)
            )
            label.pack(
                fill="x",
                padx=20,
                pady=5
            )
        

    def create_card(self, parent, column, title, value):

        card = ctk.CTkFrame(parent, height=120)

        card.grid(
            row=0,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(20, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold")
        )
        value_label.pack()

        return value_label
        
    def refresh_dashboard(self):

        total_contacts = get_total_contacts()
        total_scans = get_total_scans()
        today_scans = get_today_scans()
        duplicates = get_duplicate_count()
        recent_contacts = get_recent_contacts()

        self.contacts_value.configure(text=str(total_contacts))
        self.scans_value.configure(text=str(total_scans))
        self.duplicates_value.configure(text=str(duplicates))
        self.today_value.configure(text=str(today_scans))

        # Refresh Recent Contacts
        for widget in self.activity_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.activity_frame,
            text="👥 Recent Contacts",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=15)

        for contact in recent_contacts:
            ctk.CTkLabel(
                self.activity_frame,
                text=f"👤 {contact[0]}",
                anchor="w",
                font=("Segoe UI", 14)
            ).pack(fill="x", padx=20, pady=5)