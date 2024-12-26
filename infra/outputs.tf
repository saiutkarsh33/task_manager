output "rds_endpoint" {
  value = aws_db_instance.postgres_db.endpoint
}

output "rabbitmq_endpoint" {
  value = aws_mq_broker.rabbitmq_broker.instances[0].endpoints[0]
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis_cluster.configuration_endpoint
}

output "eks_cluster_name" {
  value = aws_eks_cluster.eks_cluster.name
}
