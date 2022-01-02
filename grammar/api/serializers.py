from django.db import models
from rest_framework import serializers
from grammar.models import Spell
from grammar import services
from rest_framework.fields import CurrentUserDefault

class SpellSerializer(serializers.ModelSerializer):
    #orig_text = serializers.SerializerMethodField()
    spelled_text = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    # I have not defined any "fields" attribute. This will get all fields of the model
    class Meta:
        model = Spell
        fields = ['orig_text', 'spelled_text', 'user']

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     print('Context:', context)
    #     context['spelled_text'] =  spell_sentence(context['orig_text']) # calculate something here, you have access to self.request
    #     return context


    # def get_spelled_text(self, obj):
    #     print('--------Orig_text:----------', obj.orig_text)
    #     srv = services
    #     spelled_text = srv.spell_sentence(obj.orig_text)
    #     return spelled_text
    
    # def get_user(self):
    #     return CurrentUserDefault()

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Spell` instance, given the validated data.
    #     """
    #     return Spell.objects.create(**validated_data)
