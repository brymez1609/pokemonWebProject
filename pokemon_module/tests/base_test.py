from django.test import TestCase
from pokemonProject.utils import CsvTool


class NewPokemonTestCase(TestCase):

    def setUp(self) -> None:
        csv_tool_instance = CsvTool("pokemon.csv")
        self.name = "Bulbasour"
        self.type_1 = "Grass"
        self.type_2 = ""
        self.attack = 49
        self.HP = 45
        self.defense = 49
        self.sp_atk = 65
        self.sp_def = 65
        self.speed = 45
        self.generation = 1
        self.column_number = 900
        self.legendary = False
        json = {
            "#": self.column_number,
            "Name": self.name,
            "Type 1": self.type_1,
            "Type 2": self.type_2,
            "Total": self.defense,
            "HP": self.HP,
            "Attack": self.attack,
            "Defense": self.defense,
            "Sp. Atk": self.sp_atk,
            "Sp. Def": self.sp_def,
            "Speed": self.speed,
            "Generation": self.generation,
            'Legendary': self.legendary
        }
        self.pokemon = csv_tool_instance.create(json)
        self.pokemon_saved = csv_tool_instance.get(index_id=csv_tool_instance.pokemon_data_frame.index.shape[0] - 1)[0]
        self.assertEqual(self.pokemon_saved, self.pokemon)


class GetPokemonTestCase(TestCase):

    def setUp(self) -> None:
        csv_tool_instance = CsvTool("pokemon.csv")
        self.pokemon = csv_tool_instance.get()
        self.assertEqual(csv_tool_instance.get(), self.pokemon)


class DeletePokemonTestCase(TestCase):

    def setUp(self) -> None:
        csv_tool_instance = CsvTool("pokemon.csv")
        self.pokemon = csv_tool_instance.delete(index_id=1)


class EditPokemonTestCase(TestCase):

    def setUp(self) -> None:
        csv_tool_instance = CsvTool("pokemon.csv")
        self.name = "Bulbasour Test Edit"
        self.type_1 = "Grass Edit"
        self.type_2 = ""
        self.attack = 80
        self.HP = 90
        self.defense = 90
        self.sp_atk = 90
        self.sp_def = 90
        self.speed = 90
        self.generation = 2
        self.column_number = 90
        self.legendary = True
        json_data = {
            "#": self.column_number,
            "Name": self.name,
            "Type 1": self.type_1,
            "Type 2": self.type_2,
            "Total": self.defense,
            "HP": self.HP,
            "Attack": self.attack,
            "Defense": self.defense,
            "Sp. Atk": self.sp_atk,
            "Sp. Def": self.sp_def,
            "Speed": self.speed,
            "Generation": self.generation,
            'Legendary': self.legendary
        }
        self.pokemon = csv_tool_instance.edit(index_id=0, json=json_data)
        self.pokemon_edited = csv_tool_instance.get(index_id=0)
        self.assertEqual(self.pokemon_edited, self.pokemon)
