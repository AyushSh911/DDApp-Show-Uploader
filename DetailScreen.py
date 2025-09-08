# DetailScreen.py (new file)
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.message_label = Label(text="", font_size=24)
        layout.add_widget(self.message_label)
        
        back_button = Button(text="Back", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.switch_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def update_message(self, message):
        self.message_label.text = message
    
    def switch_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'second'
