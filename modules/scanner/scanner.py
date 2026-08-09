import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import pytesseract
from modules.parser.card_parser import *
from database.database import save_contact
from database.database import save_scan_history
from tkinter import messagebox
from database.database import get_scan_history
from database.database import (
    save_contact,
    save_scan_history,
    contact_exists
)

class ScannerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Header
        header = ctk.CTkLabel(
            self,
            text="📷 Scan Business Card",
            font=("Segoe UI", 28, "bold")
        )
        header.pack(anchor="w", padx=20, pady=20)

        # Main Container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Side
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        upload_btn = ctk.CTkButton(
            left_frame,
            text="📤 Upload Card Image",
            height=45,
            command=self.upload_image
        )
        upload_btn.pack(pady=15)

        self.preview_label = ctk.CTkLabel(
             left_frame,
             text="Upload a visiting card",
             width=500,
             height=300
             )
        self.preview_label.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        # Right Side
        right_frame = ctk.CTkScrollableFrame(
            main_frame,
            width=450
        )
        right_frame.pack(
            side="right",
            fill="both",
            expand=False,
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            right_frame,
            text="Extracted Information",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=15)
        self.ocr_textbox = ctk.CTkTextbox(
            right_frame,
            width=400,
            height=150
        )
        self.ocr_textbox.pack(
            padx=15,
            pady=10
        )

        fields = [
            "Name",
            "Company",
            "Designation",
            "Phone",
            "Email",
            "Website",
            "Address"
        ]

        self.entries = {}

        for field in fields:

            label = ctk.CTkLabel(
                right_frame,
                text=field
            )
            label.pack(anchor="w", padx=15)

            entry = ctk.CTkEntry(
                right_frame,
                width=350
            )
            entry.pack(padx=15, pady=5)

            self.entries[field] = entry

        ctk.CTkButton(
            right_frame,
            text="💾 Save Contact",
            height=45,
            command=self.save_contact_data
        ).pack(pady=20)
        
    # ← Step 5 goes BELOW here

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.webp")
            ]
        )

        if not file_path:
            return
        self.current_image_path = file_path

        image = Image.open(file_path)

        image.thumbnail((500, 300))

        photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        self.preview_label.configure(
            image=photo,
            text=""
        )

        self.preview_label.image = photo

        self.run_ocr(file_path)

    def run_ocr(self, image_path):
        import cv2
        img = cv2.imread(image_path)
        # Scale image 3x
        img = cv2.resize(
            img,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        gray = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        text = pytesseract.image_to_string(
            gray,
            config="--oem 3 --psm 6"
        )

        self.ocr_textbox.delete("1.0", "end")
        self.ocr_textbox.insert("1.0", text)

        self.auto_fill_fields(text)
    def auto_fill_fields(self, text):
        self.entries["Name"].delete(0, "end")
        self.entries["Name"].insert(
            0,
            extract_name(text)
        )
        self.entries["Phone"].delete(0, "end")
        self.entries["Phone"].insert(
            0,
            extract_phone(text)
        )
        self.entries["Email"].delete(0, "end")
        self.entries["Email"].insert(
            0,
            extract_email(text)
        )
        self.entries["Website"].delete(0, "end")
        self.entries["Website"].insert(
            0,
            extract_website(text)
        )
        self.entries["Designation"].delete(0, "end")
        self.entries["Designation"].insert(
            0,
            extract_designation(text)
        )
        self.entries["Company"].delete(0, "end")
        self.entries["Company"].insert(
            0,
            extract_company(text)
        )
        self.entries["Address"].delete(0, "end")
        self.entries["Address"].insert(
            0,
        extract_address(text)
        )
        
    def save_contact_data(self):

        try:

            data = {
                "name": self.entries["Name"].get(),
                "company": self.entries["Company"].get(),
                "designation": self.entries["Designation"].get(),
                "phone": self.entries["Phone"].get(),
                "email": self.entries["Email"].get(),
                "website": self.entries["Website"].get(),
                "address": self.entries["Address"].get(),
                "image_path": getattr(self, "current_image_path", "")
            }

            existing = contact_exists(
                data["name"],
                data["phone"]
            )

            if existing:

                answer = messagebox.askyesno(
                    "Duplicate Contact",
                    "This contact already exists.\nDo you want to save it again?"
                )

                if not answer:
                    return

            save_contact(data)

            save_scan_history(
                data["name"],
                data["image_path"],
                self.ocr_textbox.get("1.0", "end")
            )

            messagebox.showinfo(
                "Success",
                "Contact Saved Successfully"
            )

            print("Contact Saved Successfully")

        except Exception as e:
            print("SAVE ERROR:", e)
            messagebox.showerror("Error", str(e))