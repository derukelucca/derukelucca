import os
import yaml
import git
from kubernetes import client, config

def is_valid_yaml(yaml_content):
    try:
        # Carregar o YAML e verificar se ele não está vazio
        yaml_obj = yaml.safe_load(yaml_content)
        return yaml_obj is not None
    except yaml.YAMLError:
        return False

def append_data_to_existing_configmap(namespace, configmap_name, data_to_append):
    config.load_kube_config()
    api = client.CoreV1Api()

    try:
        existing_configmap = api.read_namespaced_config_map(configmap_name, namespace)
        existing_data = existing_configmap.data

        # Acrescenta os novos dados ao ConfigMap existente
        existing_data.update(data_to_append)
        existing_configmap.data = existing_data

        api.replace_namespaced_config_map(configmap_name, namespace, existing_configmap)
        print(f"Dados acrescentados ao ConfigMap '{configmap_name}' no namespace '{namespace}'")
    except client.rest.ApiException as e:
        print(f"Erro ao acrescentar dados ao ConfigMap: {e}")

def append_data_to_configmaps_in_subdirectories(root_directory, repo_name):
    for root, dirs, files in os.walk(root_directory):
        if not files:
            continue  # Ignora pastas vazias
        for filename in files:
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    yaml_content = file.read()
                    if is_valid_yaml(yaml_content):
                        json_data = yaml_to_json(yaml_content)
                        if json_data:
                            configmap_name = os.path.basename(root)
                            namespace = f"thanos-{configmap_name}-pro"
                            append_data_to_existing_configmap(namespace, "thanos-rule", json_data)

def clone_or_pull_git_repo(repo_url, target_directory):
    if os.path.exists(target_directory):
        repo = git.Repo(target_directory)
        repo.remotes.origin.pull()
    else:
        git.Repo.clone_from(repo_url, target_directory)

if __name__ == "__main__":
    repo_url = "https://github.com/seu-usuario/seu-repositorio.git"  # Substitua pelo URL do seu repositório Git
    target_directory = "nome-do-seu-repo"  # Substitua pelo nome do diretório alvo

    clone_or_pull_git_repo(repo_url, target_directory)

    root_directory = os.path.abspath(target_directory)

    append_data_to_configmaps_in_subdirectories(root_directory, target_directory)
