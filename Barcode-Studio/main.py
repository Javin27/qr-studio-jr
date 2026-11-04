import io
import tkinter as tk
from tkinter import filedialog, messagebox

import barcode
import cv2
import numpy as np
import zxingcpp
from barcode.writer import ImageWriter
from PIL import Image, ImageTk

# ---------- Global variables ----------
generated_image = None   # PIL image of the last generated barcode
generated_photo = None   # Tk photo (must be kept so it doesn't disappear)
scan_photo = None        # Tk photo for scanner preview
camera = None
camera_running = False

# ---------- Window ----------
window = tk.Tk()
window.title("Barcode Studio")
window.geometry("800x600")

# ---------- Three pages (frames) ----------
home_frame = tk.Frame(window)
gen_frame = tk.Frame(window)
scan_frame = tk.Frame(window)


def show_page(page):
    stop_camera()
    home_frame.pack_forget()
    gen_frame.pack_forget()
    scan_frame.pack_forget()
    page.pack(fill="both", expand=True, padx=20, pady=20)


def go_home():
    show_page(home_frame)


def go_generator():
    show_page(gen_frame)


def go_scanner():
    show_page(scan_frame)


# ---------- Generator functions ----------
def generate(event=None):
    global generated_image, generated_photo

    data = data_entry.get().strip()
    if data == "":
        messagebox.showwarning("Missing data", "Enter text or numbers first.")
        return

    try:
        code = barcode.get("code128", data, writer=ImageWriter())
        buffer = io.BytesIO()
        code.write(buffer)
        buffer.seek(0)

        generated_image = Image.open(buffer).convert("RGB")

        small = generated_image.copy()
        small.thumbnail((650, 190))
        generated_photo = ImageTk.PhotoImage(small)

        gen_preview.config(image=generated_photo, text="")
        save_button.config(state="normal")
        gen_status.config(text="Generated Code 128 barcode")
    except Exception as error:
        messagebox.showerror("Generation error", str(error))


def save():
    if generated_image is None:
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile="barcode.png",
        filetypes=[("PNG image", "*.png")],
    )
    if path:
        generated_image.save(path, "PNG")
        gen_status.config(text="Saved successfully")


# ---------- Scanner functions ----------
def decode_image(image):
    results = zxingcpp.read_barcodes(np.asarray(image))

    texts = []
    for result in results:
        if result.text and result.text not in texts:
            texts.append(result.text)

    if len(texts) > 0:
        result_var.set(" | ".join(texts))
        scan_status.config(text="Found " + str(len(texts)) + " barcode(s)")
    else:
        scan_status.config(text="No readable barcode found.")


def upload_image():
    global scan_photo

    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")]
    )
    if not path:
        return

    try:
        image = Image.open(path).convert("RGB")

        small = image.copy()
        small.thumbnail((650, 250))
        scan_photo = ImageTk.PhotoImage(small)
        scan_preview.config(image=scan_photo, text="")

        decode_image(image)
    except Exception as error:
        messagebox.showerror("Image error", str(error))


def start_camera():
    global camera, camera_running

    if camera_running:
        return

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera.release()
        camera = None
        messagebox.showerror("Camera unavailable", "Could not open the webcam.")
        return

    camera_running = True
    scan_status.config(text="Webcam running - point it at a barcode.")
    camera_loop()


def camera_loop():
    global scan_photo

    if not camera_running:
        return

    ok, frame = camera.read()
    if ok:
        results = zxingcpp.read_barcodes(frame)
        if len(results) > 0 and results[0].text:
            result_var.set(results[0].text)
            scan_status.config(text="Barcode detected")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        image.thumbnail((650, 280))
        scan_photo = ImageTk.PhotoImage(image)
        scan_preview.config(image=scan_photo, text="")

    window.after(35, camera_loop)


def stop_camera():
    global camera, camera_running

    camera_running = False
    if camera is not None:
        camera.release()
        camera = None


def copy_result():
    value = result_var.get()
    if value != "" and value != "No barcode scanned yet.":
        window.clipboard_clear()
        window.clipboard_append(value)
        scan_status.config(text="Copied to clipboard.")


def on_close():
    stop_camera()
    window.destroy()


# ---------- Home page widgets ----------
tk.Label(home_frame, text="Barcode Studio", font=("Arial", 24, "bold")).pack(pady=20)
tk.Label(home_frame, text="Create and scan 1D barcodes.").pack(pady=(0, 30))
tk.Button(home_frame, text="Barcode Generator", font=("Arial", 14),
          command=go_generator, width=20).pack(pady=10)
tk.Button(home_frame, text="Barcode Scanner", font=("Arial", 14),
          command=go_scanner, width=20).pack(pady=10)

# ---------- Generator page widgets ----------
tk.Button(gen_frame, text="< Home", command=go_home).pack(anchor="w")
tk.Label(gen_frame, text="Barcode Generator", font=("Arial", 20, "bold")).pack(pady=10)

tk.Label(gen_frame, text="Barcode data:").pack(anchor="w")
data_entry = tk.Entry(gen_frame, font=("Arial", 12))
data_entry.pack(fill="x", pady=5)
data_entry.bind("<Return>", generate)

tk.Button(gen_frame, text="Generate", command=generate).pack(pady=5)

gen_preview = tk.Label(gen_frame, text="Your barcode will appear here.", bg="#EEEEEE")
gen_preview.pack(fill="both", expand=True, pady=10)

gen_status = tk.Label(gen_frame, text="Ready")
gen_status.pack(side="left")
save_button = tk.Button(gen_frame, text="Save PNG", command=save, state="disabled")
save_button.pack(side="right")

# ---------- Scanner page widgets ----------
tk.Button(scan_frame, text="< Home", command=go_home).pack(anchor="w")
tk.Label(scan_frame, text="Barcode Scanner", font=("Arial", 20, "bold")).pack(pady=10)

button_row = tk.Frame(scan_frame)
button_row.pack()
tk.Button(button_row, text="Upload Image", command=upload_image).pack(side="left", padx=5)
tk.Button(button_row, text="Start Webcam", command=start_camera).pack(side="left", padx=5)
tk.Button(button_row, text="Stop Webcam", command=stop_camera).pack(side="left", padx=5)

scan_preview = tk.Label(scan_frame, text="Image or webcam preview will appear here.", bg="#EEEEEE")
scan_preview.pack(fill="both", expand=True, pady=10)

tk.Label(scan_frame, text="Scanned result:").pack(anchor="w")
result_var = tk.StringVar(value="No barcode scanned yet.")
tk.Entry(scan_frame, textvariable=result_var, state="readonly",
         font=("Arial", 12)).pack(fill="x", pady=5)
tk.Button(scan_frame, text="Copy", command=copy_result).pack(anchor="w")

scan_status = tk.Label(scan_frame, text="Ready")
scan_status.pack(anchor="w", pady=5)

# ---------- Start the app ----------
show_page(home_frame)
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()