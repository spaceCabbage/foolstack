# Authentication System

The Gelt project uses JWT (JSON Web Tokens) for authentication with a custom user model that uses email addresses instead of usernames.

## Overview

- **Library**: `djangorestframework-simplejwt`
- **Authentication Method**: JWT tokens (Bearer token)
- **User Identification**: Email address (no username field)
- **Token Types**: Access tokens (60 min) + Refresh tokens (7 days)
- **Password Validation**: Django's built-in validators

## Custom User Model

Located in `server/users/models.py`, our custom user model extends Django's `AbstractBaseUser`:

### Fields
- `email` (EmailField, unique) - Primary identifier
- `first_name` (CharField, optional)
- `last_name` (CharField, optional)
- `is_active` (BooleanField, default=True)
- `is_staff` (BooleanField, default=False)
- `date_joined` (DateTimeField, auto-generated)

### Properties
- `full_name` - Returns concatenated first and last name
- `USERNAME_FIELD = 'email'` - Uses email for authentication

## API Endpoints

All authentication endpoints are prefixed with `/api/v1/auth/`

### 1. User Registration

**Endpoint**: `POST /api/v1/auth/register/`

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
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "date_joined": "2025-07-24T13:30:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Validation**:
- Email must be unique and valid format
- Password must pass Django's validation rules
- Password confirmation must match
- First/last names are optional

### 2. User Login

**Endpoint**: `POST /api/v1/auth/login/`

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
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "date_joined": "2025-07-24T13:30:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Token Refresh

**Endpoint**: `POST /api/v1/auth/token/refresh/`

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

### 4. User Profile

**Endpoint**: `GET /api/v1/auth/profile/`

**Headers**: `Authorization: Bearer <access_token>`

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "date_joined": "2025-07-24T13:30:00Z"
}
```

### 5. Update Profile

**Endpoint**: `PUT /api/v1/auth/profile/` or `PATCH /api/v1/auth/profile/`

**Headers**: `Authorization: Bearer <access_token>`

**Request Body** (partial update with PATCH):
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "full_name": "Jane Smith",
  "date_joined": "2025-07-24T13:30:00Z"
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

### JavaScript Example

```javascript
class AuthService {
  constructor() {
    this.baseURL = '/api/v1/auth';
  }

  // Register new user
  async register(userData) {
    const response = await fetch(`${this.baseURL}/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    
    if (response.ok) {
      const data = await response.json();
      this.storeTokens(data.access, data.refresh);
      return data.user;
    }
    throw new Error('Registration failed');
  }

  // Login user
  async login(email, password) {
    const response = await fetch(`${this.baseURL}/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.storeTokens(data.access, data.refresh);
      return data.user;
    }
    throw new Error('Login failed');
  }

  // Make authenticated requests
  async makeAuthenticatedRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    };

    let response = await fetch(url, { ...options, headers });
    
    // If token expired, try to refresh
    if (response.status === 401) {
      const refreshed = await this.refreshToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
        response = await fetch(url, { ...options, headers });
      }
    }
    
    return response;
  }

  // Refresh access token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;

    try {
      const response = await fetch(`${this.baseURL}/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
    
    this.logout();
    return false;
  }

  // Store tokens
  storeTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  // Logout user
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }
}

// Usage
const auth = new AuthService();

// Login
auth.login('user@example.com', 'password123')
  .then(user => console.log('Logged in:', user))
  .catch(err => console.error('Login error:', err));

// Get profile
auth.makeAuthenticatedRequest('/api/v1/auth/profile/')
  .then(response => response.json())
  .then(profile => console.log('Profile:', profile));
```

### Vue 3 Composition API Example

```javascript
// composables/useAuth.js
import { ref, computed } from 'vue'

const user = ref(null)
const tokens = ref({
  access: localStorage.getItem('access_token'),
  refresh: localStorage.getItem('refresh_token')
})

export function useAuth() {
  const isAuthenticated = computed(() => !!tokens.value.access)

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/v1/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      
      if (response.ok) {
        const data = await response.json()
        tokens.value.access = data.access
        tokens.value.refresh = data.refresh
        user.value = data.user
        
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        
        return true
      }
    } catch (error) {
      console.error('Login failed:', error)
    }
    return false
  }

  const logout = () => {
    tokens.value.access = null
    tokens.value.refresh = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    user,
    tokens,
    isAuthenticated,
    login,
    logout
  }
}
```

## Error Handling

### Common Error Responses

**400 Bad Request** - Validation errors:
```json
{
  "email": ["This field is required."],
  "password": ["This password is too short."]
}
```

**401 Unauthorized** - Invalid credentials:
```json
{
  "detail": "Invalid email or password."
}
```

**403 Forbidden** - Permission denied:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Security Considerations

1. **Token Storage**: Store JWT tokens securely (consider httpOnly cookies for production)
2. **HTTPS**: Always use HTTPS in production
3. **Token Expiration**: Access tokens expire after 1 hour
4. **Refresh Rotation**: Refresh tokens are rotated and old ones blacklisted
5. **Password Validation**: Django's built-in password validators are enforced
6. **CORS**: Properly configured for your domain

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
        response = self.client.post('/api/v1/auth/register/', self.user_data)
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
        
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
```

## Migration Notes

When setting up the authentication system:

1. **Initial Migration**: Run `python manage.py makemigrations users` and `python manage.py migrate`
2. **Existing Projects**: If you have existing users, you'll need a data migration
3. **Superuser**: Create with `python manage.py createsuperuser` (will prompt for email instead of username)