import boto3
import yaml

def lambda_handler(event, context):
    # Nome do cluster EKS e do ConfigMap que será alterado
    cluster_name = 'nome-do-cluster-eks'
    configmap_name = 'nome-do-configmap'

    # Configurar cliente do EKS
    eks_client = boto3.client('eks')

    # Obter informações sobre o cluster EKS
    cluster_info = eks_client.describe_cluster(name=cluster_name)
    cluster_endpoint = cluster_info['cluster']['endpoint']
    cluster_certificate = cluster_info['cluster']['certificateAuthority']['data']

    # Configurar cliente do Kubernetes usando a biblioteca `kubectl`
    kubectl = boto3.client('ssm').get_parameter(Name='/eksctl/kubeconfig/' + cluster_name + '/kubeconfig')

    # Atualizar o ConfigMap
    configmap_data = {
        'data': {
            'chave': 'valor_atualizado'
        }
    }

    # Serializar o objeto YAML para uma string
    updated_configmap_yaml = yaml.dump(configmap_data)

    # Executar o comando kubectl apply para atualizar o ConfigMap
    command = f'kubectl apply --kubeconfig {kubectl} -n namespace-do-configmap -f -'
    response = subprocess.run(command, input=updated_configmap_yaml, shell=True, capture_output=True, text=True)

    if response.returncode == 0:
        print('ConfigMap atualizado com sucesso!')
    else:
        print('Erro ao atualizar o ConfigMap:', response.stderr)
