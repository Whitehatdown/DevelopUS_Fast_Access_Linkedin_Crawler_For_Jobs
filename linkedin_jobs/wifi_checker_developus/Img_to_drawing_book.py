import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, Frame, Listbox, EXTENDED, Scrollbar
from PIL import Image, ImageTk
import os

def convert_to_coloring_sheet(image_path, output_path):
    # Step 1: Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # Resize image to ensure both images fit well together
    image = cv2.resize(image, (500, 500))
    
    # Step 2: Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply edge detection with smoothing for anti-aliasing
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(gray_image, 50, 150)

    # Step 4: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 5: Create a blank white canvas
    canvas = np.ones_like(gray_image) * 255

    # Step 6: Draw contours on the blank canvas with anti-aliasing
    for contour in contours:
        cv2.drawContours(canvas, [contour], -1, (0, 0, 0), 1, cv2.LINE_AA)

    # Combine original image and coloring sheet side by side
    combined_image = np.hstack((image, cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)))

    # Save the result
    cv2.imwrite(output_path, combined_image)

    # Optional: Display the result
    plt.imshow(cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB))
    plt.title('Original and Coloring Sheet')
    plt.axis('off')
    plt.show()

class App:
    def __init__(self, master):
        self.master = master
        master.title("Image to Coloring Sheet Converter")

        self.frame = Frame(master)
        self.frame.pack(pady=10)

        self.label = Label(self.frame, text="Upload images to convert them to coloring sheets.")
        self.label.grid(row=0, column=0, columnspan=2)

        self.upload_button = Button(self.frame, text="Upload Images", command=self.upload_images)
        self.upload_button.grid(row=1, column=0, pady=5)

        self.download_button = Button(self.frame, text="Download Coloring Sheets", command=self.download_coloring_sheets, state='disabled')
        self.download_button.grid(row=1, column=1, pady=5)

        self.image_listbox = Listbox(self.frame, selectmode=EXTENDED, height=10, width=50)
        self.image_listbox.grid(row=2, column=0, columnspan=2, pady=10)

        self.scrollbar = Scrollbar(self.image_listbox)
        self.scrollbar.pack(side="right", fill="y")

        self.image_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.image_listbox.yview)

        self.image_paths = []
        self.output_dir = "output_coloring_sheets"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def upload_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if files:
            for file in files:
                self.image_paths.append(file)
                self.image_listbox.insert("end", file)
            self.download_button.config(state='normal')

    def download_coloring_sheets(self):
        if self.image_paths:
            for image_path in self.image_paths:
                output_path = os.path.join(self.output_dir, os.path.basename(image_path).split('.')[0] + "_coloring_sheet.png")
                convert_to_coloring_sheet(image_path, output_path)
                print(f"Coloring sheet saved as {output_path}")
            self.image_paths.clear()
            self.image_listbox.delete(0, "end")
            self.download_button.config(state='disabled')

root = Tk()
app = App(root)
root.mainloop()
