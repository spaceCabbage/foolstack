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
# Start a shell or use manage directly
make manage startapp todos
```

Then add to `INSTALLED_APPS` in `server/core/settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps
    "todos",
]
```

## Adding Models

Always inherit from `core.models.BaseModel` to get **ULID** primary keys and audit fields (`created_at`, `updated_at`).

```python
# server/todos/models.py
from django.db import models
from core.models import BaseModel
from django.conf import settings

class Todo(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

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
        fields = ['id', 'title', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### View

```python
# server/todos/views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer

class TodoListCreateView(ListCreateAPIView):
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListCreateView.as_view(), name='todo-list'),
]
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
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
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

## Adding Background Tasks (Django 6.0)

Foolstack uses the native Django 6.0 task system with a threaded backend. No extra worker container is needed.

```python
# server/todos/tasks.py
from django.tasks import task
from loguru import logger

@task()
def send_reminder_email(todo_id):
    from .models import Todo
    
    try:
        todo = Todo.objects.get(id=todo_id)
        logger.info(f"Processing background task for: {todo.title}")
        # Task logic here
    except Todo.DoesNotExist:
        logger.error(f"Todo {todo_id} not found")
```

Call the task:

```python
from todos.tasks import send_reminder_email
send_reminder_email.enqueue(todo.id)
```

## Frontend Customization

### Adding Vue Routes

```javascript
// client/src/router.js
{
  path: '/todos',
  name: 'todos',
  component: () => import('@/pages/TodosPage.vue'),
}
```

### Making API Calls

```javascript
// Using the configured axios client (handles tokens automatically)
import { client } from '@/apiClient/client'

// GET request
const response = await client.get('/todos/')

// POST request
await client.post('/todos/', { title: 'New todo' })
```

## Environment Configuration

### Customizing Ports

Vite runs on **5173** internally in development. If you need to change exposed Caddy ports, modify `.env`:

```env
CADDY_HTTP_PORT=8080
CADDY_HTTPS_PORT=8443
```

---

*See [API Reference](./api-reference.md) for endpoint documentation.*
