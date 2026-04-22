# Authentication System

The Foolstack project uses JWT (JSON Web Tokens) for authentication with a custom user model that uses email addresses instead of usernames.

## Overview

- **Library**: `djangorestframework-simplejwt`
- **Authentication Method**: JWT tokens (Bearer token)
- **User Identification**: Email address (no username field)
- **Token Types**: Access tokens (60 min) + Refresh tokens (7 days)
- **Password Validation**: Django's built-in validators

## Custom User Model

Located in `server/users/models.py`, our custom user model extends Django's `AbstractBaseUser` and inherits from `core.models.BaseModel`.

### Fields
- `id` (CharField, unique, primary key) - **ULID** (26 characters)
- `email` (EmailField, unique) - Primary identifier
- `first_name` (CharField, optional)
- `last_name` (CharField, optional)
- `is_active` (BooleanField, default=True)
- `is_staff` (BooleanField, default=False)
- `created_at` (DateTimeField, auto-generated)
- `updated_at` (DateTimeField, auto-updated)

### Properties
- `full_name` - Returns concatenated first and last name
- `USERNAME_FIELD = 'email'` - Uses email for authentication

## API Endpoints

All authentication endpoints are prefixed with `/api/auth/`

### 1. User Registration

**Endpoint**: `POST /api/auth/register/` (Disabled by default, uncomment in `users/urls.py` to enable)

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
    "date_joined": "2026-04-22T13:30:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. User Login

**Endpoint**: `POST /api/auth/login/`

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
    "date_joined": "2026-04-22T13:30:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Token Refresh

**Endpoint**: `POST /api/auth/token/refresh/`

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

## JWT Configuration

Located in `server/core/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),    # 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # 1 week
    'ROTATE_REFRESH_TOKENS': True,                     # Generate new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,                  # Blacklist old refresh tokens
    'UPDATE_LAST_LOGIN': True,                         # Update user's last_login field
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

## Frontend Integration

### Pinia Auth Store

The central authentication state is managed in `client/src/stores/auth.js`.

```javascript
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// Login
await auth.login({ email: '...', password: '...' })

// Check status
console.log(auth.isAuthenticated)
console.log(auth.user)

// Logout
auth.logout()
```

### Axios Client & Interceptors

The `client/src/apiClient/client.js` is pre-configured with interceptors to:
1. Automatically inject the `Authorization: Bearer <token>` header for all requests if a token exists.
2. Intercept `401 Unauthorized` responses, attempt to refresh the token automatically, and retry the original request.
3. Redirect to `/login` if the refresh token has also expired.

```javascript
import { client } from '@/apiClient/client'

// Tokens are handled automatically
const response = await client.get('/some-protected-endpoint/')
```

## Django Admin Integration

The custom user model is fully integrated with Django admin:
- Located at `/admin/`
- Custom admin interface for user management
- Supports all standard Django admin features
- Email-based login for admin users

## Testing

Example test cases for authentication:

```python
# server/users/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        # Ensure register is uncommented in urls.py for this test
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')

    def test_user_login(self):
        # Create user first
        User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
```
