# Backend — API examples (curl)

This document contains quick curl examples you can use to exercise the backend endpoints while the server is running locally.

Start the server locally (from repository root):

```powershell
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Base URL: `http://127.0.0.1:8000`

## oauth

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

This project stores the access token in an HttpOnly cookie. Use a browser or include the cookie in curl with `--cookie`.

```bash
curl -s -X GET "http://127.0.0.1:8000/auth/authenticate" --cookie "access_token=<TOKEN>"
```

## user

1) Get user by username — retrieve user public info by username

```bash
curl -s -X GET "http://127.0.0.1:8000/user/username/filfai" --cookie "access_token=<TOKEN>"
```

2) Get user — retrieve user public info

```bash
curl -s -X GET "http://127.0.0.1:8000/user/<USER_ID>" --cookie "access_token=<TOKEN>"
```

## game

1) List games

```bash
curl -s -X GET "http://127.0.0.1:8000/game/"
```

2) Create a game

```bash
curl -s -X POST "http://127.0.0.1:8000/game/?title=MyNewGame" -H "Content-Type: application/json" --cookie "access_token=<TOKEN>"
```

3) Get a game by id

```bash
curl -s -X GET "http://127.0.0.1:8000/game/<GAME_ID>"
```

4) List games by owner

```bash
curl -s -X GET "http://127.0.0.1:8000/game/owner/<OWNER_ID>"
```

5) Delete a game

```bash
curl -s -X DELETE "http://127.0.0.1:8000/game/<GAME_ID>" --cookie "access_token=<TOKEN>"
```

## play

1) Player sends a message

```bash
curl -s -X POST "http://127.0.0.1:8000/play/player" -H "Content-Type: application/json" --cookie "access_token=<TOKEN>" -d '{"game_id":"<GAME_ID>", "message":"I open the wooden chest and look inside."}'
```

2) Narrator (AI) generates the next reply

```bash
curl -s -X GET "http://127.0.0.1:8000/play/narrator/<GAME_ID>" --cookie "access_token=<TOKEN>"
```
