"""
A simple application which is going to print Hello World
"""
import toga
import json
import httpx
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from newsapi import NewsApiClient


class HelloWorld(toga.App):

    def startup(self):

        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label('Write your name here :', style=Pack(padding=(0, 5)))
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button("Say Hello !", on_press=self.say_hello, style=Pack(padding=5))
        buttonMeteo = toga.Button("Afficher la météo", on_press=self.printMeteo, style=Pack(flex=1))
        buttonNews = toga.Button("Afficher des news", on_press=self.printNews, style=Pack(flex=1))
        # icon = toga.ImageView(
        #    "http://openweathermap.org/img/w/10d.png", style=Pack(padding=(0, 5)))

        main_box.add(name_box)
        main_box.add(button)
        main_box.add(buttonMeteo)
        main_box.add(buttonNews)
        # main_box.add(icon)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def printNews(self, widget):
        newsapi = NewsApiClient(api_key='3a98e19d8fe7460d8e4d2f2e15e64c2e')
        sources = newsapi.get_sources()
        self.main_window.info_dialog(
            "News", "Voici quelques news : {}".format(sources))

    def say_hello(self, widget):
        if self.name_input.value == "":
            self.main_window.info_dialog("Error", "You haven't choose a name, please enter one !")
        else:
            with httpx.Client() as client:
                response = client.get("https://jsonplaceholder.typicode.com/posts/42")
            payload = response.json()
            self.main_window.info_dialog('Hello, {}'.format(
                self.name_input.value), "Salut ! Voici quelques news : {}".format(payload["body"]))

    def printMeteo(self, widget):
        with httpx.Client() as client:
            # api = open("C:\Users\volko\Documents\GitHub\PythonAvatarTest\beeware-tutorial\helloworld\src\helloworld\api.mysecretkey")
            response = client.get(
                "http://api.openweathermap.org/data/2.5/weather?q=Compiegne&lang=fr&appid={}".format(
                    "84f57628dd0ba9ae420897f95a2ce69f"))
        #payload = response.json()
        new_box = toga.Box()
        icon = toga.ImageView(
            id="icon", image="http://openweathermap.org/img/w/{}.png".format(response.json()["weather"][0]["icon"]))
        new_box.add(icon)
        self.main_window.content = new_box
        self.main_window.info_dialog(
            "Meteo", "Voici la météo d'aujourd'hui au Havre : {}".format(response.json()["weather"][0]["description"]))


def main():
    return HelloWorld()
