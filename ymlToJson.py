import os
import yaml
import json
import requests

def read_alert_files(folder_path):
    alert_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".yml") or file_name.endswith(".yaml"):
            file_path = os.path.join(folder_path, file_name)
            alert_files.append(file_path)
    return alert_files

def convert_yaml_to_json(yaml_path):
    with open(yaml_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    json_data = json.dumps(yaml_data)
    return json_data

def send_alert_to_api(json_data):
    api_url = "http://example.com/api"  # Substitua pelo URL da sua API
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, data=json_data, headers=headers)
    return response

def process_alert_files(folder_path):
    alert_files = read_alert_files(folder_path)
    for file_path in alert_files:
        json_data = convert_yaml_to_json(file_path)
        response = send_alert_to_api(json_data)
        print(f"File: {file_path}")
        print(f"Response: {response.text}\n")

# Pasta onde estão os arquivos de alerta YAML
folder_path = "/caminho/para/a/pasta"

process_alert_files(folder_path)
