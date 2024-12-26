resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "task-manager-redis-subnet-group"
  subnet_ids = [aws_subnet.private_subnet.id]
}

resource "aws_elasticache_cluster" "redis_cluster" {
  cluster_id           = "task-manager-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  subnet_group_name    = aws_elasticache_subnet_group.redis_subnet_group.name
  security_group_ids   = [aws_security_group.db_sg.id]
}
