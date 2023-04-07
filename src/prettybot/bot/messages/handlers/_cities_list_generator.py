from src.config.pbconfig import *

__all__ = ['get_similar_cities']


def generate_drop_down_cities_list(cities_list: list) -> str:
    if len(cities_list) > MAX_LEN_SAMPLING_CITIES:
        cities_list[MAX_LEN_SAMPLING_CITIES] += BASE_STATEMENTS.overflow
        cities_list = cities_list[:MAX_LEN_SAMPLING_CITIES + 1]

    return BASE_STATEMENTS.city_sep.join(cities_list)


def get_similar_cities(city: str, cities: dict) -> list:
    result_list = list()
    previous_cities = list()

    for string_idx in range(1, len(city) + 1):
        result_list = _search_cities_by_coincidence(string_idx=string_idx,
                                                    city=city,
                                                    cities=cities,
                                                    length_border=MEDIUM_LEN_SAMPLING_CITIES)

        if not result_list:
            return previous_cities

        previous_cities = result_list

    return result_list


def _search_cities_by_coincidence(string_idx: int, city: str, cities: dict[str], length_border: int) -> list:
    compressed_cities_list = [correct_city.capitalize()
                              for correct_city in cities
                              if correct_city[:string_idx]
                              == city[:string_idx]]

    if len(compressed_cities_list) <= length_border:
        return [cities[correct_city] for correct_city in cities if correct_city[:string_idx] == city[:string_idx]]

    return compressed_cities_list
