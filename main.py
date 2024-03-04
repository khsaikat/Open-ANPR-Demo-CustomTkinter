import customtkinter as ctk
from customtkinter import filedialog
import os
import threading
import shutil
import subprocess
import time
import json
import numpy as np
import cv2
from PIL import Image


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

WIDTH = 1024
HEIGHT = 750

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.window_setup()
        self.load_image_setup()

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  ANPR-KC", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # populate navigation frame
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Image",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Stream",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(2, weight=1)
        self.home_frame.grid_rowconfigure(3, weight=1)

        self.home_frame_image_to_predict = ctk.CTkLabel(self.home_frame, text="", image=self.placeholder_predict_image)
        self.home_frame_image_to_predict.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        self.home_frame_upload_image_button = ctk.CTkButton(self.home_frame, text="Upload Image", command=self.upload_image_button_event)
        self.home_frame_upload_image_button.grid(row=1, column=0, padx=40, pady=10, sticky='w')
        self.home_frame_detect_button = ctk.CTkButton(self.home_frame, text="Detect Number Plate", command=self.predict_plate_button_event)
        self.home_frame_detect_button.grid(row=1, column=0, padx=40, pady=10, sticky='e')
        self.home_frame_result_log = ctk.CTkTextbox(self.home_frame, width=600)
        self.home_frame_result_log.grid(row=2, column=0, padx=20, pady=10, sticky='sw')
        self.home_frame_result_log.insert("0.0", f"OpenALPR Demo...\n\n")

        # create second frame
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(2, weight=1)
        self.second_frame.grid_rowconfigure(3, weight=1)

        self.second_frame_image_to_predict = ctk.CTkLabel(self.second_frame, text="", image=self.placeholder_video_image)
        self.second_frame_image_to_predict.grid(row=0, column=0, padx=20, pady=10, sticky='w')

        self.second_frame_start_streaming_button = ctk.CTkButton(self.second_frame, text="Start Streaming", command=self.start_streaming_button_event)
        self.second_frame_start_streaming_button.grid(row=1, column=0, padx=40, pady=10, sticky='w')

        self.second_frame_stop_streaming_button = ctk.CTkButton(self.second_frame, text="Stop Streaming", command=self.stop_streaming_button_event)
        self.second_frame_stop_streaming_button.grid(row=1, column=0, padx=40, pady=10, sticky='e')

        self.second_frame_detect_button = ctk.CTkButton(self.second_frame, text="Detect Number Plate", command=lambda: threading.Thread(target=self.predict_plate_from_stream_button_event).start())                                                                                                 
        self.second_frame_detect_button.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.second_frame_result_log = ctk.CTkTextbox(self.second_frame, width=600)
        self.second_frame_result_log.grid(row=2, column=0, padx=20, pady=10, sticky='sw')
        self.second_frame_result_log.insert("0.0", f"OpenALPR Demo...\n\n")
        
        # select default frame
        self.select_frame_by_name("home")

    def upload_image_button_event(self):
        
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select an Image",
            filetypes=[("Image files", ".png .jpg .jpeg")],
        )
        
        filename = os.path.basename(file_path)
        uploaded_path = os.path.join(self.image_path, os.path.join("uploads", filename))
        shutil.copy(file_path, uploaded_path)
        my_height = 400
        img = Image.open(uploaded_path)
        h_percent = (my_height/float(img.size[1]))
        w_size = int((float(img.size[0])*float(h_percent)))      
        if w_size > 600:
            w_size = 600
        new_image = ctk.CTkImage(img, size=(w_size, my_height))
        self.home_frame_image_to_predict.configure(image=new_image)

    def start_streaming_button_event(self):
        video_in = "./videos/night_test_2_short.mp4"
        rtsp_url = 'rtsp://admin:Katma2023@192.168.178.133:554/h264Preview_01_main'
        self.capture = cv2.VideoCapture(rtsp_url)
        self.camera_app()

    def stop_streaming_button_event(self):
        pass

    def predict_plate_from_stream_button_event(self):
        alpr = "C:/openalpr_64/alpr.exe"
        img = self.second_frame_image_to_predict.cget('image').cget('light_image')
        img_np = np.array(img)
        cv2.imwrite(os.path.join(self.image_path, "tmp_img.png"), img_np)
        
        start_ocr_time = time.time()

        process = subprocess.Popen(f"{alpr} -c eu -j ./images/tmp_img.png", stdout=subprocess.PIPE, shell=True)
        (output, err) = process.communicate()

        output_text = output.decode("utf-8")
        
        start_index = output_text.find('{')
        json_text = output_text[start_index:]

        try:
            data = json.loads(json_text)
            if 'results' in data and len(data['results']) > 0:
                plate = data['results'][0]['plate']
                confidence = data['results'][0]['confidence']
                self.add_to_log_stream(f"Plate: {plate} - Confidence: {confidence}")
        
            else:
                self.second_frame_result_log.insert(ctk.END, f"No Results found.\n")
                #print("No Results found.")
                
        except json.decoder.JSONDecodeError as e:
            self.add_to_log_stream(f"JSONDecodeError: {e}")
            print("JSONDecodeError:", e)
        
        ocr_time = time.time() - start_ocr_time
        self.add_to_log_stream(f"alpr Elapsed Time: {ocr_time}\n")

    def predict_plate_button_event(self):
        alpr = "C:/openalpr_64/alpr.exe"
        file_name = self.home_frame_image_to_predict.cget('image').cget('light_image').filename
        
        start_ocr_time = time.time()

        process = subprocess.Popen(f"{alpr} -c eu -j {file_name}", stdout=subprocess.PIPE, shell=True)
        (output, err) = process.communicate()

        output_text = output.decode("utf-8")
        
        start_index = output_text.find('{')
        json_text = output_text[start_index:]

        try:
            data = json.loads(json_text)
            if 'results' in data and len(data['results']) > 0:
                plate = data['results'][0]['plate']
                confidence = data['results'][0]['confidence']
                self.add_to_log(f"Plate: {plate} - Confidence: {confidence}")
        
            else:
                self.home_frame_result_log.insert(ctk.END, f"No Results found.\n")
                #print("No Results found.")
                
        except json.decoder.JSONDecodeError as e:
            self.add_to_log(f"JSONDecodeError: {e}")
            print("JSONDecodeError:", e)
        
        ocr_time = time.time() - start_ocr_time
        self.add_to_log(f"alpr Elapsed Time: {ocr_time}\n")
        #print(f"alpr Elapsed Time: {ocr_time}\n")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def add_to_log(self, text):
        #self.home_frame_result_log.configure(state='normal')
        self.home_frame_result_log.insert(ctk.END, f"{text}\n")
        #self.home_frame_result_log.configure(state='disabled')
        self.home_frame_result_log.see("end")

    def add_to_log_stream(self, text):
        #self.home_frame_result_log.configure(state='normal')
        self.second_frame_result_log.insert(ctk.END, f"{text}\n")
        #self.home_frame_result_log.configure(state='disabled')
        self.second_frame_result_log.see("end")

    def camera_app(self):
        ret, img = self.capture.read()        
        if ret:
            cv2image= cv2.cvtColor(self.capture.read()[1], cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            image_wc = ctk.CTkImage(img, size=(640, 480))
            self.second_frame_image_to_predict.configure(image=image_wc)
        self.after(20, self.camera_app)

    def window_setup(self):
        self.title("ALPRv01")
        WIN_W = self.winfo_screenwidth()
        WIN_H = self.winfo_screenheight()
        pos_x = int(WIN_W/2 - WIDTH/2 + 50)
        pos_y = int(WIN_H/2 - HEIGHT/2 - 25)
        self.geometry(f"{WIDTH}x{HEIGHT}+{pos_x}+{pos_y}")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def load_image_setup(self):
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "logo.png")), size=(26, 26))
        self.placeholder_predict_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "placeholder.jpg")), size=(400, 400))
        self.placeholder_video_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "cctv_temp.jpg")), size=(640, 480))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "home_light.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(self.image_path, "add_user_light.png")), size=(20, 20))


if __name__ == "__main__":
    app = App()
    app.mainloop()
