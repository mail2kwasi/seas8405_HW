# PowerShell script: setup-keycloak-user.ps1

$KC_BASE_URL = "http://localhost:8080"
$KC_REALM = "custom-realm"
$ADMIN_USER = "admin"
$ADMIN_PASS = "admin"
$CLIENT_ID = "admin-cli"
$TARGET_USER = "frank"
$NEW_PASSWORD = "nero2244"

# 1. Get admin token
$response = Invoke-RestMethod -Method Post -Uri "$KC_BASE_URL/realms/master/protocol/openid-connect/token" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body @{
    username = $ADMIN_USER
    password = $ADMIN_PASS
    grant_type = "password"
    client_id = $CLIENT_ID
  }
$ACCESS_TOKEN = $response.access_token

# 2. Get user ID
$userList = Invoke-RestMethod -Method Get -Uri "$KC_BASE_URL/admin/realms/$KC_REALM/users?username=$TARGET_USER" `
  -Headers @{ Authorization = "Bearer $ACCESS_TOKEN" }

$USER_ID = $userList[0].id

# 3. Update user
Invoke-RestMethod -Method Put -Uri "$KC_BASE_URL/admin/realms/$KC_REALM/users/$USER_ID" `
  -Headers @{ Authorization = "Bearer $ACCESS_TOKEN" } `
  -ContentType "application/json" `
  -Body (@{
    enabled = $true
    emailVerified = $true
    requiredActions = @()
    username = $TARGET_USER
  } | ConvertTo-Json -Depth 3)

# 4. Reset password
Invoke-RestMethod -Method Put -Uri "$KC_BASE_URL/admin/realms/$KC_REALM/users/$USER_ID/reset-password" `
  -Headers @{ Authorization = "Bearer $ACCESS_TOKEN" } `
  -ContentType "application/json" `
  -Body (@{
    type = "password"
    value = $NEW_PASSWORD
    temporary = $false
  } | ConvertTo-Json -Depth 3)

Write-Host "✅ User '$TARGET_USER' updated and password reset."
