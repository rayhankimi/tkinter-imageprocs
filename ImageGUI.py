import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import os


class ImageGUI:
    def __init__(self, root):
        self.root = root
        self.selected_image = None
        self.image_paths = []
        self.current_image_index = 0

        self.image_label = None
        self.load_button = None
        self.prev_button = None
        self.next_button = None
        self.select_button = None

        self.rotate_button = None
        self.monochrome_button = None
        self.save_button = None
        self.show_original_button = None

        self.image_object = None  # Save active picture
        self.original_image = None  # Save original picture

        self.root.title("Image Processing")
        self.root.geometry("600x700")

        self.welcomeGUI()

    def welcomeGUI(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        # Tombol untuk memuat gambar dari direktori
        self.load_button = tk.Button(self.root, text="Select a picture directory...", command=self.load_images)
        self.load_button.pack(pady=10)

        # Tombol untuk navigasi gambar
        self.prev_button = tk.Button(self.root, text="Previous", command=self.previous_image)
        self.prev_button.pack(side=tk.LEFT, padx=20)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        # Tombol untuk memilih gambar saat ini
        self.select_button = tk.Button(self.root, text="Select this", command=self.select_image)
        self.select_button.pack(pady=20)

    def updateGUI(self):
        self.load_button.pack_forget()
        self.prev_button.pack_forget()
        self.next_button.pack_forget()
        self.select_button.pack_forget()

        self.rotate_button = tk.Button(self.root, text="Rotate", command=lambda: self.rotate_image())
        self.rotate_button.pack(pady=20)

        self.monochrome_button = tk.Button(self.root, text="B&W", command=lambda: self.bnw_image())
        self.monochrome_button.pack(pady=20)
        
        self.show_original_button = tk.Button(self.root, text="Show Original Image", command=self.show_original_image)
        self.show_original_button.pack(pady=20)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=20)

        self.show_image(self.selected_image)

    def load_images(self):
        # Membuka dialog untuk memilih direktori
        directory = filedialog.askdirectory()
        if directory:
            # Mencari semua file gambar dalam direktori
            self.image_paths = [os.path.join(directory, f) for f in os.listdir(directory)
                                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if not self.image_paths:
                messagebox.showinfo("Info", "Tidak ada gambar di direktori ini.")
            else:
                self.current_image_index = 0
                self.show_image(self.image_paths[self.current_image_index])

    def show_image(self, path):
        try:
            self.image_object = Image.open(path)  
            img = self.image_object.resize((500, 500))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat gambar: {e}")

    def next_image(self):
        if self.image_paths:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.show_image(self.image_paths[self.current_image_index])

    def previous_image(self):
        if self.image_paths:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.show_image(self.image_paths[self.current_image_index])

    def select_image(self):
        if self.image_paths:
            self.selected_image = self.image_paths[self.current_image_index]
            messagebox.showinfo("Gambar Dipilih", f"Gambar berikut dipilih:\n{self.selected_image}")
            self.original_image = Image.open(self.selected_image)
            self.updateGUI()
        else:
            messagebox.showwarning("Belum ada gambar!", "Belum ada gambar yang dipilih, coba pilih!")

    def rotate_image(self):
        if self.image_object:
            self.image_object = self.image_object.rotate(90, expand=True)  # Menyimpan perubahan rotasi
            img_tk = ImageTk.PhotoImage(self.image_object.resize((500, 500)))
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

    def bnw_image(self):
        if self.image_object:
            self.image_object = ImageOps.grayscale(self.image_object)
            img_tk = ImageTk.PhotoImage(self.image_object.resize((500, 500)))
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
    
    def show_original_image(self):
        if self.image_object:
            self.image_object = self.original_image
            img_tk = ImageTk.PhotoImage(self.image_object.resize((500, 500)))
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

    def save_image(self):
        if self.image_object:
            # Membuka dialog save file
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                try:
                    # Menyimpan gambar saat ini ke path yang dipilih
                    self.image_object.save(file_path)
                    messagebox.showinfo("Image Saved", f"Image has been saved at: {file_path}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("No Image", "No image to save. Please edit an image first.")
