# utils/config_parser.py

import yaml
import os

class Config:
    def __init__(self, config_file='configs/default_config.yaml'):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, key_path, default=None):
        keys = key_path.split('.')
        val = self.config
        for key in keys:
            if isinstance(val, dict):
                val = val.get(key, {})
            else:
                return default
        return val or default
