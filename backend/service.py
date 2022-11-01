import json

import backend.utils.getScores as getScores
from parsing_2gis import parse_2gis


def get_scores(analog, main_flat):
    corrections = {'bid adjustment': getScores.correct_bid_adjustment(),
                   'floor': getScores.correct_floors(analog, main_flat),
                   'the area of the apartment': getScores.correct_apartment_area(analog, main_flat),
                   'kitchen area': getScores.correct_kitchen_area(analog, main_flat),
                   'the presence of a balcony / loggia': getScores.correct_balcony(analog, main_flat),
                   'distance to the metro': getScores.correct_metro(analog, main_flat),
                   'finishing condition': getScores.correct_condition(analog, main_flat)}
    return corrections


def find_analogs(main_flat):
    all_analogs = parse_2gis(main_flat['address'])
    for analog in all_analogs:
        analog['correction'] = get_scores(analog['content'], main_flat)
    return sorted(all_analogs, key=lambda curr_analog: curr_analog['final_score'], reverse=True)


# if __name__ == '__main__':
    # find_analogs()
