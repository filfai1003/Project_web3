# Backend — API examples (curl)

This document contains quick curl examples you can use to exercise the backend endpoints while the server is running locally.

Start the server locally (from repository root):

```powershell
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Base URL: `http://127.0.0.1:8000`

Notes
- Replace `<TOKEN>` and `<USER_ID>` in the examples with actual values returned by the API.
- For pretty JSON parsing in examples we use `jq` (Linux/macOS). On Windows you can install `jq` or inspect output directly.

1) Signup — create a new user

```bash
curl -s -X POST "http://127.0.0.1:8000/auth/signup" -H "Content-Type: application/json" -d '{"username":"filfai","email":"filfai@example.com","password":"secret"}'
# Example response:
# {"access_token":"ey...","token_type":"bearer","user_id":"<USER_ID>"}
```

2) Login — by username

```bash
curl -s -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"username":"filfai","password":"secret"}'
# Example response: {"access_token":"ey...","token_type":"bearer","user_id":"<USER_ID>"}
```

3) Login — by email

```bash
curl -s -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"filfai@example.com","password":"secret"}'
# Example response: {"access_token":"ey...","token_type":"bearer","user_id":"<USER_ID>"}
```

4) Authenticate — validate/refresh token

```bash
curl -s -X GET "http://127.0.0.1:8000/auth/authenticate" -H "Authorization: Bearer <TOKEN>"
# Example response: {"access_token":"ey...","token_type":"bearer","user_id":"<USER_ID>"}
```

5) Get user — retrieve user public info (requires Authorization header)

```bash
curl -s -X GET "http://127.0.0.1:8000/user/<USER_ID>" -H "Authorization: Bearer <TOKEN>"
# Example response:
# {
#   "user_id":"<USER_ID>",
#   "username":"filfai",
#   "email":"filfai@example.com",
#   "is_active": true,
#   "created_at": "2025-11-07T12:34:56.789Z"
# }
```

Small convenience: extract the access token into a shell variable (bash + jq)

```bash
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"username":"filfai","password":"secret"}' | jq -r .access_token)

echo $TOKEN

# then use it
curl -s -H "Authorization: Bearer $TOKEN" "http://127.0.0.1:8000/user/<USER_ID>" | jq
```

Windows PowerShell (example to get token without jq)

```powershell
$resp = curl -Method Post -Uri "http://127.0.0.1:8000/auth/login" -Body (@{ username = 'filfai'; password = 'secret' } | ConvertTo-Json) -ContentType 'application/json'
$json = $resp.Content | ConvertFrom-Json
$token = $json.access_token
Write-Host $token

# Use token in subsequent request
curl -Method Get -Uri "http://127.0.0.1:8000/user/$($json.user_id)" -Headers @{ Authorization = "Bearer $token" }
```

If you want, I can also add these examples to the top-level `README.md` or create Postman/HTTPie snippets.
