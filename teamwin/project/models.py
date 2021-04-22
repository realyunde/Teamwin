from django.db import models


class Project(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    is_private = models.BooleanField(default=True)
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
    )


class Role(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    permissions = models.TextField(
        null=True,
        blank=True,
    )


class Member(models.Model):
    account = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        Role,
        null=True,
        on_delete=models.SET_NULL,
    )


# WorkItem
class WorkItemType(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )


class WorkItemStatus(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )


class WorkItemPriority(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )


class WorkItem(models.Model):
    title = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    _type = models.ForeignKey(
        WorkItemType,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.ForeignKey(
        WorkItemStatus,
        null=True,
        on_delete=models.SET_NULL,
    )
    priority = models.ForeignKey(
        WorkItemPriority,
        null=True,
        on_delete=models.SET_NULL,
    )
    assigned = models.ForeignKey(
        'user.User',
        null=True,
        on_delete=models.SET_NULL,
    )
