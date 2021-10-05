import pandas
from math import isnan

from django.http import Http404


class CsvTool:
    def __init__(self, file_dir_name):
        self.file_dir_name = file_dir_name
        self.pokemon_data_frame = None
        self.read_file()
        self.head_names_list = self.pokemon_data_frame.head().columns.tolist()

    def get(self, page=0, page_size=10, index_id=None):
        pokemon_dict = []
        if index_id is None:
            if not "index_id" in self.head_names_list:
                self.head_names_list.insert(0, "index_id")
            self.pokemon_data_frame = self.pokemon_data_frame.fillna(" ")
            filtered_pokemon_list = self.pokemon_data_frame.to_records(index=False)[
                                    page_size * page:(page_size * page) + page_size].tolist()
            for pokemon in filtered_pokemon_list:
                pokemon_clean_nan = self.clean_NaN_values(pokemon)
                pokemon_dict.append(dict(zip(self.head_names_list, pokemon_clean_nan)))
        else:
            try:
                filtered_pokemon_list = self.pokemon_data_frame.loc[index_id, :].to_list()
            except KeyError:
                raise Http404
            pokemon_clean_nan = self.clean_NaN_values(filtered_pokemon_list)
            pokemon_dict.append(dict(zip(self.head_names_list, pokemon_clean_nan)))
            if len(pokemon_dict) == 0:
                raise Http404
        return pokemon_dict

    def read_file(self):
        self.pokemon_data_frame = pandas.read_csv(self.file_dir_name)

    def edit(self, index_id, json=None):
        pokemon_dict = []
        try:
            self.pokemon_data_frame.loc[index_id, :].to_list()
        except KeyError:
            raise Http404
        for field in json.keys():
            self.pokemon_data_frame.loc[index_id, field] = json[field]
        pokemon_clean_nan = self.clean_NaN_values(self.pokemon_data_frame.loc[index_id, :].to_list())
        pokemon_dict.append(dict(zip(self.head_names_list, pokemon_clean_nan)))
        self.pokemon_data_frame.to_csv(self.file_dir_name, index=False)

        json["index_id"] = self.pokemon_data_frame.index.shape[0]
        return pokemon_dict

    def create(self, json=None):
        pokemon_number = int(self.pokemon_data_frame.to_records()[-1:]["#"]) + 1
        json["#"] = pokemon_number
        json["index_id"] = self.pokemon_data_frame.index.shape[0]
        self.pokemon_data_frame = self.pokemon_data_frame.append(json, ignore_index=True)

        self.pokemon_data_frame.to_csv(self.file_dir_name, index=False)
        return json

    def delete(self, index_id):
        self.pokemon_data_frame.drop(self.pokemon_data_frame.index[index_id],
                               axis=0, inplace=True)
        self.pokemon_data_frame.to_csv(self.file_dir_name, index=False)

    def clean_NaN_values(self, list_values):
        new_list = []
        for value in list_values:
            if isinstance(value, float):
                if isnan(value):
                    new_list.append("")
                else:
                    new_list.append(value)
            else:
                new_list.append(value)
        return new_list

