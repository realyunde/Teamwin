from django.contrib import admin
from .models import Project, Role, Member, TaskType, TaskPriority, TaskStatus, Task

admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Member)
admin.site.register(TaskType)
admin.site.register(TaskPriority)
admin.site.register(TaskStatus)
admin.site.register(Task)
