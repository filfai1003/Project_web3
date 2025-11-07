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
```

2) Login — by username

```bash
curl -s -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"username":"filfai","password":"secret"}'
```

3) Login — by email

```bash
curl -s -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"filfai@example.com","password":"secret"}'
```

4) Authenticate — validate/refresh token

```bash
curl -s -X GET "http://127.0.0.1:8000/auth/authenticate" -H "Authorization: Bearer <TOKEN>"
```

5.a) Get user — retrieve user public info (requires Authorization header)

```bash
curl -s -X GET "http://127.0.0.1:8000/user/<USER_ID>"
```

5.b) Get user by username — retrieve user public info by username

```bash
curl -s -X GET "http://127.0.0.1:8000/user/username/filfai"
```