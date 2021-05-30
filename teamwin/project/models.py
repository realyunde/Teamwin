from django.db import models


# Project
class Project(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )


class Member(models.Model):
    OWNER = 0
    MASTER = 1
    DEVELOPER = 2

    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    role = models.IntegerField(
        choices=((OWNER, 'Production Owner'), (MASTER, 'Scrum Master'), (DEVELOPER, 'Developer')),
    )

    class Meta:
        unique_together = ('user', 'project')


# Sprint
class Sprint(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    goal = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )


class Task(models.Model):
    subject = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        default='todo',
        choices=(('todo', 'ToDo'), ('doing', 'Doing'), ('done', 'Done')),
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    sprint = models.ForeignKey(
        Sprint,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    assigned = models.ForeignKey(
        'user.User',
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )


class TaskComment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        'user.User',
        null=True,
        on_delete=models.SET_NULL,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )


# Share
class SharedFile(models.Model):
    name = models.CharField(max_length=254)
    path = models.CharField(max_length=64)
    filesize = models.IntegerField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )


# Invitation
class Invitation(models.Model):
    inviter = models.ForeignKey(
        'user.User',
        related_name='inviter',
        on_delete=models.CASCADE,
    )
    invitee = models.ForeignKey(
        'user.User',
        related_name='invitee',
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
