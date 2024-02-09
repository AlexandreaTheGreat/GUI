import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
import os
import cv2

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Knee OA Severity Scanner")
        self.captured_frame = None

        # Store icons in a dictionary
        self.icons = {}

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.home_frame = ttk.Frame(self.notebook)
        self.help_frame = ttk.Frame(self.notebook)
        self.info_frame = ttk.Frame(self.notebook)

        # Load icons and add tabs without text labels
        home_icon = self.get_icon("C:/Users/ALEXANDREA/Downloads/home.png")
        info_icon = self.get_icon("C:/Users/ALEXANDREA/Downloads/info.png")
        help_icon = self.get_icon("C:/Users/ALEXANDREA/Downloads/question.png")

        self.notebook.add(self.home_frame, text="Home", image=home_icon, compound="left")
        self.notebook.add(self.help_frame, text="Info", image=info_icon, compound="left")
        self.notebook.add(self.info_frame, text="Help", image=help_icon, compound="left")

        self.create_home_page()

    def get_icon(self, filename):
        icon_size = (30, 30)  # Define a standard icon size for all tabs
        icon = Image.open(filename).resize(icon_size, Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(icon)
        # Store the PhotoImage to prevent garbage collection
        self.icons[filename] = photo_image
        return photo_image

    def create_home_page(self):
        title_label = ttk.Label(self.home_frame, text="Knee OA Severity Scanner", font=("Helvetica", 18), style="Title.TLabel")
        title_label.pack(pady=(20, 50))

        start_button = ttk.Button(self.home_frame, text="Start", command=self.open_camera, style="PrimaryButton.TButton")
        start_button.pack()

    def open_camera(self):
        for widget in self.home_frame.winfo_children():
            widget.destroy()

        self.camera_frame = ttk.Frame(self.home_frame, style="TFrame")
        self.camera_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

        self.video_label = tk.Label(self.camera_frame)
        self.video_label.pack()
        
        self.capture_button = ttk.Button(self.camera_frame, text="Capture", command=self.take_picture, style="PrimaryButton.TButton")
        self.capture_button.pack(pady=20)

        # Define save and retry buttons but don't pack them yet
        self.save_button = ttk.Button(self.camera_frame, text="Save", command=self.save_image, style="PrimaryButton.TButton")
        self.retry_button = ttk.Button(self.camera_frame, text="Retry", command=self.retry_capture, style="SecondaryButton.TButton")

        self.update_camera_feed()


    def take_picture(self):
        ret, frame = self.cap.read()
        if ret:
            self.captured_frame = frame  # Store the frame
            self.display_captured_image(frame)
            self.capture_button.pack_forget()
            

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame.thumbnail((300, 200))
            photo = ImageTk.PhotoImage(image=frame)

            self.video_label.configure(image=photo)
            self.video_label.image = photo
        
        self.video_label.after(10, self.update_camera_feed)

    def display_captured_image(self, frame):
        self.cap.release()
        cv2.destroyAllWindows()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image=image)

        self.video_label.configure(image=photo)
        self.video_label.image = photo

        save_button = ttk.Button(self.camera_frame, text="Save", command=self.save_image, style="PrimaryButton.TButton")
        save_button.pack(side="left", padx=20)
        retry_button = ttk.Button(self.camera_frame, text="Retry", command=self.retry_capture, style="SecondaryButton.TButton")
        retry_button.pack(side="right", padx=20)

    def save_image(self):
        if self.captured_frame is not None:
            file_path = os.path.abspath("C:/Users/ALEXANDREA/Downloads/captured_image.jpg")
            # Use the stored frame
            image = Image.fromarray(cv2.cvtColor(self.captured_frame, cv2.COLOR_BGR2RGB))
            image.save(file_path)
            messagebox.showinfo("Image Saved", f"Image saved successfully at:\n{file_path}")
        else:
            messagebox.showerror("Save Error", "No image captured to save.")

    def retry_capture(self):
        self.camera_frame.destroy()
        self.open_camera()

def main():
    root = tk.Tk()
    root.configure(background='light blue')
    style = ttk.Style(root)
    style.theme_use("clam")

    # Configure the general frame and label styles
    style.configure("TFrame", background="#f0f0f0")
    style.configure("Title.TLabel", background="#f0f0f0")

    # Configure the button styles
    style.configure("PrimaryButton.TButton", background="#789dc4", foreground="#ffffff", padding=10,
                    hoverbackground="#48719e")
    style.configure("SecondaryButton.TButton", background="#e6a9ac", foreground="#ffffff", padding=10,
                    hoverbackground="#c89671")

    # Configure the notebook itself - this sets the tab position and overall padding around the tabs
    style.configure("LeftTab.TNotebook", tabposition="wn")

    # Correctly set the margins around the tabs to make them larger
    style.configure("TNotebook.Tab", font=('default', 12, 'bold'))

    # Initialize the app and set the window size
    app = CameraApp(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()
