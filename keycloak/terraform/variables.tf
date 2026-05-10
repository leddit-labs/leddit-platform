variable "keycloak_url" {
  description = "Keycloak server URL"
  type        = string
  default     = "http://localhost:8080"
}

variable "keycloak_admin_user" {
  description = "Keycloak admin username"
  type        = string
  default     = "admin"
}

variable "keycloak_admin_password" {
  description = "Keycloak admin password"
  type        = string
  default     = "admin"
}

variable "realm_name" {
  description = "Realm name"
  type        = string
  default     = "leddit"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

variable "leddit_frontend_url" {
  description = "Frontend URL"
  type        = string
  default     = "http://localhost:3000"
}