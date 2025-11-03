from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen

KV = """
Screen:
    MDLabel:
        text: "Hello, KivyMD!"
        halign: "center"
        font_style: "H4"
"""

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    TestApp().run()

