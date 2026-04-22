# API Reference

Complete API documentation for the Foolstack project.

## Base URL

- **Development**: `https://localhost/api`
- **Production**: `https://yourdomain.com/api`

## Authentication

Protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

See [Authentication](./authentication.md) for complete auth documentation.

## Endpoints

### Health Check

#### Ping (Fast)
```
GET /api/ping/
```

Quick health check used by Docker healthchecks. Verifies database connectivity.

**Response** (200 OK):
```json
{
  "status": "ok",
  "timestamp": "2026-04-22T12:00:00Z"
}
```

#### Health (Comprehensive)
```
GET /api/health/
```

Full system health check including database, Redis, and disk space.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "checks": {
    "database": {
      "status": "healthy"
    },
    "redis": {
      "status": "healthy"
    },
    "disk": {
      "status": "healthy",
      "free_gb": 50.5
    }
  }
}
```

### Authentication

#### Register
```
POST /api/auth/register/
```

Create a new user account. Returns tokens and user data.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": "01J9H9F1V2X3Y4Z5A6B7C8D9E0",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "date_joined": "2026-04-22T12:00:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Login
```
POST /api/auth/login/
```

Authenticate an existing user. Returns tokens and user data.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "01J9H9F1V2X3Y4Z5A6B7C8D9E0",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "date_joined": "2026-04-22T12:00:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token
```
POST /api/auth/token/refresh/
```

Get a new access token using a refresh token.

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Get Profile
```
GET /api/auth/profile/
```

Get the authenticated user's profile. Requires authentication.

**Headers**: `Authorization: Bearer <access_token>`

**Response** (200 OK):
```json
{
  "id": "01J9H9F1V2X3Y4Z5A6B7C8D9E0",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "date_joined": "2026-04-22T12:00:00Z"
}
```

#### Update Profile
```
PUT /api/auth/profile/
PATCH /api/auth/profile/
```

Update the authenticated user's profile. Requires authentication.

**Headers**: `Authorization: Bearer <access_token>`

**Request Body** (PATCH for partial update):
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

**Response** (200 OK):
```json
{
  "id": "01J9H9F1V2X3Y4Z5A6B7C8D9E0",
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "full_name": "Jane Smith",
  "date_joined": "2026-04-22T12:00:00Z"
}
```

### Admin

```
GET /admin/
```

Django admin interface. Requires staff user credentials (session-based auth).

## Error Responses

All endpoints return consistent error formats:

### Validation Error (400)
```json
{
  "email": ["This field is required."],
  "password": ["This password is too short."]
}
```

### Authentication Error (401)
```json
{
  "detail": "Invalid email or password."
}
```

### Permission Denied (403)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found (404)
```json
{
  "detail": "Not found."
}
```

### Server Error (500)
```json
{
  "detail": "Internal server error."
}
```

## Token Lifetimes

| Token Type | Default Lifetime | Notes                             |
|------------|------------------|-----------------------------------|
| Access     | 60 minutes       | Short-lived, use for API requests |
| Refresh    | 7 days           | Use to get new access tokens      |

Refresh tokens are rotated on use (old token is blacklisted).

---

*See [Authentication](./authentication.md) for more details on the auth system.*
