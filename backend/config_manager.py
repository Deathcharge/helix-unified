# backend/config_manager.py
# Configuration loader for helix_config.toml

import toml
import os
from pathlib import Path
from typing import Any, Dict

# Determine the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "helix_config.toml"

class ConfigManager:
    """
    Manages loading and accessing configuration from helix_config.toml.
    """
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Loads the TOML configuration file."""
        if not CONFIG_PATH.exists():
            print(f"CRITICAL ERROR: Configuration file not found at {CONFIG_PATH}")
            # Fallback to a minimal default config to prevent total crash
            self._config = {
                "general": {"VERSION": "v16.7-fallback", "STATE_DIR": "Helix/state"},
                "discord": {"COMMAND_PREFIX": "!"}
            }
            return

        try:
            with open(CONFIG_PATH, 'r') as f:
                self._config = toml.load(f)
            print(f"INFO: Configuration loaded successfully from {CONFIG_PATH}")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load configuration file: {e}")
            self._config = {}

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value.
        Prioritizes environment variables (SECTION_KEY) over TOML file.
        """
        env_key = f"{section.upper()}_{key.upper()}"
        
        # 1. Check Environment Variable
        env_value = os.getenv(env_key)
        if env_value is not None:
            # Attempt to cast to appropriate type if possible
            if isinstance(default, bool):
                return env_value.lower() in ('true', '1', 't', 'y', 'yes')
            elif isinstance(default, int):
                try:
                    return int(env_value)
                except ValueError:
                    pass
            elif isinstance(default, float):
                try:
                    return float(env_value)
                except ValueError:
                    pass
            return env_value

        # 2. Check TOML Configuration
        if section in self._config and key in self._config[section]:
            return self._config[section][key]

        # 3. Return Default Value
        return default

# Global instance for easy access
config = ConfigManager()

if __name__ == '__main__':
    # Example usage for testing
    print(f"System Version: {config.get('general', 'VERSION')}")
    print(f"Command Prefix: {config.get('discord', 'COMMAND_PREFIX')}")
    print(f"Initial Harmony: {config.get('ucf', 'INITIAL_HARMONY')}")
    print(f"Non-existent Key: {config.get('nonexistent', 'key', default='default_value')}")
    
    # Test environment variable override
    os.environ['UCF_INITIAL_HARMONY'] = '0.99'
    print(f"Initial Harmony (Override): {config.get('ucf', 'INITIAL_HARMONY')}")
    del os.environ['UCF_INITIAL_HARMONY']

