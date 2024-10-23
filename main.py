from kivy.lang  import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard

import requests
from settings import *


class WeatherScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = 'Львів'

    def get_weather(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(CURRENT_WEATHER_URL, params)
        response = data.json()
        return response
    
    def search(self):
        try:
            self.city = self.ids.city.text
            weather = self.get_weather(self.city)
            # додаємо температуру у вікно
            temp = weather["main"]["temp"]
        except:
            # якщо не введено місто, показуємо погоду у Львові
            self.city = "Львів"
            weather = self.get_weather(self.city)

        # додаємо температуру у вікно
        temp = weather["main"]["temp"]
        self.ids.temp.text = f"{round(temp)}°C"
        # як відчувєаться температура 
        feels_like = weather["main"][ "feels_like"]
        self.ids.feels_like.text = f"Відчувається як {round(feels_like)}°C"
        # опис погоди
        desc = weather["weather"][0]["description"]
        self.ids.desc.text = desc.capitalize()
        # вологість повітря
        humidity = weather["main"]["humidity"]
        self.ids.humidity.text =  f"Вологість: {humidity}%"
        # швидкість вітру      
        wind = weather["wind"]["speed"]
        self.ids.wind.text =  f"Вітер: {wind} м/c"
        # картинка погоди
        icon = weather["weather"][0]["icon"]
        self.ids.icon.source = f'https://openweathermap.org/img/wn/{icon}@2x.png'

        # попередньо завантажимо прогноз погоди на інший екран
        forecast_data = self.forecast.get_forecast(self.city)
        self.forecast.show_forecast(forecast_data)
        #відображаємо панель з погодою 
        self.ids.weather_panel.opacity= 1
        

    def show_forecast(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'forecast'
        

class WeatherCard(MDCard):
    def __init__(self, weather, *args, **kwargs):
        super().__init__(*args, **kwargs)
        temp = weather["main"]["temp"]
        self.ids.temp.text = f"{round(temp)}°C"
        desc = weather["weather"][0]["description"]
        self.ids.desc.text = desc.capitalize()
        icon = weather["weather"][0]["icon"]
        self.ids.icon.source = f'https://openweathermap.org/img/wn/{icon}@2x.png'
        date_time = weather["dt_txt"]
        self.ids.date.text = f"{date_time[5:16]}"
        
class ForecastScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forecast = []

    def get_forecast(self, city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(FORECAST_URL, params)
        response = data.json()
        return response['list']
    
    def show_forecast(self, forecast):
        #додаємо картки з прогнозом погоди кожні 6 годин
        for i in range(0, len(forecast), 2):
            data = forecast[i]
            card = WeatherCard(data)
            self.ids.weather_list.add_widget(card)

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'


class LCloudApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        sm = MDScreenManager()
        self.weather_screen = WeatherScreen(name='home')
        self.forecast_screen = ForecastScreen(name='forecast')
        self.weather_screen.forecast  = self.forecast_screen
        sm.add_widget(self.weather_screen)
        sm.add_widget(self.forecast_screen)
        return sm

LCloudApp().run()