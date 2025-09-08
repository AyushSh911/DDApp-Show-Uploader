# ShowsList.py (updated - remove thumbnails fetch, use app.json_thumbnails in ItemButton)
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
        # Get the full data for this item_id from app's json_thumbnails
        item_data = app.json_thumbnails.get(self.item_id, {})
        detail_screen.update_details(self.item_id, item_data)
        sm.transition = SlideTransition(direction='left')
        sm.current = 'detail'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        
        # Fetch ShowIds JSON
        url_show_ids = "https://s3.ap-south-1.amazonaws.com/co.techxr.system.backend.upload.dev/DurlabhDarshan/Jsons/ShowIds_TEST.json"
        try:
            response_show_ids = requests.get(url_show_ids)
            response_show_ids.raise_for_status()
            json_show_ids = response_show_ids.json()
            coming_soon_ids = json_show_ids.get('commingSoonVideoShowIds', [])
        except Exception as e:
            print(f"Error fetching ShowIds JSON: {e}")
            coming_soon_ids = []
        
        # Prepare data: Use videoTitle if available, else fallback to ID
        # Fetch thumbnails from app (assumed fetched in build)
        app = App.get_running_app()
        json_thumbnails = app.json_thumbnails
        
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
