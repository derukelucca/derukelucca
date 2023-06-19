from kubernetes import client, config

def lambda_handler(event, context):
    # Nome do cluster EKS e do ConfigMap que será alterado
    cluster_name = 'nome-do-cluster-eks'
    configmap_name = 'nome-do-configmap'
    namespace = 'namespace-do-configmap'

    # Arquivo de configuração kubeconfig do cluster EKS
    kubeconfig_file = '/path/to/kubeconfig'

    # Carregar as configurações do cluster a partir do kubeconfig
    config.load_kube_config(config_file=kubeconfig_file)

    # Criar um objeto de cliente para interagir com a API do Kubernetes
    k8s_client = client.CoreV1Api()

    # Obter o objeto ConfigMap atual
    configmap = k8s_client.read_namespaced_config_map(name=configmap_name, namespace=namespace)

    # Atualizar o dado do ConfigMap
    configmap.data['chave'] = 'valor_atualizado'

    # Atualizar o ConfigMap no cluster
    k8s_client.patch_namespaced_config_map(name=configmap_name, namespace=namespace, body=configmap)

    print('ConfigMap atualizado com sucesso!')
