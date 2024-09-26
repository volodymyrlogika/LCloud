from kivy.lang  import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
import requests
from settings import *


class WeatherScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_weather(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(CURRENT_WEATHER_URL, params)
        response = data.json()
        print(response)
        return response
    
    def search(self):
        city = self.ids.city.text
        weather = self.get_weather(city)
        
        temp = weather["main"]["temp"]
        self.ids.temp.text = f"{round(temp)}°C"
        



class LCloudApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"

        return WeatherScreen()


LCloudApp().run()