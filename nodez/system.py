import os
import json
import qrcode

from toga import App


class SystemOp():
    def __init__(self, app:App):
        super().__init__()
        
        self.app = app

        self.data_path = self.app.paths.data
        self.config_path = self.app.paths.config
        self.logs_path = self.app.paths.logs
        self.cache_path = self.app.paths.cache


    def qr_generate(self, address):
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
            
        qr_filename = f"qr_{address}.png"
        qr_path = os.path.join(self.cache_path, qr_filename)
        if os.path.exists(qr_path):
            return qr_path
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=1,
        )
        qr.add_data(address)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        with open(qr_path, 'wb') as f:
            qr_img.save(f)
        
        return qr_path
        
    
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
                'explorer_window',
                'message_window',
                'ecosys_window',
                'mining_window',
                'browser_window',
                'peerinfo_window'
                ]
                   ):
                return True
        
        return False
    
    
    def is_window_open(self, window_name):
        settings_path = os.path.join(self.config_path, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings = json.load(f)
                return settings.get(window_name, False)
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
    
    
    
    def format_price(self, price):
        if price > 0.00000001 and price < 0.0000001:
            return f"{price:.10f}"
        elif price > 0.0000001 and price < 0.000001:
            return f"{price:.9f}"
        elif price > 0.000001 and price < 0.00001:
            return f"{price:.8f}"
        elif price > 0.00001 and price < 0.0001:
            return f"{price:.7f}"
        elif price > 0.0001 and price < 0.001:
            return f"{price:.6f}"
        elif price > 0.001 and price < 0.01:
            return f"{price:.5f}"
        elif price > 0.01 and price < 0.1:
            return f"{price:.4f}"
        elif price > 0.1 and price < 1:
            return f"{price:.3f}"
        elif price > 1 and price < 10:
            return f"{price:.2f}"
        elif price > 10 and price < 100:
            return f"{price:.1f}"
        else:
            return f"{price:.0f}"
        
        
        
    def format_balance(self, total):
        formatted_total = '{:.8f}'.format(total)  
        parts = formatted_total.split('.')  
        integer_part = parts[0]
        decimal_part = parts[1] 

        if len(integer_part) > 4:
            digits_to_remove = len(integer_part) - 4
            formatted_decimal = decimal_part[:-digits_to_remove]
        else:
            formatted_decimal = decimal_part

        formatted_balance = integer_part + '.' + formatted_decimal
        return formatted_balance