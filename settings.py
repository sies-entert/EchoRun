import pygame
import json

class Config():
    def __init__(self, config = "config.json"):
        self.config = config
        self.settings = self.load_config()
        
    def load_config(self):
        try:
            with open(self.config, "r") as o:
                settings = json.load(o)
                print("Loaded Config:", settings)
                print("Current type", type(settings))
                return settings
        except:
            return self.default_config()

    def save_config(self):
        with open(self.config, "w") as f:
            json.dump(self.settings, f, indent=4)
            
    def update_settings(self, key, value):
        keys = key.split(".")
        settings = self.settings
        
        for a in keys[:-1]:
            settings = settings[a]
        settings[keys[-1]] = value
        
        self.save_config()
        
    def default_config(self):
        self.settings = {
            "window_mode": {
                "fullscreen": "fullscreen"
            },
            "resolution": {
                "wsvga": [1024, 576],
                "hd": [1280, 720],
                "fwxga": [1366, 768],
                "wsxga": [1600, 900],
                "fullhd": [1920, 1080]
            },
            "font_size": {
                "fwsvga": 20,
                "fhd": 30,
                "ffwxga": 40,
                "fwsxga": 50,
                "ffullhd": 60
            },
            "button_size": {
                "bwsvga": [150, 50],
                "bhd": [175, 59],
                "bfwxga": [200, 68],
                "bwsxga": [225, 75],
                "bfullhd": [250, 83]
            },
            "line_size": {
                "lwsvga": [300, 50],
                "lhd": [325, 59],
                "lfwxga": [350, 68],
                "lwsxga": [375, 75],
                "lfullhd": [400, 83]
            },
            "current_window_mode": "fullscreen",
            "current_resolution": "fullhd",
            "font_resolution": "ffullhd",
            "button_WuH": "bfullhd",
            "line_WuH": "lfullhd",
            "theme": "light",
            "themes": {
                "dark": {
                    "SCREENBACKGROUND": [5, 5, 5],
                    "MENUBACKGROUND": [0, 0, 0],
                    "FONTCOLOR": [255, 255, 255],
                    "BUTTONBACK": [0, 0, 0],
                    "BUTTONOUTLINE": [255, 255, 255]
                },
                "light": {
                    "SCREENBACKGROUND": [254, 254, 254],
                    "MENUBACKGROUND": [255, 255, 255],
                    "FONTCOLOR": [0, 0, 0],
                    "BUTTONBACK": [255, 255, 255],
                    "BUTTONOUTLINE": [0, 0, 0]
                }
            }
        }