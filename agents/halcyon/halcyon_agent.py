from pathlib import Path
import yaml

class HalcyonAgent:
    def __init__(self, config_dir=None):
        self.config_dir = config_dir or Path(__file__).parent / "config"
        self.config = self.load_config()

    def load_config(self):
        config_path = self.config_dir / "halcyon_core.yaml"
        if config_path.exists():
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def initialize(self):
        print(f"Initializing Halcyon agent with role: {self.config.get('agent', {}).get('role', 'Unknown')}")

    def safety_forecasting(self):
        print("Performing safety forecasting and civic override.")
