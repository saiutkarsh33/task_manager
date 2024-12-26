resource "aws_eks_cluster" "eks_cluster" {
  name     = "task-manager-eks"
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = [aws_subnet.private_subnet.id]
  }
}
