import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
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

        self.image_object = None  # Menyimpan objek gambar yang aktif

        self.root.title("Menampilkan Gambar dari Direktori")
        self.root.geometry("600x700")

        self.welcomeGUI()

    def welcomeGUI(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        # Tombol untuk memuat gambar dari direktori
        self.load_button = tk.Button(self.root, text="Pilih Direktori Gambar", command=self.load_images)
        self.load_button.pack(pady=10)

        # Tombol untuk navigasi gambar
        self.prev_button = tk.Button(self.root, text="Sebelumnya", command=self.previous_image)
        self.prev_button.pack(side=tk.LEFT, padx=20)

        self.next_button = tk.Button(self.root, text="Berikutnya", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        # Tombol untuk memilih gambar saat ini
        self.select_button = tk.Button(self.root, text="Pilih Gambar Ini", command=self.select_image)
        self.select_button.pack(pady=20)

    def updateGUI(self):
        self.load_button.pack_forget()
        self.prev_button.pack_forget()
        self.next_button.pack_forget()
        self.select_button.pack_forget()

        # Menggunakan lambda untuk memanggil fungsi ketika tombol ditekan
        self.rotate_button = tk.Button(self.root, text="Rotasi", command=lambda: self.rotate_image())
        self.rotate_button.pack(pady=20)
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
            self.image_object = Image.open(path)  # Menyimpan gambar asli
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
            self.updateGUI()
        else:
            messagebox.showwarning("Belum ada gambar!", "Belum ada gambar yang dipilih, coba pilih!")

    def rotate_image(self):
        if self.image_object:  # Memastikan ada gambar yang diputar
            self.image_object = self.image_object.rotate(90, expand=True)  # Menyimpan perubahan rotasi
            img_tk = ImageTk.PhotoImage(self.image_object.resize((500, 500)))
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
