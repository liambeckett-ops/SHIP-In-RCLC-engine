from pathlib import Path
import yaml

class SolvineAgent:
    def __init__(self, config_dir=None):
        self.config_dir = config_dir or Path(__file__).parent / "config"
        self.config = self.load_config()

    def load_config(self):
        config_path = self.config_dir / "solvine_core.yaml"
        if config_path.exists():
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def initialize(self):
        print(f"Initializing Solvine agent with role: {self.config.get('agent', {}).get('role', 'Unknown')}")

    def meta_coordination(self):
        print("Performing meta-coordination and symbolic synthesis.")
