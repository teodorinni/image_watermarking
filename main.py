import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import copy


FONT_COLOR = (225, 225, 225)
TEXT_FONT = ImageFont.truetype("ariblk.ttf", size=16)
start_image = Image.open("start_image.jpg")
image_no_watermark = Image.open("start_image.jpg")
image_with_watermark = Image.open("start_image.jpg")
logo_image = Image.open("default_logo.png")
logo_image.thumbnail((200, 200))
logo_uploaded = False


# upload image to change
def upload_image():
    filetypes = [("Image Files", ".bmp .ico .jpeg .jpg .png")]
    file_dir = filedialog.askopenfilename(title="Select an image to upload ", initialdir="/", filetypes=filetypes)
    global image_no_watermark, image_with_watermark, img_to_change
    image_no_watermark = Image.open(file_dir)
    image_no_watermark.thumbnail((900, 600), Image.ANTIALIAS)
    image_with_watermark = Image.open(file_dir)
    image_with_watermark.thumbnail((900, 600), Image.ANTIALIAS)
    img_to_change = ImageTk.PhotoImage(image=image_no_watermark)
    canvas.itemconfig(img_on_screen, image=img_to_change)
    r_text.config(state="normal")
    enable_text()
    r_logo.config(state="normal")


# enable text entry if text radio button is selected
def enable_text():
    text_entry.config(state="normal")
    logo_upload.config(state="disabled")
    x_label.config(state="disabled")
    y_label.config(state="disabled")
    x_coord.config(state="disabled")
    y_coord.config(state="disabled")


# enable upload logo button if upload radio button is selected
def enable_upload():
    logo_upload.config(state="normal")
    text_entry.config(state="disabled")
    if logo_uploaded:
        enable_coords()


# upload logo
def upload_logo():
    filetypes = [("Image Files", ".bmp .ico .jpeg .jpg .png")]
    file_dir = filedialog.askopenfilename(title="Select an image to upload ", initialdir="/", filetypes=filetypes)
    global logo_image, logo_uploaded
    logo_image = Image.open(file_dir)
    logo_image.thumbnail((200, 200))
    enable_coords()
    logo_uploaded = True


# check if text for watermark is not empty
def check_watermark_text(*args):
    if text_str.get() != "" and text_or_logo.get() == 0:
        enable_coords()
    elif text_str.get() == "" and text_or_logo.get() == 0:
        x_label.config(state="disabled")
        y_label.config(state="disabled")
        x_coord.config(state="disabled")
        y_coord.config(state="disabled")


# enable coordinates entries
def enable_coords():
    x_label.config(state="normal")
    y_label.config(state="normal")
    x_coord.config(state="normal")
    y_coord.config(state="normal")


# check inputs in x coordinate and y coordinate, delete any symbols except numbers and activate check image button
def check_x_coord(*args):
    try:
        int(x_value.get())
        x_status.config(text="")
        if len(x_value.get()) > 4:
            x_value.set(x_value.get()[:-1])
            x_status.config(text="4 characters max.")
    except ValueError:
        if len(x_value.get()) != 0:
            x_value.set(x_value.get()[:-1])
            x_status.config(text="Only numbers are allowed.")
        else:
            pass
    finally:
        if len(x_value.get()) > 0 and len(y_value.get()) > 0:
            add_wm_btn.config(state="normal")
        else:
            add_wm_btn.config(state="disabled")


def check_y_coord(*args):
    try:
        int(y_value.get())
        y_status.config(text="")
        if len(y_value.get()) > 4:
            y_value.set(y_value.get()[:-1])
            y_status.config(text="4 characters max.")
    except ValueError:
        if len(y_value.get()) != 0:
            y_value.set(y_value.get()[:-1])
            y_status.config(text="Only numbers are allowed.")
        else:
            pass
    finally:
        if len(y_value.get()) > 0 and len(x_value.get()) > 0:
            add_wm_btn.config(state="normal")
        else:
            add_wm_btn.config(state="disabled")


