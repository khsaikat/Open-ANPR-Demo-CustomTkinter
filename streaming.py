import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image
import cv2


def camera_app(self):
        ret, img = cap.read()
        cv2image= cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        #ImgTks = ImageTk.PhotoImage(image=img)
        image_wc = ctk.CTkImage(img, size=(640, 480))
        #self.camera.imgtk = ImgTks
        self.camera.configure(image=image_wc)
        self.after(20, self.camera_app)