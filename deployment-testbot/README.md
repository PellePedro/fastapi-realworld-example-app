# FastAPI RealWorld Example App - TestBot Deployment

TestBot-compatible deployment scripts for the FastAPI RealWorld Example App.

## Files

- **setup.sh** - Starts app + PostgreSQL and registers a test user
- **get-token.sh** - Outputs the JWT auth token
- **docker-compose.yaml** - Service configuration

## Usage

```bash
# Start services and create test user
./setup.sh

# Run tests
docker compose --profile test run --rm test

# Get auth token for manual testing
TOKEN=$(./get-token.sh)

# Test API
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/user

# Stop services
docker compose down -v
```

## Application Details

- **Port:** 8000
- **API Base:** http://localhost:8000/api
- **Auth Type:** JWT (via `Authorization: Token <jwt>` header)
- **Test Account:** testbot@example.com / TestPass123!

## API Endpoints

- `POST /api/users` - Register
- `POST /api/users/login` - Login
- `GET /api/user` - Get current user
- `PUT /api/user` - Update current user
- `GET /api/profiles/{username}` - Get profile
- `POST /api/profiles/{username}/follow` - Follow user
- `DELETE /api/profiles/{username}/follow` - Unfollow user
- `GET /api/articles` - List articles
- `POST /api/articles` - Create article
- `GET /api/articles/feed` - Get feed
- `GET /api/articles/{slug}` - Get article
- `PUT /api/articles/{slug}` - Update article
- `DELETE /api/articles/{slug}` - Delete article
- `POST /api/articles/{slug}/favorite` - Favorite article
- `DELETE /api/articles/{slug}/favorite` - Unfavorite article
- `GET /api/articles/{slug}/comments` - List comments
- `POST /api/articles/{slug}/comments` - Create comment
- `DELETE /api/articles/{slug}/comments/{id}` - Delete comment
- `GET /api/tags` - Get all tags
