# main.py (updated)
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

# Import screens from their respective files
from ShowsList import SecondScreen
from DetailScreen import DetailScreen  # New import

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
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(DetailScreen(name='detail'))  # Add the detail screen
        return sm

if __name__ == '__main__':
    MyFirstKivyApp().run()
