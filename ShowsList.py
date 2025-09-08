# ShowsList.py (updated - remove DetailScreen)
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.metrics import dp
from kivy.app import App

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
    pass

class ItemButton(Button):
    def on_press(self):
        app = App.get_running_app()
        sm = app.root  # Assuming the root is the ScreenManager
        item_id = int(self.text)
        detail_screen = sm.get_screen('detail')
        detail_screen.update_message(f"You pressed button {item_id}")
        sm.transition = SlideTransition(direction='left')
        sm.current = 'detail'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=2, spacing=2)
        
        # Header label
        label = Label(
            text="Unapproved Shows", 
            font_size=24,
            size_hint_y=None,
            height=dp(50),
            padding=[0, 30, 0, 0]
        )
        layout.add_widget(label)
        
        # RecycleView for the list
        rv = RecycleView()
        rv_layout = SelectableRecycleBoxLayout(
            default_size=(dp(50), dp(56)),
            default_size_hint=(1, None),
            size_hint_y=None,
            height=dp(500),  # Adjust height as needed
            orientation='vertical'
        )
        rv.add_widget(rv_layout)
        rv.viewclass = 'ItemButton'  # Use custom button class
        rv.data = [{'text': str(x)} for x in range(1, 6)]  # Items: 1,2,3,4,5
        layout.add_widget(rv)
        
        # Back button
        back_button = Button(text="Back", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.switch_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def switch_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first'
