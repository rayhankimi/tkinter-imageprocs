import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import os


class ImageGUI:
    def __init__(self, root):
        self.root = root

        # Image related attributes
        self.image_paths = []
        self.current_image_index = 0
        self.current_image_path = None
        self.original_image = None  # The original image selected
        self.processed_image = None  # The image after processing

        # GUI elements
        self.image_label = tk.Label(self.root)
        self.load_button = tk.Button(self.root, text="Select a picture directory...", command=self.load_images)
        self.prev_button = tk.Button(self.root, text="Previous", command=self.previous_image)
        self.next_button = tk.Button(self.root, text="Next", command=self.next_image)
        self.select_button = tk.Button(self.root, text="Select this", command=self.select_image)
        self.rotate_button = tk.Button(self.root, text="Rotate", command=self.rotate_image)
        self.grayscale_button = tk.Button(self.root, text="Grayscale", command=self.convert_to_grayscale)
        self.show_original_button = tk.Button(self.root, text="Show Original Image", command=self.show_original_image)
        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)

        # Setup root window
        self.root.title("Image Processing")
        self.root.geometry("600x700")

        # Setup initial GUI
        self.setup_initial_gui()

    def setup_initial_gui(self):
        """Setup the initial GUI elements."""
        # Pack initial GUI elements
        self.image_label.pack(pady=20)
        self.load_button.pack(pady=10)
        self.prev_button.pack(side=tk.LEFT, padx=20)
        self.next_button.pack(side=tk.RIGHT, padx=20)
        self.select_button.pack(pady=20)

        # Hide processing buttons
        self.rotate_button.pack_forget()
        self.grayscale_button.pack_forget()
        self.show_original_button.pack_forget()
        self.save_button.pack_forget()

    def setup_processing_gui(self):
        """Setup the GUI elements for image processing."""
        # Unpack initial GUI elements
        self.load_button.pack_forget()
        self.prev_button.pack_forget()
        self.next_button.pack_forget()
        self.select_button.pack_forget()

        # Pack processing buttons
        self.rotate_button.pack(pady=10)
        self.grayscale_button.pack(pady=10)
        self.show_original_button.pack(pady=10)
        self.save_button.pack(pady=10)

        # Show the selected image
        self.display_image_in_label(self.processed_image)

    def load_images(self):
        """Load image paths from a selected directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.image_paths = [os.path.join(directory, f) for f in os.listdir(directory)
                                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if not self.image_paths:
                messagebox.showinfo("Info", "No images found in this directory.")
            else:
                self.current_image_index = 0
                self.current_image_path = self.image_paths[self.current_image_index]
                self.show_image(self.current_image_path)

    def load_image(self, image_path):
        """Load an image from the given path."""
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            return None

    def display_image_in_label(self, image):
        """Display the given PIL Image in the image label."""
        if image:
            img_resized = image.resize((500, 500))
            img_tk = ImageTk.PhotoImage(img_resized)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Keep a reference

    def show_image(self, image_path):
        """Load and display the image from the given path."""
        image = self.load_image(image_path)
        if image:
            self.display_image_in_label(image)

    def next_image(self):
        """Navigate to the next image."""
        if self.image_paths:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.current_image_path = self.image_paths[self.current_image_index]
            self.show_image(self.current_image_path)
        else:
            messagebox.showwarning("No Images", "No images loaded. Please load images first.")

    def previous_image(self):
        """Navigate to the previous image."""
        if self.image_paths:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.current_image_path = self.image_paths[self.current_image_index]
            self.show_image(self.current_image_path)
        else:
            messagebox.showwarning("No Images", "No images loaded. Please load images first.")

    def select_image(self):
        """Select the current image for processing."""
        if self.image_paths:
            self.current_image_path = self.image_paths[self.current_image_index]
            self.original_image = self.load_image(self.current_image_path)
            if self.original_image:
                self.processed_image = self.original_image.copy()
                messagebox.showinfo("Image Selected", f"Selected image:\n{self.current_image_path}")
                self.setup_processing_gui()
        else:
            messagebox.showwarning("No Image", "No image selected. Please select an image.")

    def rotate_image(self):
        """Rotate the processed image by 90 degrees."""
        if self.processed_image:
            self.processed_image = self.processed_image.rotate(90, expand=True)
            self.display_image_in_label(self.processed_image)
        else:
            messagebox.showwarning("No Image", "No image loaded. Please select an image.")

    def convert_to_grayscale(self):
        """Convert the processed image to grayscale."""
        if self.processed_image:
            self.processed_image = ImageOps.grayscale(self.processed_image)
            self.display_image_in_label(self.processed_image)
        else:
            messagebox.showwarning("No Image", "No image loaded. Please select an image.")

    def show_original_image(self):
        """Revert to the original image."""
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_image_in_label(self.processed_image)
        else:
            messagebox.showwarning("No Original Image", "No original image available.")

    def save_image(self):
        """Save the processed image to a file."""
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Image Saved", f"Image has been saved at: {file_path}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("No Image", "No image to save. Please edit an image first.")


if __name__ == '__main__':
    root = tk.Tk()
    app = ImageGUI(root)
    root.mainloop()
