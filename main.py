import argparse
import os
import json

class App:
    def __init__(self, config_path):
        self.loadSettings(config_path=config_path)

    def loadSettings(self, config_path):
        # First check if the config file exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")

        # Load the config file as json file
        with open(config_path, 'r') as file:
            self.config = json.load(file)

        # Check if the config file was loaded correctly
        if not isinstance(self.config, dict):
            raise ValueError("Invalid config file format.")

    def start(self):
        # Aquí es donde colocarías la lógica para iniciar tu aplicación
        pass

def main():
    #Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.json'))
    args = parser.parse_args()

    app = App(args.config)
    app.start()

if __name__ == "__main__":
    main()