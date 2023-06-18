import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class Embedder:
    def _init_(self):
        self.original_image_path = ""
        self.original_image = None
        self.watermark_image_path = ""
        self.watermark_image = None
        self.watermarked_image = None

    def select_original_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image_path = path
            self.original_image = cv2.imread(path)
            # cv2.imshow("Original Image", self.original_image)

    def select_watermark_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.watermark_image_path = path
            self.watermark_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            # cv2.imshow("Watermark Image", self.watermark_image)

    def embed_watermark(self):
        if self.original_image is None or self.watermark_image is None:
            return

        # Resize watermark image to fit into original image's bottom right corner
        height, width = self.original_image.shape[:2]
        watermark_height, watermark_width = self.watermark_image.shape[:2]
        resized_watermark_height = min(int(height * 0.25), watermark_height)
        resized_watermark_width = min(int(width * 0.25), watermark_width)
        watermark_resized = cv2.resize(self.watermark_image, (resized_watermark_width, resized_watermark_height))

        # Define region of interest (ROI) as bottom right corner of original image
        roi = self.original_image[height - resized_watermark_height:height, width - resized_watermark_width:width]

        # Add watermark to ROI
        watermark_mask = cv2.threshold(watermark_resized, 127, 255, cv2.THRESH_BINARY)[1]
        watermark_mask = cv2.merge((watermark_mask, watermark_mask, watermark_mask))
        bg_mask = cv2.bitwise_not(watermark_mask)
        watermark_colored = cv2.merge((watermark_resized, watermark_resized, watermark_resized))
        watermark_bg = cv2.bitwise_and(roi, bg_mask)
        watermark_fg = cv2.bitwise_and(watermark_colored, watermark_mask)
        watermark_added = cv2.add(watermark_bg, watermark_fg)
        self.watermarked_image = self.original_image.copy()
        self.watermarked_image[height - resized_watermark_height:height, width - resized_watermark_width:width] = watermark_added

        # Display watermarked image
        cv2.imshow("Watermarked Image", self.watermarked_image)

    def run(self):
        root = tk.Tk()
        root.title("Watermark Embedder")
        root.geometry("500x300")

        original_image_button = tk.Button(root, text="Select Original Image", command=self.select_original_image)
        original_image_button.pack()

        watermark_image_button = tk.Button(root, text="Select Watermark Image", command=self.select_watermark_image)
        watermark_image_button.pack()

        embed_button = tk.Button(root, text="Embed Watermark", command=self.embed_watermark)
        embed_button.pack()

        root.mainloop()

embedder = Embedder()
embedder.run()