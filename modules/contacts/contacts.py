from dataclasses import fields
from turtle import left, right, title

import customtkinter as ctk
from tkinter import messagebox
from database.database import (
    get_all_contacts,
    search_contacts,
    delete_contact,
    export_contacts_excel,
    export_contacts_pdf,
    get_contact_by_id,
    update_contact
)
from PIL import Image, ImageTk
import os


class ContactsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="👥 Contacts",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(anchor="w", padx=20, pady=20)

        # Search Box

        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        toolbar.pack(
            fill="x",
            padx=20,
            pady=10
        )
        self.search_entry = ctk.CTkEntry(
            toolbar,
            width=280,
            placeholder_text="Search Contact..."
        )
        self.search_entry.pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="🔍 Search",
            width=110,
            command=self.search_contact
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="🔄 Refresh",
            width=110,
            command=self.load_contacts
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="📊 Excel",
            width=110,
            command=export_contacts_excel
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            toolbar,
            text="📄 PDF",
            width=110,
            command=export_contacts_pdf
        ).pack(
            side="left",
            padx=5
        )

        # Scrollable Contact Area

        self.contacts_frame = ctk.CTkScrollableFrame(
            self,
            width=1000,
            height=500
        )

        self.contacts_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.load_contacts()
    def search_contact(self):
        keyword = self.search_entry.get()
        for widget in self.contacts_frame.winfo_children():
            widget.destroy()
        contacts = search_contacts(keyword)
        if not contacts:
            ctk.CTkLabel(
                self.contacts_frame,
                text="No Contacts Found"
            ).pack(pady=20)
            return
        for contact in contacts:
            card = ctk.CTkFrame(
                self.contacts_frame
            )
            card.pack(
                fill="x",
                padx=10,
                pady=10
            )
            info = f"""
ID: {contact[0]}

Name: {contact[1]}

Company: {contact[2]}

Designation: {contact[3]}

Phone: {contact[4]}
"""

            ctk.CTkLabel(
                card,
                text=info,
                justify="left",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15,
                pady=15
            )
            
    

    def delete_contact_ui(self, contact_id):
        result = messagebox.askyesno(
            "Delete Contact",
            "Are you sure you want to delete this contact?"
        )
        if result:
            delete_contact(contact_id)
            messagebox.showinfo(
                "Success",
                "✅ Contact Deleted Successfully"
            )
            self.load_contacts()

    def load_contacts(self):

        for widget in self.contacts_frame.winfo_children():
            widget.destroy()

        contacts = get_all_contacts()

        if not contacts:

            ctk.CTkLabel(
                self.contacts_frame,
                text="No Contacts Found"
            ).pack(pady=20)

            return

        for contact in contacts:

            card = ctk.CTkFrame(
                self.contacts_frame
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )

            ctk.CTkLabel(
                card,
                text=f"👤 {contact[1]}",
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w", padx=15, pady=(10,5))

            ctk.CTkLabel(
                card,
                text=f"🏢 {contact[2]}"
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"💼 {contact[3]}"
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"📞 Phone {contact[4]}"
            ).pack(anchor="w", padx=15)
            ctk.CTkLabel(
                card,
                text=f"📧 Email: {contact[5]}"
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"🌐 Website: {contact[6]}"
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"📍 Address: {contact[7]}"
            ).pack(anchor="w", padx=15)

            button_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            button_frame.pack(
                anchor="e",
                padx=15,
                pady=10
            )
            button_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            button_frame.pack(
                anchor="e",
                padx=15,
                pady=10
            )

            ctk.CTkButton(
                button_frame,
                text="👁 View",
                width=90,
                command=lambda c=contact:
                self.view_contact(c)
            ).pack(
                side="left",
                padx=5
            )

            ctk.CTkButton(
                button_frame,
                text="✏ Edit",
                width=90,
                command=lambda cid=contact[0]:
                self.open_edit_window(cid)
            ).pack(
                side="left",
                padx=5
            )

            ctk.CTkButton(
                button_frame,
                text="🗑 Delete",
                width=90,
                fg_color="red",
                command=lambda cid=contact[0]:
                self.delete_contact_ui(cid)
            ).pack(
                side="left",
                padx=5
            )
    def open_edit_window(self, contact_id):
        print("Edit clicked:", contact_id)
        data = get_contact_by_id(contact_id)
        print("Data:", data)
        data = get_contact_by_id(contact_id)

        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.lift()
        self.edit_window.focus_force()
        self.edit_window.grab_set()

        self.edit_window.title("Edit Contact")

        self.edit_window.geometry("500x650")

        labels = [
            "Name",
            "Company",
            "Designation",
            "Phone",
            "Email",
            "Website",
            "Address"
        ]
        entries = []

        values = [
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7]
        ]

        for i, label_text in enumerate(labels):

            ctk.CTkLabel(
                self.edit_window,
                text=label_text
            ).pack(
                pady=(10, 0)
            )

            entry = ctk.CTkEntry(
                self.edit_window,
                width=350
            )

            entry.pack(pady=5)

            entry.insert(
                0,
                str(values[i]) if values[i] is not None else ""
            )
            entries.append(entry)

        ctk.CTkButton(
            self.edit_window,
            text="💾 Save Changes",
            command=lambda:
                self.save_edited_contact(
                    contact_id,
                    entries,
                    self.edit_window
                )
        ).pack(
            pady=20
        )  
    def save_edited_contact(
        self,
        contact_id,
        entries,
        window
    ):

        update_contact(
            contact_id,
            entries[0].get(),
            entries[1].get(),
            entries[2].get(),
            entries[3].get(),
            entries[4].get(),
            entries[5].get(),
            entries[6].get()
        )

        messagebox.showinfo(
            "Success",
            "Contact Updated Successfully"
        )

        window.destroy()

        self.load_contacts()
    def view_contact(self, contact):

        try:

    

            import tkinter as tk

            view = tk.Toplevel(self)
            view.title("Contact Details")
            view.geometry("900x550")
            main_frame = tk.Frame(view)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            left_frame = tk.Frame(main_frame)
            left_frame.pack(side="left", fill="both", padx=20)
            tk.Label(
                left_frame,
                text="🖼 Business Card",
                font=("Segoe UI", 16, "bold")
            ).pack(pady=10)

            image_path = contact[8]
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((280, 180))
                photo = ImageTk.PhotoImage(image)

                image_label = tk.Label(
                    left_frame,
                    image=photo,
                    relief="solid",
                    bd=2
                )

                image_label.image = photo
                image_label.pack(pady=10)

            else:

                tk.Label(
                left_frame,
                text="No Business Card Image",
                width=30,
                height=12,
                relief="solid"
            ).pack()  

            right_frame = tk.Frame(main_frame)
            right_frame.pack(side="right", fill="both", expand=True, padx=20)

            print("Contact:", contact)

            ctk.CTkLabel(
                view,
                text="Contact Details",
                font=("Segoe UI", 24, "bold")
            ).pack(pady=20)

            fields = [
                ("👤 Name", contact[1]),
                ("🏢 Company", contact[2]),
                ("💼 Designation", contact[3]),
                ("📞 Phone", contact[4]),
                ("📧 Email", contact[5]),
                ("🌐 Website", contact[6]),
                ("📍 Address", contact[7])
            ]

            for label, value in fields:

                tk.Label(
                    right_frame,
                    text=label,
                    font=("Segoe UI", 12, "bold"),
                    anchor="w"
                ).pack(anchor="w", pady=(8,0))

                tk.Label(
                    right_frame,
                    text=value,
                    wraplength=350,
                    justify="left"
                ).pack(anchor="w")
                tk.Button(
                    view,
                    text="Close",
                    width=15,
                    command=view.destroy
                ).pack(pady=20)

        except Exception as e:
            print("ERROR:", e)