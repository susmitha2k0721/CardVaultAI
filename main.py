import customtkinter as ctk

from modules.dashboard.dashboard import DashboardPage
from modules.scanner.scanner import ScannerPage
from modules.contacts.contacts import ContactsPage
from modules.history.history import HistoryPage
from modules.settings.settings import SettingsPage
from database.database import create_database


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class CardVaultAI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CardVault AI")
        self.geometry("1400x800")

        # Sidebar
        self.sidebar_width = 240
        self.sidebar = ctk.CTkFrame(
             self,
             width=self.sidebar_width,
             corner_radius=0,
             fg_color="#0F172A")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        header_frame = ctk.CTkFrame(
             self.sidebar,
             fg_color="transparent"
             )
        header_frame.pack(fill="x", pady=20)
        self.logo = ctk.CTkLabel(
             header_frame,
             text="🛡 CardVault AI",
             text_color="white",
             font=("Segoe UI", 22, "bold")
             )
        self.logo.pack(pady=10)
        self.toggle_btn = ctk.CTkButton(
             header_frame,
             text="☰",
             width=40,
             command=self.toggle_sidebar
             )
        self.toggle_btn.pack(pady=5)
        self.sidebar_expanded = True
        self.menu_buttons = {}

        # Menu Buttons
        menus = {
            "Dashboard": "dashboard",
            "Scan Card": "scanner",
            "Contacts": "contacts",
            "History": "history",
            "Settings": "settings"
            }
        for text, page in menus.items():
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45,
                fg_color="transparent",
                hover_color="#1E293B",
                anchor="w",
                text_color="white",
                command=lambda p=page: self.show_page(p)
                )
            btn.pack(fill="x", padx=10, pady=5)
            self.menu_buttons[page] = btn

        # Content Area
        self.content = ctk.CTkFrame(self)
        self.content.pack(side="right", fill="both", expand=True)

        # Pages
        self.pages = {
            "dashboard": DashboardPage(self.content,self),
            "scanner": ScannerPage(self.content),
            "contacts": ContactsPage(self.content),
            "history": HistoryPage(self.content),
            "settings": SettingsPage(self.content),
        }

        self.show_page("dashboard")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()
            # Refresh pages when they are opened
            if page_name == "dashboard":
                self.pages["dashboard"].refresh_dashboard()

            if page_name == "history":
                self.pages["history"].load_history()

            if page_name == "contacts":
                self.pages["contacts"].load_contacts()

            self.pages[page_name].pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

            self.highlight_active(page_name)
    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.configure(width=70)
            self.logo.configure(text="🛡")
            for btn in self.menu_buttons.values():
                btn.configure(text="")
            self.sidebar_expanded = False
        else:
            self.sidebar.configure(width=240)
            labels = {
                "dashboard": "Dashboard",
                "scanner": "Scan Card",
                "contacts": "Contacts",
                "history": "History",
                "settings": "Settings"
                }
            self.logo.configure(text="🛡 CardVault AI")
            for page, btn in self.menu_buttons.items():
                btn.configure(text=labels[page])
            self.sidebar_expanded = True
    def highlight_active(self, page_name):
        for btn in self.menu_buttons.values():
            btn.configure(
                fg_color="transparent"
                )
        self.menu_buttons[page_name].configure(
            fg_color="#2563EB"
            )
if __name__ == "__main__":
    create_database()
    app = CardVaultAI()
    app.mainloop()