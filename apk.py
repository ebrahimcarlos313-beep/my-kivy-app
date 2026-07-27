from kivy.app import App
from kivy.uix.label import Label

class MySimpleApp(App):
    def build(self):
        return Label(text="Hello, this is my first mobile app!" ,font_size='20sp')
if __name__ == '__main__':
    MySimpleApp().run()
