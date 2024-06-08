import os
import json

from toga import App

class SystemOp():
    def __init__(self, app:App):
        super().__init__()
        self.app = app
        self.data_path = self.app.paths.data
        self.config_path = self.app.paths.config
        
    
    def update_settings(self, setting_key, setting_value):
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
        settings_path = os.path.join(self.config_path, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
            settings = {}
        settings[setting_key] = setting_value
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
            
            
    def check_window_is_open(self):
        settings_path = os.path.join(self.config_path, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            
            if any(settings.get(key, False) for key in [
                'cash_window',
                'wallet_window',
                'browser_window'
                ]
                   ):
                return True
        
        return False
        
    
    def load_config_file(self):
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        file_path = os.path.join(config_path, config_file)
        if not os.path.exists(file_path):
            return None
        if os.path.exists(file_path):
            return file_path
        
        
        
    def load_node_files(self):
        required_files = [
            'bitcoinzd.exe',
            'bitcoinz-cli.exe',
            'bitcoinz-tx.exe'
        ]
        missing_files = [
            file_name for file_name in required_files
            if not os.path.exists(os.path.join(self.data_path, file_name))
        ]
        if missing_files:
            return missing_files
        else:
            return None
        
        
    def load_params_files(self):
        directory_path = os.path.join(os.getenv('APPDATA'), "ZcashParams")
        required_files = [
            'sprout-proving.key',
            'sprout-verifying.key',
            'sapling-spend.params',
            'sapling-output.params',
            'sprout-groth16.params'
        ]
        missing_files = [
            file_name for file_name in required_files
            if not os.path.exists(os.path.join(directory_path, file_name))
        ]

        if missing_files:
            return missing_files
        else:
            return None
        
        
    def clean_config_path(self):
        if not os.path.exists(self.config_path):
            return
        db_path = os.path.join(self.config_path, 'config.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            
            
    def windows_screen_center(self, size):
        
        screen_size = self.app.screens[0].size
        screen_width, screen_height = screen_size
        window_width, window_height = size
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        return (x, y)
    
    def windows_full_screen(self):
        
        screen_size = self.app.screens[0].size
        window_width, window_height = screen_size
        x = window_width - 50
        y = window_height - 100
        
        return (x, y)