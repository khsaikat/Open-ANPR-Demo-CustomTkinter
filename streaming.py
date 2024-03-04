# import customtkinter as ctk
# from customtkinter import filedialog
# from PIL import Image
# import cv2
from reolink_aio.api import Host
import asyncio


rtsp_url = 'rtsp://:@:/h264Preview_01_main'

IP_ADDRESS = '192.168.1.152'
PORT = 554
USERNAME = 'admin'
PASSWORD = 'Katma2023'


async def print_mac_address():
    # initialize the host
    host = Host(IP_ADDRESS, PORT, USERNAME, PASSWORD)
    # connect and obtain/cache device settings and capabilities
    await host.get_host_data()
    # check if it is a camera or an NVR
    print("It is an NVR: %s, number of channels: %s", host.is_nvr, host.num_channels)
    # print mac address
    print(host.mac_address)
    # close the device connection
    await host.logout()

if __name__ == "__main__":
    asyncio.run(print_mac_address())
                

