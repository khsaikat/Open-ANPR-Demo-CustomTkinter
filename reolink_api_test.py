from reolinkapi import Camera
import json


IP_ADDRESS = '192.168.1.152'
PORT = 554
USERNAME = 'admin'
PASSWORD = 'Katma2023'


if __name__ == "__main__":
    cam = Camera(IP_ADDRESS, USERNAME, PASSWORD)

    #alarm = cam.get_alarm_motion()
    #print(json.dumps(alarm, indent=2))
    #dst = cam.get_dst()
    #print(json.dumps(dst, indent=2))
    #rtsp_url = cam.get_users()
    print(json.dumps(cam.get_motion_files(), indent=2))
    
    