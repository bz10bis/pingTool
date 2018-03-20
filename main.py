import time
import os
import sys
import socket
import subprocess
from random import randint
import threading
from tkinter import *


class Ping(object):
    def __init__(self, master, config):
        self.count = 0
        self.min_ip = 100
        self.max_ip = 0
        self.avg_ip = 0
        self.signal_list = list()
        self.max_size = config["width"]
        self.w_height = config["height"]
        self.w_width = config["width"]
        self.canvas = Canvas(master, width=self.w_width, height=self.w_height, background="blue")
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.create_text(10, 5, text="Min:", font="Arial 6", fill="white")
        self.label_min_ip = self.canvas.create_text(15, 5, text="Min: 0", font="Arial 8", fill="white")
        self.label_max_ip = self.canvas.create_text(15, 14, text="Max: 0", font="Arial 8", fill="white")
        self.label_avg_ip = self.canvas.create_text(15, 23, text="Moy: 0", font="Arial 8", fill="white")
        self.label_current_ip = self.canvas.create_text(10, 32, text="Curr: 0", font="Arial 6", fill="white")
        self.offset = 0
        self.speed = 100
        self.update()

    def update(self):
        # ping_value = randint(0, 9) * 10
        ping_value = self.do_a_ping("192.168.1.82", 80)
        ping_value = round(ping_value * 1000)
        if self.count < 10000:
            if ping_value < self.min_ip:
                self.min_ip = ping_value
            elif ping_value > self.max_ip:
                self.max_ip = ping_value

            self.signal_list.append(ping_value)
            if len(self.signal_list) >= self.max_size:
                del self.signal_list[-1]
            self.avg_ip = round(sum(self.signal_list) / len(self.signal_list))
            self.canvas.itemconfigure(self.label_min_ip, text="Min: {}".format(str(self.min_ip)))
            self.canvas.itemconfigure(self.label_max_ip, text="Max: {}".format(str(self.max_ip)))
            self.canvas.itemconfigure(self.label_avg_ip, text="Avg: {}".format(str(self.avg_ip)))
            self.canvas.itemconfigure(self.label_current_ip, text="Cur: {}".format(str(ping_value)))
            self.canvas.after(self.speed, self.update)
            x0 = self.w_width - self.count
            y0 = self.w_height - (ping_value + 30)
            x1 = self.w_width - self.count
            y1 = self.w_height
            color = "white"
            if ping_value > 1000:
                ping_value = 9999
                color = "red"
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            self.count += 1
            print(self.count)

    def do_a_ping(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s_start = time.time()
        success = False
        try:
            s.connect((host, int(port)))
            s.shutdown(socket.SHUT_RD)
            success = True
        except socket.timeout:
            print("timeout")
        except OSError as e:
            print("Os Error: {}".format(e))
        s_stop = time.time()
        if success:
            elapse_time = s_stop - s_start
        else:
            elapse_time = 9999
        return elapse_time


if __name__ == '__main__':
    print("Python Ping")
    config = {
        "width": 400,
        "height": 150
    }
    root = Tk()
    Ping(root, config)
    root.mainloop()
