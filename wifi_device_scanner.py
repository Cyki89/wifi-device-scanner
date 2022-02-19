import os
import time
from scapy.all import ARP, Ether, srp
from datetime import datetime


HOUR_IN_SEC = 3600
MINUTE_IN_SEC = 60

IP_NETWORK_RANGE = '<YourNetworkId>/<range>' #'192.168.1.1/24'
IP_DEVICE = '<YourNetworkId>' #'192.168.1.116'
YOUTUBE_MUSIC_URL = '<YotubeUrl>' #'https://www.youtube.com/watch?v=nIso825-Ko4'
PROJECT_PATH = '<YourProjectPath>' #'C:/Users/admin/Desktop/apps/wifi_device_scanner'

SLEEPING_START_HOUR = 1
SLEEPING_END_HOUR = 8


def get_curr_hour():
    return datetime.now().hour


def is_sleeping_time(curr_hour):
    return SLEEPING_START_HOUR <= curr_hour < SLEEPING_END_HOUR


def calculate_time_to_start():
    curr_time = datetime.now()
    start_time = get_starting_app_time(curr_time)

    return (start_time - curr_time).total_seconds()


def get_starting_app_time(curr_time):
    time_kwargs = {
        'year': curr_time.year,
        'month': curr_time.month,
        'day': curr_time.day,
        'hour': SLEEPING_END_HOUR     
    }

    return datetime(**time_kwargs)


def get_ip_devices():
    arp = ARP(pdst=IP_NETWORK_RANGE)
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether/arp

    result = srp(packet, timeout=10, verbose=0)[0]

    return [received.psrc for _, received in result]


def is_device_connected(): 
    return IP_DEVICE in get_ip_devices()


def do_initial_tasks():
    # Here you can put tasks that should run when your device will be within Wi-Fi range
    open_project_in_vscode(PROJECT_PATH)
    open_page_in_chrome(YOUTUBE_MUSIC_URL)


def open_page_in_chrome(url):
    os.system(f'start chrome {url}')


def open_project_in_vscode(path):
    os.system(f'code {path}')


def main():
    device_connected = False

    while True:
        if is_sleeping_time(get_curr_hour()):
            device_connected = False
            sleep_time = calculate_time_to_start()

        elif device_connected:
            device_connected = is_device_connected()
            sleep_time = HOUR_IN_SEC
        
        else:
            device_connected = is_device_connected()
            if device_connected:
                do_initial_tasks()

            sleep_time = HOUR_IN_SEC if device_connected else MINUTE_IN_SEC
        
        # Of course, you should adjust the sleep time and the logic of main fucntion base to your preferences
        time.sleep(sleep_time)

        
if __name__ == '__main__':
    main()
