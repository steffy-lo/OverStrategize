# coding=utf-8

import math
import glfw
import win32gui
import win32con

from OpenGL.GL import *
from OpenGL.GLUT import *
import keyboard as kb

from PIL import Image
import numpy as np
import random


class FullScreenOverlay:
    def __init__(self):
        glfw.init()
        glutInit()
        self.video_mode, self.window = self.__create_window()

        self.width = self.video_mode.size.width
        self.height = self.video_mode.size.height

        self.mid = self.video_mode.size.width / 2, self.video_mode.size.height / 2
        self.corner = {
            "lower_left": (0, 0),
            "lower_right": (self.width, 0),
            "upper_left": (0, self.height),
            "upper_right": (self.width, self.height)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        glfw.terminate()

    def __create_window(self):
        # glfw
        glfw.window_hint(glfw.DECORATED, 0)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, 1)
        glfw.window_hint(glfw.FLOATING, 1)
        glfw.window_hint(glfw.SAMPLES, 14)
        video_mode = glfw.get_video_mode(glfw.get_primary_monitor())
        window = glfw.create_window(
            video_mode.size.width - 1,
            video_mode.size.height - 1,
            "Overlay", None, None
        )
        glfw.make_context_current(window)

        # ws_ex_transparent
        hwnd = glfw.get_win32_window(window)
        win32gui.SetWindowLong(
            hwnd, win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT
        )

        # opengl
        glInitGl46VERSION()
        glOrtho(0, video_mode.size.width, 0, video_mode.size.height, -1, 1)

        return video_mode, window

    @property
    def loop(self):
        return kb.is_pressed("tab") and not glfw.window_should_close(self.window)

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)


class Draw:
    red = (250, 0, 0)
    green = (0, 250, 0)
    blue = (0, 0, 250)
    black = (0, 0, 0)
    white = (250, 250, 250)
    alert = (0.92, 0.3, 0.25)
    cyan = (0.1, 0.7, 0.95)

    @staticmethod
    def line(x1, y1, x2, y2, line_width, color=None):
        glLineWidth(line_width)
        glBegin(GL_LINES)
        glColor3f(*color)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    @staticmethod
    def dashed_line(x1, y1, x2, y2, line_width, color, factor=2, pattern="11111110000"):
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(factor, int(pattern, 2))
        glLineWidth(line_width)
        glEnable(GL_LINE_STIPPLE)

        glBegin(GL_LINES)
        glColor3f(*color)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        glPopAttrib()

    @staticmethod
    def outline(x, y, width, height, line_width, color):
        glLineWidth(line_width)
        glBegin(GL_LINE_LOOP)
        glColor3f(*color)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    @staticmethod
    def alpha_box(x, y, width, height, color, alpha=0.5):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_POLYGON)
        glColor4f(*color, alpha)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        glDisable(GL_BLEND)

    @staticmethod
    def circle(x, y, radius, color, filled=True):
        glBegin(GL_POLYGON if filled else GL_LINE_LOOP)
        glColor3f(*color)
        for i in range(360):
            glVertex2f(
                math.cos(math.radians(i)) * radius + x,
                math.sin(math.radians(i)) * radius + y
            )
        glEnd()

    @staticmethod
    def text(x, y, color, text, font=GLUT_BITMAP_HELVETICA_18):
        glColor3f(*color)
        glWindowPos2f(x, y)
        [glutBitmapCharacter(font, ord(ch)) for ch in text]

    @staticmethod
    def display_image(image_file, posX, posY):
        img = Image.open(image_file)
        # img = img.resize((100, 100))
        img = img.convert('RGBA')
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        width, height = img.size
        image_data = np.zeros(shape=(height, width, 4))
        for y in range(height):
            for x in range(width):
                rgba = list(img.getpixel((x, y)))
                if rgba[:3] != [0, 255, 0] and rgba[:3] != [0, 0, 0]:
                    image_data[y][x] = [0, 0, 0, 0]
                else:
                    image_data[y][x] = rgba
        glRasterPos2f(posX, posY)
        glDrawPixels(width, height, GL_RGBA, GL_FLOAT, image_data)
