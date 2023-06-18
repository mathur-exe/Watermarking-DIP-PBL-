from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

# function to open an image file
def open_image():
    filename = filedialog.askopenfilename()
    return filename

# function to save an image file
def save_image(image):
    filename = filedialog.asksaveasfilename()
    image.save(filename)

# function to add watermark to image
def watermark(image_path, watermark_text):
    # open image file
    image = Image.open(image_path)

    # create ImageDraw object
    draw = ImageDraw.Draw(image)

    # get the image size
    width, height = image.size

    # set font for watermark text
    # font = ImageFont.truetype("path/to/arial.ttf", 36)

    # calculate position for watermark text
    # text_width, text_height = draw.textsize(watermark_text, font)
    # x = width - text_width - 10
    # y = height - text_height - 10

    # add watermark text to image
    # draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    return image

# function to handle button click event
def add_watermark():
    # get input images and watermark text from user
    image_path = open_image()
    watermark_text = watermark_text_input.get()

    # add watermark to image
    watermarked_image = watermark(image_path, watermark_text)

    # save watermarked image
    save_image(watermarked_image)

# create GUI
root = Tk()
root.title("Image Watermarking")

# create input fields for image and watermark text
image_path_input = Entry(root, width=50)
watermark_text_input = Entry(root, width=50)

# create buttons for selecting image and adding watermark
select_image_button = Button(root, text="Select Image", command=lambda: image_path_input.insert(0, open_image()))
add_watermark_button = Button(root, text="Add Watermark", command=add_watermark)

# set default watermark text
watermark_text_input.insert(0, "© Your Company Name")

# display input fields and buttons
image_path_input.grid(row=0, column=0, padx=10, pady=10)
select_image_button.grid(row=0, column=1, padx=10, pady=10)
watermark_text_input.grid(row=1, column=0, padx=10, pady=10)
add_watermark_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
