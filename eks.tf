
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name                   = local.name
  cluster_endpoint_public_access = true
  create_kms_key              = false
  create_cloudwatch_log_group = false
  cluster_encryption_config   = {}

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.public_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets
  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    spot = {
      desired_size = 1
      min_size     = 1
      max_size     = 1

      labels = {
        role = "spot"
      }
      instance_types = ["t3.small"]
      capacity_type  = "SPOT"
    }

  }
}



resource "null_resource" "deploy-yaml" {

  depends_on = [ module.eks , module.eks , helm_release.alb-controller]

  provisioner "local-exec" {
      command = "aws eks update-kubeconfig --name eks-cluster"
  }
  provisioner "local-exec" {
      command = "kubectl apply -f flask.yaml"
  }
   lifecycle {
        replace_triggered_by = [null_resource.replace_trigger]
   }
}

resource "null_resource" "update-flask-image" {
  depends_on = [null_resource.deploy-yaml]

  provisioner "local-exec" {
      command = "kubectl rollout restart deployment flask"
  }
   lifecycle {
        replace_triggered_by = [null_resource.replace_trigger]
   }
}


resource "null_resource" "replace_trigger" {
  triggers = {
    replace = false
  }
}

