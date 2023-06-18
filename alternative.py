import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

class Embedder:
    def _init_(self):
        self.master = tk.Tk()
        self.original_image = None
        self.original_image_resized = None
        self.watermark_image = None
        self.alpha = tk.DoubleVar()
        self.alpha.set(0.1)
        
        self.master.title("Image Watermarking")
        self.master.geometry("800x600")

        self.original_image_label = tk.Label(self.master, text="Original Image")
        self.original_image_label.pack()
        self.select_original_image_button = tk.Button(self.master, text="Select Original Image", command=self.select_original_image)
        self.select_original_image_button.pack()

        self.watermark_image_label = tk.Label(self.master, text="Watermark Image")
        self.watermark_image_label.pack()
        self.select_watermark_image_button = tk.Button(self.master, text="Select Watermark Image", command=self.select_watermark_image)
        self.select_watermark_image_button.pack()

        self.alpha_label = tk.Label(self.master, text="Alpha")
        self.alpha_label.pack()
        self.alpha_scale = tk.Scale(self.master, from_=0.0, to=1.0, resolution=0.01, variable=self.alpha, orient=tk.HORIZONTAL, length=400)
        self.alpha_scale.pack()

        self.embed_button = tk.Button(self.master, text="Embed Watermark", command=self.embed_watermark)
        self.embed_button.pack()

        self.master.mainloop()

    def select_original_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image File", ".jpg .png")])
        if path:
            self.original_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            self.original_image_resized = cv2.resize(self.original_image, (512, 512))
            cv2.imshow("Original Image", self.original_image_resized)

    def select_watermark_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image File", ".jpg .png")])
        if path:
            self.watermark_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            self.watermark_image = cv2.resize(self.watermark_image, (512, 512))
            cv2.imshow("Watermark Image", self.watermark_image)

    def embed_watermark(self):
        # Zero-pad the watermark image
        pad_height = self.original_image_resized.shape[0] - self.watermark_image.shape[0]
        pad_width = self.original_image_resized.shape[1] - self.watermark_image.shape[1]
        watermark_image_padded = np.pad(self.watermark_image, ((0, pad_height), (0, pad_width)), mode='constant')

        original_dct = cv2.dct(np.float32(self.original_image_resized)/255.0)
        watermark_dct = cv2.dct(np.float32(watermark_image_padded)/255.0)

        watermarked_dct = original_dct + self.alpha.get() * watermark_dct

        watermarked_image = cv2.idct(watermarked_dct) * 255.0
        watermarked_image = np.uint8(watermarked_image)

        cv2.imshow("Watermarked Image", watermarked_image)

    def run(self):
        self.master.mainloop()


if __name__ == '_main_':
    embedder = Embedder()
    embedder.run()