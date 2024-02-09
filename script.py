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
        home_icon = self.get_icon("C:/Users/ALEXANDREA/GUI/assets/home.png")
        info_icon = self.get_icon("C:/Users/ALEXANDREA/GUI/assets/info.png")
        help_icon = self.get_icon("C:/Users/ALEXANDREA/GUI/assets/question.png")

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
        title_label = ttk.Label(self.home_frame, text="Knee OA Severity Scanner", font=("Helvetica", 50, 'bold'), style="Title.TLabel")
        title_label.pack(pady=100)

        start_button = ttk.Button(self.home_frame, text="Start", command=self.open_camera, style="PrimaryButton.TButton")
        start_button.pack()

    def open_camera(self):
        for widget in self.home_frame.winfo_children():
            widget.destroy()
        
        # Create a top frame for the back button and camera frame
        top_frame = tk.Frame(self.home_frame)
        top_frame.pack(fill="x", expand=False)
        
        back_button = ttk.Button(top_frame, text="Back", command=self.show_home_page, style="TertiaryButton.TButton")
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        self.camera_frame = ttk.Frame(top_frame, style="TFrame")
        self.camera_frame.grid(row=0, column=1, padx=10, pady=10)
        
        self.camera_view_frame = tk.Frame(self.camera_frame)
        self.camera_view_frame.pack(expand=True, fill="both", padx=150, pady=10)
        
        self.button_frame = tk.Frame(self.camera_frame)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  # Adjust width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)  # Adjust height
        
        self.video_label = tk.Label(self.camera_view_frame)
        self.video_label.pack(expand=True, fill="both")
        
        self.video_label.bind(self.update_camera_feed)

        self.capture_button = ttk.Button(self.button_frame, text="Capture", command=self.take_picture, style="PrimaryButton.TButton")
        self.capture_button.pack(side="bottom", padx=10)
        
        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_image, style="PrimaryButton.TButton")
        self.retry_button = ttk.Button(self.button_frame, text="Retry", command=self.retry_capture, style="SecondaryButton.TButton")
        
        self.update_camera_feed()


    def show_home_page(self):
        for widget in self.home_frame.winfo_children():
            widget.destroy()
        self.create_home_page()


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
            frame = frame.resize((700, 500), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=frame)

            self.video_label.configure(image=photo)
            self.video_label.image = photo
        
        self.video_label.after(10, self.update_camera_feed)

    def display_captured_image(self, frame):
        self.cap.release()
        cv2.destroyAllWindows()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((600, 1000))
        photo = ImageTk.PhotoImage(image=image)

        self.video_label.configure(image=photo)
        self.video_label.image = photo

        self.save_button.pack(side="left", padx=10, pady=10)  # Adjust padding as needed
        self.retry_button.pack(side="right", padx=10, pady=10)

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
    root.attributes('-fullscreen', True)
    root.configure(background='light blue')
    style = ttk.Style(root)
    style.theme_use("clam")

    # Configure the general frame and label styles
    style.configure("TFrame", background="#f0f0f0")
    style.configure("Title.TLabel", background="#f0f0f0", padding=20)

    # Configure the button styles
    style.configure("PrimaryButton.TButton", font=('Helvetica', 30, 'bold'), background="#789dc4", foreground="#ffffff", padding=50,
                    hoverbackground="#48719e")
    style.configure("SecondaryButton.TButton", font=('Helvetica', 30, 'bold'), background="#e6a9ac", foreground="#ffffff", padding=50,
                    hoverbackground="#c89671")
    style.configure("TertiaryButton.TButton", font=('Helvetica', 20, 'bold'), background="#e6a9ac", foreground="#ffffff", padding=30,
                    hoverbackground="#c89671")


    # Correctly set the margins around the tabs to make them larger
    style.configure("TNotebook.Tab", font=('default', 20, 'bold'), padding=[50, 15], sticky="NSEW")
    # Ensure active tabs have the same padding, potentially increase it to match your needs
    style.map("TNotebook.Tab", padding=[("selected", [50, 15])])
        
    # Initialize the app and set the window size
    app = CameraApp(root)
    root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.mainloop()

if __name__ == "__main__":
    main()