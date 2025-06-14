import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import pytesseract

def select_and_ocr():
    # Open system file manager dialog for selecting image files
    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
    filepath = filedialog.askopenfilename(title="Select an Image File", filetypes=filetypes)

    if not filepath:
        return  # user canceled
    
    try:
        # Open and OCR the selected image
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        
        # Display extracted text or message if none found
        if text.strip():
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, text)
        else:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, "[No text detected in the image.]")
        
        # Update label showing the selected file
        file_label.config(text=f"File: {filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"Error processing image:\n{e}")

root = tk.Tk()
root.title("Image to Text OCR")
root.geometry("700x600")

upload_btn = tk.Button(root, text="Select Image File", command=select_and_ocr, font=("Arial", 14))
upload_btn.pack(pady=20)

file_label = tk.Label(root, text="No file selected", fg="gray")
file_label.pack()

text_area = scrolledtext.ScrolledText(root, font=("Arial", 12))
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