# modify selected image and send it to screen
def add_watermark():
    global image_with_watermark, img_with_watermark, img_with_watermark_logo, logo_image
    # if text watermark is selected
    if text_or_logo.get() == 0:
        watermark_text = text_str.get()
        image_editable = ImageDraw.Draw(image_with_watermark)
        image_editable.text((float(x_value.get()), float(y_value.get())), watermark_text, fill=FONT_COLOR, font=TEXT_FONT)
        img_with_watermark = ImageTk.PhotoImage(image=image_with_watermark)
        canvas.itemconfig(img_on_screen, image=img_with_watermark)
        save_btn.config(state="normal")
        clear_btn.config(state="normal")
    # if logo watermark is selected
    else:
        image_with_watermark.paste(logo_image, (int(x_value.get()), int(y_value.get())), mask=logo_image)
        img_with_watermark_logo = ImageTk.PhotoImage(image=image_with_watermark)
        canvas.itemconfig(img_on_screen, image=img_with_watermark_logo)
        save_btn.config(state="normal")
        clear_btn.config(state="normal")


def save_image():
    file = filedialog.asksaveasfile(mode="w", defaultextension=".jpg")
    if file is None:
        return
    image_with_watermark.save(file)


def clear_watermark():
    global image_no_watermark, image_with_watermark, img_with_watermark_clear
    image_with_watermark = copy.deepcopy(image_no_watermark)
    img_with_watermark_clear = ImageTk.PhotoImage(image=image_with_watermark)
    canvas.itemconfig(img_on_screen, image=img_with_watermark_clear)
    save_btn.config(state="disabled")


# app
app = tk.Tk()
app.minsize(width=1000, height=800)
app.title("Image Watermarking App")
app.config(padx=30, pady=30)

# canvas
canvas = tk.Canvas(app, width=900, height=600, highlightthickness=0, borderwidth=0)
start_img = ImageTk.PhotoImage(image=start_image)
img_on_screen = canvas.create_image(450, 300, image=start_img)
canvas.grid(row=0, column=0, columnspan=7, padx=10, pady=10)

# upload image button
upload_button = tk.Button(app, text="Upload Image", height=2, command=upload_image)
upload_button.grid(row=1, column=6, rowspan=2, ipadx=10, ipady=10)

# radiobuttons to select text or logo watermark
text_or_logo = tk.IntVar(app, 0)
r_text = tk.Radiobutton(app, text="Add text watermark", variable=text_or_logo, value=0, state="disabled", command=enable_text)
r_logo = tk.Radiobutton(app, text="Add logo watermark", variable=text_or_logo, value=1, state="disabled", command=enable_upload)
r_text.grid(row=1, column=0, padx=5, pady=5)
r_logo.grid(row=2, column=0, padx=5, pady=5)

# text entry and logo uploads
text_str = tk.StringVar(app)
text_str.trace("w", check_watermark_text)
text_entry = tk.Entry(app, state="disabled", textvariable=text_str)
logo_upload = tk.Button(app, text="Upload Logo", state="disabled", command=upload_logo)
text_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
logo_upload.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# watermark coordinates
x_label = tk.Label(app, text="X coordinate:", state="disabled")
x_value = tk.StringVar(app)
x_value.trace("w", check_x_coord)
x_coord = tk.Entry(app, state="disabled", width=5, textvariable=x_value)
x_status = tk.Label(app, fg="red", width=25)
y_label = tk.Label(app, text="Y coordinate:", state="disabled")
y_value = tk.StringVar(app)
y_value.trace("w", check_y_coord)
y_coord = tk.Entry(app, state="disabled", width=5, textvariable=y_value)
y_status = tk.Label(app, fg="red", width=25)
x_label.grid(row=1, column=2, sticky="e", padx=5, pady=5)
x_coord.grid(row=1, column=3, sticky="w", padx=5, pady=5)
x_status.grid(row=1, column=4, sticky="w", padx=5, pady=5)
y_label.grid(row=2, column=2, sticky="e", padx=5, pady=5)
y_coord.grid(row=2, column=3, sticky="w", padx=5, pady=5)
y_status.grid(row=2, column=4, sticky="w", padx=5, pady=5)

# check image and save image button
add_wm_btn = tk.Button(app, text="Add Watermark", width=16, state="disabled", command=add_watermark)
save_btn = tk.Button(app, text="Save Image", width=16, state="disabled", command=save_image)
clear_btn = tk.Button(app, text="Clear Watermarks", width=16, state="disabled", command=clear_watermark)
add_wm_btn.grid(row=1, column=5, padx=5, pady=5)
save_btn.grid(row=3, column=5, padx=5, pady=5)
clear_btn.grid(row=2, column=5, padx=5, pady=5)

app.mainloop()
