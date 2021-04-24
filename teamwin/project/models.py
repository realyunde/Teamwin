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


# Task
class TaskType(models.Model):
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


class TaskStatus(models.Model):
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


class TaskPriority(models.Model):
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


class Task(models.Model):
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
        TaskType,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.ForeignKey(
        TaskStatus,
        null=True,
        on_delete=models.SET_NULL,
    )
    priority = models.ForeignKey(
        TaskPriority,
        null=True,
        on_delete=models.SET_NULL,
    )
    assigned = models.ForeignKey(
        'user.User',
        null=True,
        on_delete=models.SET_NULL,
    )
