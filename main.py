from PIL import Image
import pytesseract
from tkinter import Tk, Button, Scrollbar, filedialog, messagebox, Text, VERTICAL, END
import re


class ImageToTextApp:
    def __init__(self, master):
        self.master = master
        master.title("Image to Text Converter (c) Elshan Gurbanov")
        self.scroll_y = Scrollbar(master, orient=VERTICAL)
        self.scroll_y.pack(side="right", fill="y")
        self.text_area = Text(master, wrap="word", yscrollcommand=self.scroll_y.set, font=("Times New Roman", 14),
                              width=60, height=40)
        self.text_area.pack(side="left", expand=True, fill="both")
        self.scroll_y.config(command=self.text_area.yview)
        self.browse_button = Button(master, text="Browse", command=self.browse_image)
        self.browse_button.pack(side="left", pady=10)
        self.copy_button = Button(master, text="Copy", command=self.copy_text)
        self.copy_button.pack(side="left", pady=10)
        set_tesseract_path()
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.image_path = None

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.convert_image()

    def convert_image(self):
        try:
            image_print = Image.open(self.image_path)
            text = pytesseract.image_to_string(image_print, lang='rus+eng')
            text = re.sub(r'\xa0', ' ', text)
            self.text_area.delete("1.0", END)
            self.text_area.insert("1.0", text)
        except FileNotFoundError:
            messagebox.showerror("Error", "Image file not found.")
        except pytesseract.TesseractNotFoundError:
            messagebox.showerror("Error", "Pytesseract not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {e}")

    def copy_text(self):
        text_to_copy = self.text_area.get("1.0", END)
        self.master.clipboard_clear()
        self.master.clipboard_append(text_to_copy)
        self.master.update()


def set_tesseract_path():
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tessdata_dir_config = r'C:\Program Files\Tesseract-OCR\tessdata'
    except pytesseract.TesseractNotFoundError:
        messagebox.showerror("Error", "Pytesseract not found")


def main():
    root = Tk()
    app = ImageToTextApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
