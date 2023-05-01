import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog

# Define a function to open the source and watermark images


class DisplayWindow:
    global original_image, watermark_image, original_image_resized
    global width, height, x, y, alpha
    def __init__(self, master):
        self.master = master
        master.title("Watermarking")

        self.width = tk.IntVar(value=200)
        self.height = tk.IntVar(value=200)
        self.x = tk.IntVar(value=0)
        self.y = tk.IntVar(value=0)
        self.alpha = tk.DoubleVar(value=0.5)

        self.original_image = None
        self.watermark_image = None
        self.original_image_resized = None

        self.open_button = tk.Button(master, text='Open Images', command=self.open_images)
        self.open_button.pack()

        self.width_slider = tk.Scale(master, from_=100, to=2000, orient=tk.HORIZONTAL, label='Width', variable=self.width)
        self.width_slider.pack()

        self.height_slider = tk.Scale(master, from_=100, to=2000, orient=tk.HORIZONTAL, label='Height', variable=self.height)
        self.height_slider.pack()

        self.x_slider = tk.Scale(master, from_=0, to=1900, orient=tk.HORIZONTAL, label='X Position', variable=self.x)
        self.x_slider.pack()

        self.y_slider = tk.Scale(master, from_=0, to=1200, orient=tk.HORIZONTAL, label='Y Position', variable=self.y)
        self.y_slider.pack()

        self.alpha_slider = tk.Scale(master, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, label='Watermark Intensity', variable=self.alpha)
        self.alpha_slider.pack()

        self.embed_button = tk.Button(master, text='Embed Watermark', command=self.embed_watermark)
        self.embed_button.pack()


    def open_images(self):
        
        self.source_path = filedialog.askopenfilename()
        self.watermark_path = filedialog.askopenfilename()

        self.original_image = cv2.imread(self.source_path, cv2.IMREAD_GRAYSCALE)
        self.original_image_resized = cv2.resize(self.original_image, (self.width.get(), self.height.get()))
        self.watermark_image = cv2.imread(self.watermark_path, cv2.IMREAD_GRAYSCALE)
        self.watermark_image = cv2.resize(self.watermark_image, (self.width.get(), self.height.get()))


    # Define a function to embed the watermark and display the watermarked image
    def embed_watermark(self):
        original_dct = cv2.dct(np.float32(self.original_image_resized)/255.0)
        watermark_dct = cv2.dct(np.float32(self.watermark_image)/255.0)

        watermarked_dct = original_dct + self.alpha.get() * watermark_dct

        watermarked_image = cv2.idct(watermarked_dct) * 255.0

        cv2.imshow('Watermarked Image', watermarked_image)

window = tk.Tk()
root = DisplayWindow(window)
window.mainloop()