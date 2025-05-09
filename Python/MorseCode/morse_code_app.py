import tkinter as tk
from tkinter import ttk, messagebox

# Morse code dictionary for decoding
morse_to_text = {
    ".-": "a", "-...": "b", "-.-.": "c", "-..": "d", ".": "e",
    "..-.": "f", "--.": "g", "....": "h", "..": "i", ".---": "j",
    "-.-": "k", ".-..": "l", "--": "m", "-.": "n", "---": "o",
    ".--.": "p", "--.-": "q", ".-.": "r", "...": "s", "-": "t",
    "..-": "u", "...-": "v", ".--": "w", "-..-": "x", "-.--": "y",
    "--..": "z", "/": " "
}

# Morse code dictionary for encoding
text_to_morse = {v: k for k, v in morse_to_text.items()}
text_to_morse[" "] = "/"  # space to /

# Function to decode morse code to text
def decode_morse():
    morse_input = morse_entry.get("1.0", tk.END).strip()
    if not morse_input:
        messagebox.showwarning("Warning", "Please enter Morse code to decode.")
        return
    morse_chars = morse_input.split(" ")
    decoded_message = ""
    for char in morse_chars:
        decoded_message += morse_to_text.get(char, "?")
    text_entry.delete("1.0", tk.END)
    text_entry.insert(tk.END, decoded_message)

# Function to encode text to morse code
def encode_text():
    text_input = text_entry.get("1.0", tk.END).lower().strip()
    if not text_input:
        messagebox.showwarning("Warning", "Please enter text to encode.")
        return
    encoded_message = ""
    for char in text_input:
        encoded_message += text_to_morse.get(char, "?") + " "
    morse_entry.delete("1.0", tk.END)
    morse_entry.insert(tk.END, encoded_message)

# Main window
root = tk.Tk()
root.title("Morse Code Translator")
root.geometry("720x500")
root.configure(bg="#e9edf0")

# Title label
title_label = tk.Label(root, text="Morse Code Translator", font=("Helvetica", 24, "bold"), bg="#e9edf0", fg="#333")
title_label.pack(pady=20)

# Text to encode
text_frame = tk.LabelFrame(root, text="Text", font=("Helvetica", 14, "bold"), bg="#f9f9f9", fg="#333", padx=10, pady=10)
text_frame.pack(padx=20, pady=10, fill="both")

text_entry = tk.Text(text_frame, height=5, font=("Consolas", 14), wrap=tk.WORD)
text_entry.pack(fill="both")

# Morse code text
morse_frame = tk.LabelFrame(root, text="Morse Code (use / for space between words)", font=("Helvetica", 14, "bold"),
                            bg="#f9f9f9", fg="#333", padx=10, pady=10)
morse_frame.pack(padx=20, pady=10, fill="both")

morse_entry = tk.Text(morse_frame, height=5, font=("Consolas", 14), wrap=tk.WORD)
morse_entry.pack(fill="both")

# Buttons
button_frame = tk.Frame(root, bg="#e9edf0")
button_frame.pack(pady=20)

encode_button = ttk.Button(button_frame, text="Encode to Morse", command=encode_text)
encode_button.grid(row=0, column=0, padx=20, ipadx=10, ipady=5)

decode_button = ttk.Button(button_frame, text="Decode to Text", command=decode_morse)
decode_button.grid(row=0, column=1, padx=20, ipadx=10, ipady=5)

# Footer
footer_label = tk.Label(root, text="© 2025 Aarav MorseCode Application", font=("Helvetica", 10), bg="#e9edf0", fg="#666")
footer_label.pack(side="bottom", pady=10)

# Run the app
root.mainloop()
