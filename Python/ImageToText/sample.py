import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract

# Set up main application window
class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Text OCR Converter")

        self.label = tk.Label(root, text="Select an Image File")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Image File", command=self.select_image)
        self.select_button.pack(pady=20)

        self.result_text = tk.Text(root, height=15, width=50)
        self.result_text.pack(pady=10)

    # Function to select image file
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if file_path:
            self.extract_text(file_path)

    # Function to extract text using OCR
    def extract_text(self, file_path):
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            self.result_text.delete(1.0, tk.END)  # Clear previous text
            self.result_text.insert(tk.END, text)  # Display new text
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
