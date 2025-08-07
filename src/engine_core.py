import os
from config.config_loader import ConfigLoader

config_loader = ConfigLoader()
config = config_loader.config

def get_engine_setting(key, default=None):
    return config.get(key, default)

# Example usage
if __name__ == "__main__":
    print("Engine core loaded with settings:", config)
