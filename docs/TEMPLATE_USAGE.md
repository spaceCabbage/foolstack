# Template Customization Guide

How to customize Foolstack for your project.

> For initial setup, see the [Quick Start](../README.md#quick-start) in the main README.

## Rename the Project

Use `make init` to rename all references from "foolstack" to your project name:

```bash
# Clone the template
git clone https://github.com/yourusername/foolstack.git myproject
cd myproject

# Rename all references
make init myproject

# Now run setup
make setup
```

This updates:
- Container names (`myproject_server`, `myproject_client`, etc.)
- Volume names
- Code references
- Documentation

## Adding Django Apps

```bash
# Start the shell
make shell

# Create a new app
python manage.py startapp todos
exit
```

Then add to `INSTALLED_APPS` in `server/core/settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps
    "todos",
]
```

## Adding Models

```python
# server/todos/models.py
from django.db import models
from django.conf import settings

class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

```bash
make migrations
make migrate
```

## Adding API Endpoints

### Serializer

```python
# server/todos/serializers.py
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['created_at']
```

### View

```python
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

### URLs

```python
# server/todos/urls.py
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

router = DefaultRouter()
router.register('', TodoViewSet, basename='todo')

urlpatterns = router.urls
```

Add to main URLs in `server/core/urls.py`:

```python
urlpatterns = [
    # ... existing paths
    path("api/todos/", include("todos.urls")),
]
```

## Customizing the User Model

The custom User model is in `server/users/models.py`. To add fields:

```python
# server/users/models.py
class User(AbstractBaseUser, PermissionsMixin):
    # ... existing fields

    # Add your fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
```

After adding fields:

```bash
make migrations
make migrate
```

Update the serializer in `server/users/serializers.py` to include new fields.

## Adding Celery Tasks

```python
# server/todos/tasks.py
from celery import shared_task
from loguru import logger

@shared_task
def send_reminder_email(todo_id):
    from .models import Todo

    todo = Todo.objects.get(id=todo_id)
    logger.info(f"Sending reminder for: {todo.title}")
    # Send email logic here
    return f"Reminder sent for {todo.title}"
```

Call the task:

```python
from todos.tasks import send_reminder_email
send_reminder_email.delay(todo.id)
```

## Frontend Customization

### Adding Vue Routes

```javascript
// client/src/router/index.js
{
  path: '/todos',
  name: 'todos',
  component: () => import('../views/TodosView.vue'),
  meta: { requiresAuth: true }
}
```

### Making API Calls

```javascript
// Using the configured axios client
import { client } from '@/apiClient/client'

// GET request
const response = await client.get('/todos/')

// POST request
await client.post('/todos/', { title: 'New todo' })
```

## Environment Configuration

### Development vs Production

The `ENVIRONMENT` variable controls behavior:

| Setting    | Development | Production    |
|------------|-------------|---------------|
| DEBUG      | True        | False         |
| SSL        | Self-signed | Let's Encrypt |
| Hot reload | Enabled     | Disabled      |
| Log level  | DEBUG       | INFO          |

### Custom Ports

Override default ports in `.env`:

```env
SERVER_PORT=8001
CLIENT_PORT=3000
REDIS_PORT=6380
```

## Database Migration (Production)

To use PostgreSQL instead of SQLite:

1. Add `psycopg2-binary` to `server/requirements.txt`

2. Update `server/core/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'foolstack'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

3. Add PostgreSQL service to `docker-compose.yml`

4. Rebuild: `make build && make up`

---

*See [API Reference](./api-reference.md) for endpoint documentation.*
