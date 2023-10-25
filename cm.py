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

        # Após atualizar o ConfigMap, atualize o Deployment para reiniciar o pod
        update_deployment(namespace, "thanos-ruler")

    except client.rest.ApiException as e:
        print(f"Erro ao acrescentar dados ao ConfigMap: {e}")

def update_deployment(namespace, deployment_name):
    extensions_v1 = client.ExtensionsV1Api()

    try:
        # Obtenha o recurso Deployment atual
        current_deployment = extensions_v1.read_namespaced_deployment(deployment_name, namespace)

        # Altere a versão do aplicativo (imagem, rótulo, etc.) para forçar a recriação do pod
        current_deployment.spec.template.metadata.annotations = {
            "kubectl.kubernetes.io/restartedAt": str(int(time.time() * 10**9))
        }

        # Atualize o Deployment
        extensions_v1.replace_namespaced_deployment(deployment_name, namespace, current_deployment)

        print(f"Deployment '{deployment_name}' no namespace '{namespace}' atualizado para reiniciar o pod.")
    except client.rest.ApiException as e:
        print(f"Erro ao atualizar o Deployment: {e}")

# Resto do script...

if __name__ == "__main__":
    # Resto do script...

    try:
        clone_or_pull_git_repo(repo_url, target_directory)
        root_directory = os.path.abspath(target_directory)
        append_data_to_configmaps_in_subdirectories(root_directory, target_directory)
    except Exception as e:
        logging.exception("Erro durante a execução do script:")
