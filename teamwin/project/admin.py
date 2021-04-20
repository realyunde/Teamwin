from django.contrib import admin
from .models import Project, Role, Member, WorkItemType, WorkItemPriority, WorkItemStatus, WorkItem

admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Member)
admin.site.register(WorkItemType)
admin.site.register(WorkItemPriority)
admin.site.register(WorkItemStatus)
admin.site.register(WorkItem)
