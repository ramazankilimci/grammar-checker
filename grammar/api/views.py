from rest_framework import serializers, viewsets
from rest_framework.response import Response

from grammar.models import Spell
from grammar.services import spell_sentence
from .serializers import SpellSerializer
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

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
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def spell_check(request):
    """
    List all spell checks, or create a new spell check.
    """
    if request.method == 'GET':
        spellings = Spell.objects.all()
        serializer = SpellSerializer(spellings, many=True)
        return JsonResponse(serializer.data, safe=False)


    elif request.method == 'POST':
        print('User:', request.user.id)
        data = JSONParser().parse(request)
        print('Data:', data)
        serializer = SpellSerializer(data=data, context={'request': request})
        print('Serializer:', serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def spell_check_detail(request, pk):
    """
    Retrieve, update or delete a cspell check.
    """
    try:
        spell = Spell.objects.get(pk=pk)
    except Spell.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SpellSerializer(spell)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SpellSerializer(spell, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        spell.delete()
        # return HttpResponse(status=204)
        return JsonResponse({'deleted': True})