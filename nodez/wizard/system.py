import os

from toga import App

class SystemOp():
    def __init__(self, app:App):
        super().__init__()
        self.app = app
        self.data_path = self.app.paths.data
        
        
    
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