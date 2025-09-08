# main.py (updated to fetch JSON once and store in app)
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import requests

# Import screens from their respective files
from ShowsList import SecondScreen
from DetailScreen import DetailScreen  # Assuming DetailScreen.py exists

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        
        # Create a vertical layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add the label
        label = Label(text="Show Approver", font_size=24)
        layout.add_widget(label)
        
        # Add the button
        button = Button(text="Start", size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_second_screen)
        layout.add_widget(button)
        
        self.add_widget(layout)
    
    def switch_to_second_screen(self, instance):
        # Switch to the second screen with a slide transition
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'second'

class MyFirstKivyApp(App):
    def build(self):
        # Fetch VideoThumbnails JSON once here
        url_thumbnails = "https://s3.ap-south-1.amazonaws.com/co.techxr.system.backend.upload.dev/DurlabhDarshan/Jsons/VideoThumbnails.json"
        try:
            response_thumbnails = requests.get(url_thumbnails)
            response_thumbnails.raise_for_status()
            self.json_thumbnails = response_thumbnails.json()
        except Exception as e:
            print(f"Error fetching VideoThumbnails JSON: {e}")
            self.json_thumbnails = {}
        
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(DetailScreen(name='detail'))  # Add the detail screen
        return sm

if __name__ == '__main__':
    MyFirstKivyApp().run()
