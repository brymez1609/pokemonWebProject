from rest_framework.test import APIClient
from pokemon_module.tests import base_test


class NewPokemonTestCase(base_test.NewPokemonTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_new_pokemon(self):
        client = APIClient()
        result = client.post('', {
            "Name": "Bulbasour",
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
            "Legendary": False
        }, format='json')
        self.assertEqual(result.status_code, 201)


class GetPokemonTestCase(base_test.GetPokemonTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_get_pokemon(self):
        client = APIClient()
        result = client.get('', {'index_id': 10}, format='json')
        self.assertEqual(result.status_code, 200)


class DeletePokemonTestCase(base_test.DeletePokemonTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_delete_pokemon(self):
        client = APIClient()
        result = client.delete('/1', {}, format='json')
        self.assertEqual(result.status_code, 204)


class EditPokemonTestCase(base_test.EditPokemonTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_edit_pokemon(self):
        client = APIClient()
        result = client.put('/0', {
            "Name": "Bulbasour Test Case",
            "Type 1": "Grass Test Case",
            "Type 2": "Poison Test Case",
            "Total": 10,
            "HP": 10,
            "Attack": 10,
            "Defense": 10,
            "Sp. Atk": 10,
            "Sp. Def": 10,
            "Speed": 10,
            "Generation": 2,
            "Legendary": False
        }, format='json')
        self.assertEqual(result.status_code, 200)
