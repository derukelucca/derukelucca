import boto3
from kubernetes import client, config

def list_eks_namespaces(cluster_name, region_name):
    # Configurar o acesso ao cluster EKS
    eks_client = boto3.client('eks', region_name=region_name)
    response = eks_client.describe_cluster(name=cluster_name)
    cluster_endpoint = response['cluster']['endpoint']
    cluster_certificate = response['cluster']['certificateAuthority']['data']

    config.load_kube_config()
    config.load_incluster_config()

    # Usar as informações do cluster EKS
    kube_config = config.new_client_from_config()
    kube_config.server = cluster_endpoint
    kube_config.certificate_authority = cluster_certificate

    client.Configuration.set_default(kube_config)

    # Listar os namespaces
    api = client.CoreV1Api()
    namespaces = api.list_namespace()

    return [ns.metadata.name for ns in namespaces.items]

if __name__ == "__main__":
    cluster_name = "seu-cluster-eks"  # Substitua pelo nome do seu cluster EKS
    aws_region = "us-west-2"  # Substitua pela região do seu cluster EKS

    namespaces = list_eks_namespaces(cluster_name, aws_region)
    for namespace in namespaces:
        print(namespace)
