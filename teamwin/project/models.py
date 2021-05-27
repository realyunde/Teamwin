from django.db import models


# Project
class Project(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    description = models.TextField()
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='product_owner',
    )
    master = models.ForeignKey(
        'user.User',
        null=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='scrum_master',
    )


class Developer(models.Model):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
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
