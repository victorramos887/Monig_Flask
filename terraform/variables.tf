#Variables
variable "infrastructure_version" {
  default = "1"
}
variable "access_key" {
  default = ""
}

variable "terraform_key" {
    default="terraform-aws"
}

variable "versao" {
    default = "~> 4.16"
}

variable "region" {
  default = "us-east-2"
}
variable "vpc_cidr" {
  description = "The CIDR Block for the SiteSeer VPC"
  default     = "10.0.0.0/16"
}

variable "rt_wide_route" {
  description = "Route in the SiteSeer Route Table"
  default     = "0.0.0.0/0"
}
variable "subnet_count" {
  description = "no of subnets"
  default = 2
}
variable "availability_zones" {
  description = "availability zone to create subnet"
  default = [
    "us-east-2a",
    "us-east-2b"]
}
variable "postgres_db_port" {
  description = "Port exposed by the RDS instance"
  default = 5432
}
variable "rds_instance_type" {
  description = "Instance type for the RDS database"
  default = "db.t2.micro"
}
# Change monig to postgres
variable "rds_identifier" {
  description = "db identifier"
  default     = "moing"
}
variable "rds_storage_type" {
  description = "db storage type"
  default     = "gp2"
}
# Change 20 to 5
variable "rds_allocated_storage" {
  description = "db allocated storage"
  default     = 20
}
variable "rds_engine" {
  description = "type of db engine"
  default     = "postgres"
}
variable "rds_engine_version" {
  description = "db engine version"
  default     = "12"
}
variable "rds_database_name" {
  description = "db nome"
  default     = "monig"
}
variable "rds_username" {
  description = "db username"
  default     = "postgres"
}
variable "rds_password" {
  description = "db password"
  default     = "adminmonig"
}
variable "rds_final_snapshot_identifier" {
  description = "db final snapshot identifier"
  default     = "worker-final"
}
variable "flask_app_port" {
  description = "Port exposed by the flask application"
  default = 5000
}

variable "flask_app_image" {
  description = "Dockerhub image for flask-app"
  default = "docker.io/viictorramos/monig:test"
}
variable "flask_app" {
  description = "FLASK APP variable"
  default = "app"
}
variable "flask_env" {
  description = "FLASK ENV variable"
  default = "dev"
}
variable "flask_app_home" {
  description = "APP HOME variable"
  default = "/usr/src/app/"
}
variable "sqlalchemy_database_uri" {
  description = "uri do banco"
  default = "postgresql://postgres:postgres@localhost:5432/monig"
}

variable "sqlalchemy_database_uri_asnc" {
  description = "uri assincrona"
  default     = "postgresql+asyncpg://postgres:postgres@localhost:5432/monig"
}

variable "secret_key" {
  description = "chave"
  default     = "dev"
}

variable "jwt_secret_key" {
  description = "JWT"
  default = "JWT_SECRET_KEY"
}

variable "time_zone" {
  description =  "Zona temporal"
  default     =  "America/Sao_Paulo"
}

variable "db_test" {
  description = "Banco de dados pytest"
  default     = "sqlite:///test.db"
}

variable "session_type" {
  description = "..."
  default = "redis"
}

variable "port" {
  description = "Porta de acesso"
  default     = 5000
}

variable "app_port" {
  description = "Porta acesso init"
  default     =  5000
}

variable "flask_debug" {
  description = "Debug run"
  default     = 1
}