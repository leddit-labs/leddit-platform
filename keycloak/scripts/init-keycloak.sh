set -e

echo "Starting Keycloak"

docker compose up -d

echo "Waiting for Keycloak"
until curl -s http://localhost:9000/health/ready > /dev/null 2>&1; do
    sleep 2
done

echo "Keycloak is ready"

echo "Applying Terraform configuration"
cd terraform
terraform init
terraform apply -auto-approve

echo ""
echo "Done!"
echo "Keycloak: http://localhost:8080"
echo "Realm: leddit"
echo "Test user: testuser / leddit123"