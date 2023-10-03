from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import DictProperty


KV = '''
#:import utils utils

BoxLayout:
    orientation: "vertical"
    ScrollableLabel:
        text: str(app.weather_data) # ValueError: Label.text accept only str
        font_size: 50
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
    Button:
        text: "write"
        on_release: utils.write_weather_data()
    Button:
        text: "read"
        on_release: utils.read_weather_data()

    Button:
        text: "stream"
        on_release: utils.stream_weather_data()
    Button:
        text: "remove stream listener"
        on_release: utils.remove_listener_of_weather_data()

<ScrollableLabel@Label+ScrollView>

'''


class TestApp(App):
    weather_data = DictProperty(rebind=True)
    
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    TestApp().run()
