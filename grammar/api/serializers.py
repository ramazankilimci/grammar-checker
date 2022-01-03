from django.db import models
from rest_framework import serializers
from grammar.models import Spell
from grammar import services
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.models import User

class SpellSerializer(serializers.ModelSerializer):
    #orig_text = serializers.SerializerMethodField()
    spelled_text = serializers.CharField(allow_blank=True, required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # I have not defined any "fields" attribute. This will get all fields of the model
    class Meta:
        model = Spell
        fields = ['orig_text', 'spelled_text', 'user', 'id', 'spelled_date']

    def create(self, validated_data):
        """
        Create and return a new `Spell` instance, given the validated data.
        """
        srv = services
        spell = Spell(orig_text=validated_data['orig_text'],
                      spelled_text=srv.spell_sentence(validated_data['orig_text']),
                      user = User.objects.get(id=self.context['request'].user.id)
                      )
        spell.save()
        return spell
