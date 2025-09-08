# DetailScreen.py (updated to fetch from correct TEST JSON and prevent duplicates)
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.app import App
import requests
import json
import boto3  # For AWS S3 interactions (install via pip install boto3)
import sys
import os  # For path joining
from dotenv import load_dotenv  # For loading .env file (install via pip install python-dotenv)

# Load environment variables from .env file in the root directory
load_dotenv()


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        # Main layout (will be populated dynamically)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
    
    def update_details(self, show_id, item_data):
        # Clear previous content
        self.layout.clear_widgets()
        
        # Add header with ID
        header = Label(text=f"Details for Show ID: {show_id}", font_size=24, size_hint_y=None, height=dp(50))
        self.layout.add_widget(header)
        
        # ScrollView for the grid
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        
        # Grid for key-value pairs (2 columns)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))  # Bind for dynamic height
        
        # Dynamically resolve font path (for bundled vs. development)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            font_path = os.path.join(sys._MEIPASS, 'NotoSansDevanagari.ttf')
        else:
            font_path = 'NotoSansDevanagari.ttf'  # Local development path
        
        for key, value in item_data.items():
            key_label = Label(text=key, size_hint_y=None, height=dp(40), halign='left', valign='middle')
            key_label.bind(size=key_label.setter('text_size'))
            grid.add_widget(key_label)
            
            value_label = Label(
                text=str(value), 
                size_hint_y=None, 
                height=dp(40), 
                halign='left', 
                valign='middle',
                font_name=font_path  # Dynamic path
            )
            value_label.bind(size=value_label.setter('text_size'))
            grid.add_widget(value_label)
        
        scroll_view.add_widget(grid)
        self.layout.add_widget(scroll_view)
        
        # Buttons layout
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=10)
        
        approve_button = Button(text="Approve", size_hint=(None, None), size=(150, 50))
        approve_button.bind(on_press=lambda instance: self.show_confirm_popup(show_id, 'approve'))
        buttons_layout.add_widget(approve_button)
        
        reject_button = Button(text="Reject", size_hint=(None, None), size=(150, 50))
        reject_button.bind(on_press=self.on_reject)
        buttons_layout.add_widget(reject_button)
        
        back_button = Button(text="Back", size_hint=(None, None), size=(150, 50))
        back_button.bind(on_press=self.switch_back)
        buttons_layout.add_widget(back_button)
        
        self.layout.add_widget(buttons_layout)
    
    def show_confirm_popup(self, show_id, action):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Are you sure?"))
        
        buttons = BoxLayout(orientation='horizontal', spacing=10)
        yes_button = Button(text="Yes")
        yes_button.bind(on_press=lambda instance: self.handle_action(show_id, action, popup))
        buttons.add_widget(yes_button)
        
        no_button = Button(text="No")
        no_button.bind(on_press=lambda instance: popup.dismiss())
        buttons.add_widget(no_button)
        
        content.add_widget(buttons)
        
        popup = Popup(title="Confirm", content=content, size_hint=(0.8, 0.4))
        popup.open()
    
    def handle_action(self, show_id, action, popup):
        popup.dismiss()
        if action == 'approve':
            self.approve_show(show_id)
    
    def approve_show(self, show_id):
        # Fetch current ShowIds_TEST.json (match SecondScreen)
        url = "https://s3.ap-south-1.amazonaws.com/co.techxr.system.backend.upload.dev/DurlabhDarshan/Jsons/ShowIds_TEST.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
        except Exception as e:
            self.show_result_popup("Failure", "Error fetching JSON.")
            print(f"Error fetching JSON: {e}")
            return
        
        # Update JSON: Move ID from commingSoonVideoShowIds to approvedVideoShowIds
        coming_soon = json_data.get('commingSoonVideoShowIds', [])
        approved = json_data.get('approvedVideoShowIds', [])
        
        # Ensure no duplicates and safe remove
        if show_id in coming_soon:
            coming_soon.remove(show_id)
        if show_id not in approved:
            approved.append(show_id)
        
        # Optional: Sort lists to maintain order (if IDs are numeric strings)
        coming_soon.sort(key=lambda x: int(x))
        approved.sort(key=lambda x: int(x))
        
        json_data['commingSoonVideoShowIds'] = coming_soon
        json_data['approvedVideoShowIds'] = approved
        
        # Upload updated JSON to S3
        try:
            # Load credentials from .env
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            bucket_name = os.environ.get('BUCKET_NAME', 'co.techxr.system.backend.upload.dev')  # Fallback if not in .env
            object_key = os.environ.get('OBJECT_KEY', 'DurlabhDarshan/Jsons/ShowIds_TEST.json')  # Fallback if not in .env
            
            s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=json.dumps(json_data), ContentType='application/json')
            self.show_result_popup("Success", f"Show ID {show_id} approved and uploaded.")
            
            # Refresh the list in SecondScreen
            second_screen = self.manager.get_screen('second')
            second_screen.refresh_list()
        except Exception as e:
            self.show_result_popup("Failure", "Error uploading to S3.")
            print(f"Error uploading to S3: {e}")
            return
        
        # Navigate back after approval
        self.switch_back(None)
    
    def show_result_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        ok_button = Button(text="OK", size_hint=(None, None), size=(100, 50))
        ok_button.bind(on_press=lambda instance: popup.dismiss())
        content.add_widget(ok_button)
        
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.3))
        popup.open()
    
    def on_reject(self, instance):
        print("Rejected!")  # Placeholder: Add actual reject logic here
        self.switch_back(instance)
    
    def switch_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'second'
