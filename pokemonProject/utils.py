import pandas


class CsvTool:
    def __init__(self, file_dir_name):
        self.file_dir_name = file_dir_name
        self.pokemon_data = None
        self.read_file()
        self.head_names_list = self.pokemon_data.head().columns.tolist()

    def get(self, page=0, page_size=10, index_id=None):
        pokemon_dict = []
        if index_id is None:
            self.head_names_list.insert(0, "index_id")
            filtered_pokemon_list = self.pokemon_data.to_records()[
                                    page_size * page:(page_size * page) + page_size].tolist()
            for pokemon in filtered_pokemon_list:
                pokemon_dict.append(dict(zip(self.head_names_list, pokemon)))
        elif index_id - 1 >= 0:
            filtered_pokemon_list = self.pokemon_data.loc[index_id, :].to_list()
            pokemon_dict.append(dict(zip(self.head_names_list, filtered_pokemon_list)))
        return pokemon_dict

    def read_file(self):
        self.pokemon_data = pandas.read_csv(self.file_dir_name)

    def edit(self, index_id, json=None):
        for field in json.keys():
            self.pokemon_data.loc[index_id, field] = json[field]
        self.pokemon_data.to_csv(self.file_dir_name, index=False)

    def create(self, json=None):
        pokemon_number = int(self.pokemon_data.to_records()[-1:]["#"]) + 1
        json = {'#': pokemon_number, 'Name': 'La Bulba ', 'Type 1': 'Grass', 'Type 2': 'Poison', 'Total': 318, 'HP': 45,
                     'Attack': 49, 'Defense': 49, 'Sp. Atk': 65, 'Sp. Def': 65, 'Speed': 45, 'Generation': 1,
                     'Legendary': False}
        self.pokemon_data = self.pokemon_data.append(json, ignore_index=True)
        self.pokemon_data.to_csv(self.file_dir_name, index=False)

    def delete(self, index_id):
        self.pokemon_data.drop(self.pokemon_data.index[index_id],
                                                   axis=0, inplace=True)
        self.pokemon_data.to_csv(self.file_dir_name, index=False)


if __name__ == "__main__":
    csvTool = CsvTool("../pokemon.csv")
    #csvTool.delete(index_id=0)
    #csvTool.create()
    data = csvTool.get(page=0, page_size=3)
    #data = csvTool.get(index_id=7)
    for a in data:
        print(a)