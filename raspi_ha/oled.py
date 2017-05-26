import math
import time
import datetime
import lirc

import os.path
from PIL import Image

# from demo_opts import get_device
from luma.core.render import canvas
from luma.emulator.device import pygame as get_device

# IR connection
sockid = lirc.init("raspi_ha", blocking=False)
codeIR = None


def check_ir():
    global codeIR
    codeIR = lirc.nextcode()
    return codeIR


def ir_func(command):
    if command == 'channelup':
        raise NextExit
    elif command == 'channeldown':
        raise PrevExit


class NextExit(Exception):
    pass


class PrevExit(Exception):
    pass


class SplashMenu:
    def __init__(self):
        self.device = get_device()
        self.main()

    def __del__(self):
        self.device.clear()
        ClockMenu()

    def main(self):
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'images', 'pi_logo.png'))
        logo = Image.open(img_path).convert("RGBA")
        fff = Image.new(logo.mode, logo.size, (255,) * 4)

        background = Image.new("RGBA", self.device.size, "white")
        posn = ((self.device.width - logo.width) // 2, 0)

        for i in range(2):
            for angle in range(0, 360, 2):
                rot = logo.rotate(angle, resample=Image.BILINEAR)
                img = Image.composite(rot, fff, rot)
                background.paste(img, posn)
                self.device.display(background.convert(self.device.mode))
        del self


class ClockMenu:
    def __init__(self):
        self.device = get_device()
        self.main()

    def __del__(self):
        self.device.clear()

    @staticmethod
    def posn(angle, arm_length):
        dx = int(math.cos(math.radians(angle)) * arm_length)
        dy = int(math.sin(math.radians(angle)) * arm_length)
        return dx, dy

    def main(self):
        today_last_time = "Unknown"
        try:
            while True:
                if check_ir():
                    ir_func(codeIR[0])

                now = datetime.datetime.now()
                today_date = now.strftime("%d %b %y")
                today_time = now.strftime("%H:%M:%S")
                if today_time != today_last_time:
                    today_last_time = today_time
                    with canvas(self.device) as draw:
                        now = datetime.datetime.now()
                        today_date = now.strftime("%d %b %y")

                        margin = 4

                        cx = 30
                        cy = self.device.height / 2

                        left = cx - cy
                        right = cx + cy

                        hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
                        hrs = self.posn(cy - margin - 7)

                        min_angle = 270 + (6 * now.minute)
                        mins = self.posn(cy - margin - 2)

                        sec_angle = 270 + (6 * now.second)
                        secs = self.posn(cy - margin - 2)

                        draw.ellipse((left + margin, margin, right - margin, self.device.height - margin),
                                     outline="white")
                        draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill="white")
                        draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill="white")
                        draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="red")
                        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill="white", outline="white")
                        draw.text((2 * (cx + margin), cy - 8), today_date, fill="yellow")
                        draw.text((2 * (cx + margin), cy), today_time, fill="yellow")

                time.sleep(0.1)

        except NextExit:
            del self
            ind = menu_list.index(self.__class__)
            if ind == (len(menu_list) - 1):
                ind = 0
            else:
                ind += 1
            menu_list[ind]()

        except PrevExit:
            del self
            menu_list[menu_list.index(self.__class__) - 1]()


class RelayMenu:
    def __init__(self):
        pass


class AutoRelayMenu:
    def __init__(self):
        pass


class TorrentMenu:
    def __init__(self):
        pass


class MusicMenu:
    def __init__(self):
        pass


if __name__ == "__main__":
    menu_list = [ClockMenu, RelayMenu, AutoRelayMenu, TorrentMenu, MusicMenu]
    SplashMenu()
