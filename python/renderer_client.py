import time
import json
import threading

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from render.epd2in9 import EPD, EPD_WIDTH, EPD_HEIGHT

class RendererClient:

    # Initializer / Instance Attributes
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
        self.light = "Light"
        self.potentiometer = "Poten"
        self.led = "On"
        self.messages = []

        epd = EPD()
        epd.init(epd.lut_partial_update)
        self.epd = epd
        
        self.full_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)  # 255: clear the frame
        self.full_draw = ImageDraw.Draw(self.full_image)

        self.clear()
        render_client_thread = threading.Thread(target=self.draw_loop)
        render_client_thread.daemon = True
        render_client_thread.start()
        render_client_thread.join(20)
        


    def clear(self):
        self.full_draw.rectangle((0, 0, EPD_WIDTH, EPD_HEIGHT), fill = 0)
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(self.full_image, 0, 0)
        self.epd.display_frame()
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(self.full_image, 0, 0)
        self.epd.display_frame()
        self.full_draw.rectangle((0, 0, EPD_WIDTH, EPD_HEIGHT), fill = 255)
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(self.full_image, 0, 0)
        self.epd.display_frame()
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(self.full_image, 0, 0)
        self.epd.display_frame()

    def draw_loop(self):
        while (True):
            # Draw messages
            self.full_draw.rectangle([(0, 0), (EPD_WIDTH, EPD_HEIGHT)], fill = 255)
            i = 0
            self.messages = self.messages[-12:]
            for message in self.messages:
                self.full_draw.text((8, i * 14),  message.rstrip(), font = self.font, fill = 0)
                i += 1

            # # Draw info
            self.full_draw.line([(1, 168), (EPD_WIDTH, 168)], fill = 0, width = 2)
            self.full_draw.text((8, 168 + 46), "IP " + self.ip_address, font = self.font, fill = 0)
            self.full_draw.text((8, 168 + 60), "Time "  + time.strftime('%H:%M:%S'), font = self.font, fill = 0)
            self.full_draw.text((8, 168 + 74), "Led " + ("On" if self.led else "Off" ), font = self.font, fill = 0)
            self.full_draw.text((8, 168 + 88), self.light, font = self.font, fill = 0)
            self.full_draw.text((8, 168 + 102), self.potentiometer, font = self.font, fill = 0)

            self.epd.clear_frame_memory(0xFF)
            self.epd.set_frame_memory(self.full_image, 0, 0)
            self.epd.display_frame()
            self.epd.clear_frame_memory(0xFF)
            self.epd.set_frame_memory(self.full_image, 0, 0)
            self.epd.display_frame()

    def setMessage(self, message):
        self.messages.append(message)

    def setSensorData(self, sensorData):
        if (sensorData.startswith( 'Light')):
            self.light = sensorData.rstrip()
        elif (sensorData.startswith( 'Poten')):
            self.potentiometer = sensorData.rstrip()

    def setLed(self, value):
        self.led = value

    def getState(self):
        return json.dumps({
            'light': self.light,
            'potentiometer': self.potentiometer,
            'led': self.led
        }) 
