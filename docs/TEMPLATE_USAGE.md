# 📖 Foolstack Template Usage Guide

This guide will help you customize the Foolstack template for your specific project needs.

## 🎯 Getting Started with the Template

### 1. Create Your Project

#### Option A: GitHub Template (Recommended)
```bash
# Using GitHub UI:
# 1. Go to the foolstack repository
# 2. Click "Use this template" button
# 3. Name your new repository
# 4. Clone your new repo

# Using GitHub CLI:
gh repo create myproject --template yourusername/foolstack --clone
cd myproject
```

#### Option B: Manual Clone
```bash
git clone https://github.com/yourusername/foolstack.git myproject
cd myproject
rm -rf .git
git init
git add .
git commit -m "Initial commit from foolstack template"
```

### 2. Initial Setup

```bash
# One-command setup
make setup

# This automatically:
# - Creates .env with secure defaults
# - Builds all Docker containers
# - Runs database migrations
# - Starts all services

# Create your admin user
make superuser
```

### 3. Verify Everything Works

- Frontend: http://localhost
- API: http://api.localhost
- Admin: http://api.localhost/admin

## 🔧 Customization Steps

### 1. Update Project Metadata

#### Backend (Django)
Edit `server/pyproject.toml`:
```toml
[tool.poetry]
name = "myproject"
description = "My awesome project"
authors = ["Your Name <you@example.com>"]
```

Edit `server/core/settings.py`:
```python
# Update the project name in settings
WSGI_APPLICATION = 'core.wsgi.application'  # Keep as 'core'
```

#### Frontend (Vue)
Edit `client/package.json`:
```json
{
  "name": "myproject-frontend",
  "version": "0.1.0",
  "description": "My project frontend"
}
```

Edit `client/index.html`:
```html
<title>My Project</title>
```

### 2. Configure Your Domain

For local development, update `.env`:
```env
BASE_DOMAIN=myproject.local
```

Add to `/etc/hosts`:
```
127.0.0.1 myproject.local
127.0.0.1 api.myproject.local
```

### 3. Create Your First App

```bash
# Create a Django app
make app todos

# This creates server/todos/
# Don't forget to add it to INSTALLED_APPS in settings.py
```

### 4. Remove Template Branding

1. Update `client/src/App.vue` - Remove foolstack references
2. Update `client/src/components/` - Customize components
3. Update `server/core/urls.py` - Change API title
4. Update container names in `docker-compose.yml` (optional)

## 🏗️ Common Customizations

### Add a Database Model

```python
# server/todos/models.py
from django.db import models
from authentication.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

```bash
# Create and apply migrations
make migrations
make migrate
```

### Add an API Endpoint

```python
# server/todos/serializers.py
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('user',)

# server/todos/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

### Add Frontend Routes

```javascript
// client/src/router/index.js
{
  path: '/todos',
  name: 'todos',
  component: () => import('../views/TodosView.vue'),
  meta: { requiresAuth: true }
}
```

### Customize Authentication

The template includes email-based authentication. To customize:

1. Modify `server/authentication/models.py` for user fields
2. Update `server/authentication/serializers.py` for validation
3. Adjust `client/src/stores/auth.js` for frontend handling

## 🚀 Production Deployment

### 1. Environment Configuration

Create production `.env`:
```env
ENVIRONMENT=production
BASE_DOMAIN=myproject.com
DJANGO_SECRET_KEY=<generate-new-secure-key>
CADDY_EMAIL=admin@myproject.com
```

### 2. Database Migration (Optional)

For PostgreSQL in production:
```python
# server/core/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### 3. Deploy

```bash
# Build for production
make prod-build

# Start production services
make prod-up
```

## 📁 Project Structure Decisions

### Why This Structure?

- **Separate client/server directories**: Clear separation of concerns
- **Docker-first approach**: Consistent environments, easy deployment
- **Single .env file**: Centralized configuration
- **Makefile commands**: Simplified developer experience

### Adding New Services

To add Redis, PostgreSQL, or other services:

1. Add to `docker-compose.yml`
2. Update `.env.example` with new variables
3. Add Makefile commands if needed
4. Document in your project README

## 🔍 Debugging Tips

### Common Issues

1. **Port conflicts**: Change `VUE_PORT` or `DJANGO_PORT` in `.env`
2. **Permission errors**: Check Docker volume permissions
3. **CORS issues**: Verify `BASE_DOMAIN` matches your browser URL
4. **Module not found**: Rebuild containers after adding dependencies

### Useful Commands

```bash
# View logs for specific service
docker-compose logs -f server
docker-compose logs -f client

# Access Django shell
make shell-django
python manage.py shell

# Access database
make shell-django
python manage.py dbshell

# Run specific tests
docker-compose exec server poetry run python manage.py test todos
```

## 🤝 Best Practices

1. **Keep the template structure**: It's designed for scalability
2. **Use environment variables**: Never hardcode sensitive data
3. **Follow Django/Vue conventions**: The template sets good patterns
4. **Document your changes**: Update README as you customize
5. **Test in Docker**: Ensure consistency with production

## 🚨 What to Change Immediately

1. **Django SECRET_KEY**: Generate a new one for production
2. **CORS settings**: Update for your domains
3. **API permissions**: Default is AllowAny for some endpoints
4. **Container names**: Optional but recommended for clarity
5. **Git remote**: Point to your repository

## 📚 Next Steps

1. Review the [Developer Documentation](docs/README.md)
2. Explore the authentication system
3. Add your first model and API endpoint
4. Customize the frontend theme
5. Set up your CI/CD pipeline

---

Remember: This template is a starting point. Feel free to modify anything to fit your project's needs!