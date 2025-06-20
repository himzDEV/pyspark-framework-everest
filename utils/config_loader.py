
import yaml
import json
import os

class ConfigLoader:
    """
    Utility to load pipeline configuration from YAML or JSON.
    """

    @staticmethod
    def load(config_path: str) -> dict:
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        if config_path.endswith(".yaml") or config_path.endswith(".yml"):
            with open(config_path, "r") as f:
                return yaml.safe_load(f)

        elif config_path.endswith(".json"):
            with open(config_path, "r") as f:
                return json.load(f)

        else:
            raise ValueError("Config file must be YAML (.yaml/.yml) or JSON (.json)")
