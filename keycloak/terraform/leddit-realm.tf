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
}

resource "keycloak_openid_client" "leddit_frontend" {
  realm_id  = keycloak_realm.leddit.id
  client_id = "leddit-frontend"
  name      = "Leddit Frontend"

  access_type = "PUBLIC"
  standard_flow_enabled = true
  direct_access_grants_enabled = true #made this true for testing purposes

  valid_redirect_uris = [
    "http://localhost:3000/*",
    "http://localhost:5173/*",
  ]

  web_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
  ]
}

resource "keycloak_openid_client" "leddit_api" {
  realm_id  = keycloak_realm.leddit.id
  client_id = "leddit-api"
  name      = "Leddit API"

  access_type = "CONFIDENTIAL"
  service_accounts_enabled = true
  standard_flow_enabled = false
  direct_access_grants_enabled = true #i enabled this for postman testing
}

resource "keycloak_user" "test_user" {
  realm_id   = keycloak_realm.leddit.id
  username   = "testuser"
  email      = "test@leddit.local"
  enabled    = true
  email_verified = true

  initial_password {
    value     = "leddit123"
    temporary = false
  }
}