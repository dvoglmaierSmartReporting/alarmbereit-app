# -*- coding: utf-8 -*-

import yaml
import json

def yaml_to_json():
    with open("feuerwehr_tools_storage.yaml", "r") as f:
        try:
            # Parse the YAML content
            parsed_yaml = yaml.safe_load(f)
            
            # Convert the parsed YAML to JSON
            json_output = json.dumps(parsed_yaml, ensure_ascii=False, indent=4)
            
            return json_output
        
        except yaml.YAMLError as e:
            print(e)
    

# Example usage
if __name__ == "__main__":
    

    print(yaml_to_json())
