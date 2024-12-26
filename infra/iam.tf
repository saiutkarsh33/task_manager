# The aws_iam_role resource creates an IAM role that the EKS control plane 
# (eks.amazonaws.com) can assume. This role grants permissions that allow 
# EKS to manage various cluster components.

resource "aws_iam_role" "eks_role" {
  name = "eks-cluster-role"

  # The assume_role_policy defines which entities can assume this role.
  # In this case, we allow the EKS service principal (eks.amazonaws.com)
  # to assume this role. This is necessary for EKS to perform actions on
  # our behalf, such as creating and managing Kubernetes control plane resources.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action: "sts:AssumeRole"
      Effect: "Allow"
      Principal: {
        Service: "eks.amazonaws.com"
      }
    }]
  })
}

# The aws_iam_role_policy_attachment attaches the AmazonEKSClusterPolicy to the 
# EKS IAM role. This policy gives EKS the permissions it needs to manage
# cluster infrastructure, such as network interfaces, security groups, and 
# other AWS resources that support the Kubernetes control plane.
resource "aws_iam_role_policy_attachment" "eks_role_attachment" {
  role       = aws_iam_role.eks_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
