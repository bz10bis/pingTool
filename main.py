import time
import os
import sys
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
        self.label_min_ip = self.canvas.create_text(10, 5, text="Min:", font="Arial 6", fill="white")
        self.label_max_ip = self.canvas.create_text(10, 14, text="Max: 100", font="Arial 6", fill="white")
        self.label_avg_ip = self.canvas.create_text(10, 23, text="Moy: 21", font="Arial 6", fill="white")
        self.update()

    def update(self):
        ping_value = randint(0, 9) * 10
        print(ping_value)
        if self.count < 100:
            if ping_value < self.min_ip:
                self.min_ip = ping_value
            elif ping_value > self.max_ip:
                self.max_ip = ping_value

            self.signal_list.append(ping_value)
            if len(self.signal_list) >= self.max_size:
                del self.signal_list[-1]
            self.avg_ip = sum(self.signal_list) / len(self.signal_list)
            self.canvas.itemconfigure(self.label_min_ip, text="Min: {}".format(str(self.min_ip)))
            self.canvas.itemconfigure(self.label_max_ip, text="Max: {}".format(str(self.max_ip)))
            self.canvas.itemconfigure(self.label_avg_ip, text="Avg: {}".format(str(self.avg_ip)))
            self.canvas.after(300, self.update)
            self.draw_lines()
            self.count += 1
        #print(ping_value)
        #print(self.signal_list)

    def draw_lines(self):
        for i,s in enumerate(reversed(self.signal_list)):
            self.canvas.create_line(self.w_width - i, s, self.w_width - i, s, fill="white")
            print("i : {}".format(i))
            print("s : {}".format(s))

if __name__ == '__main__':
    print("Python Ping")
    config = {
        "width": 400,
        "height": 150
    }
    root = Tk()
    Ping(root, config)
    root.mainloop()
