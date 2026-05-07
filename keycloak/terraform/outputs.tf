output "realm_config" {
  value = {
    realm      = keycloak_realm.leddit.realm
    issuer_uri = "${var.keycloak_url}/realms/${keycloak_realm.leddit.realm}"
    certs_url  = "${var.keycloak_url}/realms/${keycloak_realm.leddit.realm}/protocol/openid-connect/certs"
  }
}

output "clients" {
  value = {
    frontend = {
      client_id = keycloak_openid_client.leddit_frontend.client_id
      type      = "public"
    }
    api = {
      client_id     = keycloak_openid_client.leddit_api.client_id
      client_secret = sensitive(keycloak_openid_client.leddit_api.client_secret)
      type          = "confidential"
    }
  }
  sensitive = true
}

output "test_user" {
  value = {
    username = keycloak_user.test_user.username
    password = "leddit123"
  }
}