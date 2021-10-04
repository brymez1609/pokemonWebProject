from django.http import Http404, HttpResponseGone
from django.shortcuts import render


# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pokemonProject.utils import CsvTool


class PokemonAPIView(APIView):
    csvInstance = CsvTool("pokemon.csv")

    def get(self, request):
        try:
            page = int(request.GET.get("page", 0))
            page_size = int(request.GET.get("page_size", 10))
            if request.GET.get("index_id", None):
                index_id = int(request.GET.get("index_id", None))
            else:
                index_id = None
        except:
            return Response({"detail": "Error getting params"}, status="400")
        data = self.csvInstance.get(index_id=index_id, page=page,
                                    page_size=page_size)
        return Response(data)

    def put(self, request, pk, ):
        self.csvInstance.get(index_id=pk)
        new_pokemon_object = self.csvInstance.edit(index_id=pk, json=request.data)
        return Response(new_pokemon_object, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        self.csvInstance.get(index_id=pk)
        self.csvInstance.delete(index_id=pk)
        return Response({"detail": "Pokemon deleted correctly"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        try:
            self.validate_data(request.data)
            pokemon_created = self.csvInstance.create(request.data)
            return Response(pokemon_created, status="201")
        except Exception as e:
            return Response({"detail": str(e)}, status="400")

    def validate_data(self, data):
        required_fields = ["Name", "Type 1", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Generation"]
        try:
            for field in required_fields:
                val = data[field]
        except KeyError as e:
            raise Exception("column '{}' is required".format(e.args[0]))