from PIL import Image, ImageGrab
import pytesseract
from tkinter import Tk, Button, Scrollbar, filedialog, messagebox, Text, VERTICAL, END, Frame
import re
import io


class RoundedTextFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0, relief="flat")
        self.text_area = Text(self, wrap="word", font=("Times New Roman", 14), width=60, height=20)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)


class ImageToTextApp:
    def __init__(self, master):
        self.master = master
        master.title("Image to Text Converter (c) Elshan Gurbanov")
        self.scroll_y = Scrollbar(master, orient=VERTICAL)
        self.scroll_y.pack(side="right", fill="y")
        self.text_frame = RoundedTextFrame(master)
        self.text_frame.pack(side="left", expand=True, fill="both")
        self.scroll_y.config(command=self.text_frame.text_area.yview)
        set_tesseract_path()
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.image_path = None
        self.clipboard_button = Button(master, text="Clipboard", command=self.perform_ocr_from_clipboard)
        self.clipboard_button.pack(side="top", padx=5, pady=5, fill="x")
        self.browse_button = Button(master, text="Browse", command=self.browse_image)
        self.browse_button.pack(side="top", padx=5, pady=5, fill="x")
        self.copy_button = Button(master, text="Copy", command=self.copy_text)
        self.copy_button.pack(side="top", padx=5, pady=5, fill="x")
        self.delete_button = Button(master, text="Delete", command=self.delete_text)
        self.delete_button.pack(side="top", padx=5, pady=5, fill="x")

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.convert_image()

    def convert_image(self):
        if self.image_path:
            try:
                image_print = Image.open(self.image_path)
                text = pytesseract.image_to_string(image_print, lang='rus+eng')
                text = re.sub(r'\xa0', ' ', text)
                self.text_frame.text_area.delete("1.0", END)  # Clear previous text
                self.text_frame.text_area.insert("1.0", text)
            except FileNotFoundError:
                messagebox.showerror("Error", "Image file not found.")
            except pytesseract.TesseractNotFoundError:
                messagebox.showerror("Error", "Pytesseract not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error processing image: {e}")
        else:
            messagebox.showwarning("Warning", "Please select an image first.")

    def copy_text(self):
        text_to_copy = self.text_frame.text_area.get("1.0", END)
        self.master.clipboard_clear()
        self.master.clipboard_append(text_to_copy)
        self.master.update()

    def delete_text(self):
        self.text_frame.text_area.delete("1.0", END)

    def perform_ocr_from_clipboard(self):
        try:
            clipboard_image = ImageGrab.grabclipboard()
            if clipboard_image:
                image_stream = io.BytesIO()
                clipboard_image.save(image_stream, format='PNG')
                image_stream.seek(0)
                image_print = Image.open(image_stream)
                text = pytesseract.image_to_string(image_print, lang='rus+eng')
                text = re.sub(r'\xa0', ' ', text)
                self.text_frame.text_area.delete("1.0", END)
                self.text_frame.text_area.insert("1.0", text)
            else:
                messagebox.showwarning("Warning", "Clipboard does not contain a valid image.")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing clipboard image: {e}")


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
