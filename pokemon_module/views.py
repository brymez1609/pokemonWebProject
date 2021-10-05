from django.http import Http404, HttpResponseGone
from django.shortcuts import render


# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pokemonProject.utils import CsvTool


class PokemonAPIView(APIView):
    csvInstance = CsvTool("pokemon.csv")
    """
    This is an API CRUD for pokemons in a csv file.
    """
    def get(self, request):
        """
        This method retrieve a list of Pokemons or just one pokemon.
        :param request:
        :return: Context Data from client.

        Query params:
        :param page_size:
        :return: Page size, by default it returns 10 items.

        :param index_id:
        :return: If you want to get only one item.

        :param page:
        :return: Page, by default is 0.
        """
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
        """
        This method edit pokemon by "pk" param.
        If the pokemon does not exists it returns Http404 error.
        :param request:
        :param pk:
        :return: The new pokemon edited.
        """
        self.csvInstance.get(index_id=pk)
        new_pokemon_object = self.csvInstance.edit(index_id=pk, json=request.data)
        return Response(new_pokemon_object, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        This method delete pokemon by "pk" param
        If the pokemon does not exists it returns a Http404 error.
        :param request:
        :param pk:
        :return:
        """
        self.csvInstance.get(index_id=pk)
        self.csvInstance.delete(index_id=pk)
        return Response({"detail": "Pokemon deleted correctly"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        """
        This method create a new Pokemon object:
        example of post:
        {
            "Name": "Celeby",
            "Type 1": "Grass",
            "Type 2": "Poison",
            "Total": 318,
            "HP": 45,
            "Attack": 49,
            "Defense": 49,
            "Sp. Atk": 65,
            "Sp. Def": 65,
            "Speed": 45,
            "Generation": 1,
            "Legendary": false
        }
        :param request:
        :return:
        """
        try:
            self.validate_data(request.data)
            pokemon_created = self.csvInstance.create(request.data)
            return Response(pokemon_created, status="201")
        except Exception as e:
            return Response({"detail": str(e)}, status="400")

    def validate_data(self, data):
        """
        This method validate all fields that are required for save a new pokemon object.
        :param data:
        :return: a list of fields (Column names)
        """
        required_fields = ["Name", "Type 1", "Attack", "HP", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Generation"]
        try:
            for field in required_fields:
                val = data[field]
        except KeyError as e:
            raise Exception("column '{}' is required".format(e.args[0]))