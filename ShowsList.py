# ShowsList.py (updated)
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
from kivy.properties import StringProperty
import requests

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
    pass

class ItemButton(Button):
    item_id = StringProperty('')  # Property to hold the show ID
    
    def on_press(self):
        app = App.get_running_app()
        sm = app.root  # Assuming the root is the ScreenManager
        detail_screen = sm.get_screen('detail')
        detail_screen.update_message(f"You pressed button {self.item_id}")
        sm.transition = SlideTransition(direction='left')
        sm.current = 'detail'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        
        # Fetch ShowIds JSON
        url_show_ids = "https://s3.ap-south-1.amazonaws.com/co.techxr.system.backend.upload.dev/DurlabhDarshan/Jsons/ShowIds.json"
        try:
            response_show_ids = requests.get(url_show_ids)
            response_show_ids.raise_for_status()
            json_show_ids = response_show_ids.json()
            coming_soon_ids = json_show_ids.get('commingSoonVideoShowIds', [])
        except Exception as e:
            print(f"Error fetching ShowIds JSON: {e}")
            coming_soon_ids = []
        
        # Fetch VideoThumbnails JSON
        url_thumbnails = "https://s3.ap-south-1.amazonaws.com/co.techxr.system.backend.upload.dev/DurlabhDarshan/Jsons/VideoThumbnails.json"
        try:
            response_thumbnails = requests.get(url_thumbnails)
            response_thumbnails.raise_for_status()
            json_thumbnails = response_thumbnails.json()
        except Exception as e:
            print(f"Error fetching VideoThumbnails JSON: {e}")
            json_thumbnails = {}
        
        # Prepare data: Use videoTitle if available, else fallback to ID
        button_data = []
        for show_id in coming_soon_ids:
            show_id_str = str(show_id)
            video_title = json_thumbnails.get(show_id_str, {}).get('videoTitle', show_id_str)
            button_data.append({'text': video_title, 'item_id': show_id_str})
        
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
        item_height = dp(56)
        rv_layout = SelectableRecycleBoxLayout(
            default_size=(dp(50), item_height),
            default_size_hint=(1, None),
            size_hint_y=None,
            height=len(button_data) * item_height if button_data else dp(56),  # Dynamic height, min 56 for empty
            orientation='vertical'
        )
        rv.add_widget(rv_layout)
        rv.viewclass = 'ItemButton'  # Use custom button class
        rv.data = button_data  # Data with text (title) and item_id (ID)
        layout.add_widget(rv)
        
        # Back button
        back_button = Button(text="Back", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.switch_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def switch_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first'
