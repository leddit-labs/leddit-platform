resource "keycloak_realm" "leddit" {
  realm   = var.realm_name
  enabled = true

  display_name = "Leddit"

  registration_allowed           = true
  registration_email_as_username = false
  verify_email                   = false
  login_with_email_allowed       = true
  reset_password_allowed         = true
  edit_username_allowed          = false

  attributes = {
    frontend_url = "http://localhost:9080"
  }
}

# ============================================
# Frontend Client
# ============================================
resource "keycloak_openid_client" "leddit_frontend" {
  realm_id  = keycloak_realm.leddit.id
  client_id = "leddit-frontend"
  name      = "Leddit Frontend"

  access_type                  = "PUBLIC"
  standard_flow_enabled        = true
  direct_access_grants_enabled = true

  valid_redirect_uris = [
    "http://localhost:3000/*",
    "http://localhost:5173/*",
  ]

  web_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
  ]
}

# ============================================
# Profile Mapper
# ============================================
data "keycloak_openid_client_scope" "profile" {
  realm_id = keycloak_realm.leddit.id
  name     = "profile"
}

# Use a user property mapper instead of user attribute mapper
resource "keycloak_openid_user_property_protocol_mapper" "sub_mapper" {
  realm_id            = keycloak_realm.leddit.id
  client_scope_id     = data.keycloak_openid_client_scope.profile.id
  name                = "sub"
  user_property       = "id"
  claim_name          = "sub"
  add_to_access_token = true
  add_to_id_token     = true
}

# ============================================
# Audience Mapper - allows leddit-api to introspect tokens
# ============================================
resource "keycloak_openid_audience_protocol_mapper" "leddit_api_audience" {
  realm_id  = keycloak_realm.leddit.id
  client_id = keycloak_openid_client.leddit_frontend.id
  name      = "leddit-api-audience"

  included_client_audience = "leddit-api"
  add_to_access_token      = true
}

# ============================================
# Default Client Scopes
# ============================================
resource "keycloak_openid_client_default_scopes" "frontend_scopes" {
  realm_id  = keycloak_realm.leddit.id
  client_id = keycloak_openid_client.leddit_frontend.id

  default_scopes = [
    "profile",
    "email",
    "roles",
    "web-origins",
  ]
}

# ============================================
# API Client (used by APISIX for introspection)
# ============================================
resource "keycloak_openid_client" "leddit_api" {
  realm_id  = keycloak_realm.leddit.id
  client_id = "leddit-api"
  name      = "Leddit API"

  access_type                  = "CONFIDENTIAL"
  service_accounts_enabled     = true
  standard_flow_enabled        = false
  direct_access_grants_enabled = true

  client_secret = "leddit-api-dev-secret-123"
}

# ============================================
# Realm Management Permissions (for introspection)
# ============================================
data "keycloak_openid_client" "realm_management" {
  realm_id  = keycloak_realm.leddit.id
  client_id = "realm-management"
}

data "keycloak_role" "view_users" {
  realm_id  = keycloak_realm.leddit.id
  client_id = data.keycloak_openid_client.realm_management.id
  name      = "view-users"
}

data "keycloak_role" "query_users" {
  realm_id  = keycloak_realm.leddit.id
  client_id = data.keycloak_openid_client.realm_management.id
  name      = "query-users"
}

resource "keycloak_openid_client_service_account_role" "leddit_api_view_users" {
  realm_id                = keycloak_realm.leddit.id
  service_account_user_id = keycloak_openid_client.leddit_api.service_account_user_id
  client_id               = data.keycloak_openid_client.realm_management.id
  role                    = "view-users"
}

resource "keycloak_openid_client_service_account_role" "leddit_api_query_users" {
  realm_id                = keycloak_realm.leddit.id
  service_account_user_id = keycloak_openid_client.leddit_api.service_account_user_id
  client_id               = data.keycloak_openid_client.realm_management.id
  role                    = "query-users"
}

resource "keycloak_user" "test_user" {
  realm_id       = keycloak_realm.leddit.id
  username       = "testuser"
  email          = "test@leddit.local"
  first_name     = "Test"
  last_name      = "User"
  enabled        = true
  email_verified = true

  initial_password {
    value     = "leddit123"
    temporary = false
  }
}

resource "keycloak_user" "nevermod" {
  realm_id       = keycloak_realm.leddit.id
  username       = "nevermod"
  email          = "nevermod@leddit.local"
  first_name     = "Never"
  last_name      = "Mod"
  enabled        = true
  email_verified = true

  initial_password {
    value     = "nevermod"
    temporary = false
  }
}

resource "keycloak_user" "maybemod" {
  realm_id       = keycloak_realm.leddit.id
  username       = "maybemod"
  email          = "maybemod@leddit.local"
  first_name     = "Maybe"
  last_name      = "Mod"
  enabled        = true
  email_verified = true

  initial_password {
    value     = "maybemod"
    temporary = false
  }
}

# ============================================
# Realm Roles
# ============================================
resource "keycloak_role" "user_role" {
  realm_id    = keycloak_realm.leddit.id
  name        = "user"
  description = "Standard Leddit user role"
}

# ============================================
# GitHub Identity Provider
# ============================================
resource "keycloak_oidc_identity_provider" "github" {
  realm                         = keycloak_realm.leddit.id
  alias                         = "github"
  display_name                  = "GitHub"
  provider_id                   = "github"
  enabled                       = true
  store_token                   = false
  trust_email                   = true
  first_broker_login_flow_alias = "first broker login"
  sync_mode                     = "IMPORT"

  client_id     = var.github_client_id
  client_secret = var.github_client_secret
  default_scopes = "user:email"

  authorization_url = "https://github.com/login/oauth/authorize"
  token_url         = "https://github.com/login/oauth/access_token"
  user_info_url     = "https://api.github.com/user"
}

# ============================================
# GitHub Role Mapper
# ============================================
resource "keycloak_hardcoded_role_identity_provider_mapper" "github_user_role" {
  realm                   = keycloak_realm.leddit.id
  name                    = "github-user-role-mapper"
  identity_provider_alias = keycloak_oidc_identity_provider.github.alias
  role                    = keycloak_role.user_role.name
}