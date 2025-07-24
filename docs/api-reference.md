# API Reference

Complete API documentation for the Gelt project.

## Base URL
- **Development**: `http://api.localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication
See [Authentication System](./authentication.md) for complete auth documentation.

- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT/PATCH /api/v1/auth/profile/` - Update user profile

### Health Check
- `GET /health/` - Application health status

### Admin
- `GET /admin/` - Django admin interface

## Error Responses

All endpoints return consistent error formats:

```json
{
  "detail": "Error message",
  "field_errors": {
    "field_name": ["Field-specific error message"]
  }
}
```

## Rate Limiting
*To be implemented*

## Pagination
*To be implemented*

---
*This documentation will be expanded as new endpoints are added.*