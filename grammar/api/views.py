from rest_framework import serializers, viewsets
from rest_framework.response import Response

from grammar.models import Spell
from grammar.services import spell_sentence
from .serializers import SpellSerializer
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view



# class SpellViewSet(viewsets.ModelViewSet):
#     queryset = Spell.objects.all()
#     serializer_class = SpellSerializer
    
#     @action(detail=True,
#             methods=['post'],
#             authentication_classes=[BasicAuthentication],
#             permission_classes=[IsAuthenticated])
#     def spellcheck(self, request, *args, **kwargs):
#         spell = self.get_object()
#         spell.user.add(request.user)
#         return Response({'spelled': True})


@api_view(['GET', 'POST'])
def spell_check(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        spellings = Spell.objects.all()
        serializer = SpellSerializer(spellings, many=True)
        return JsonResponse(serializer.data, safe=False)


    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('Data:', data)
        serializer = SpellSerializer(data=data)
        print('Serializer:', serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)