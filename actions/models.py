from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import JSONField

# Create your models here.
class Action(models.Model):
    activity = (('1', 'Spell'),
                ('2', 'Follow'),
                ('3', 'Unfollow'),
                ('4', 'Search'))

    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=CASCADE)
    verb = models.CharField(max_length=255, choices=activity)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                db_index=True)
    action_json = JSONField(default=dict)

    class Meta:
        ordering = ('-created',)