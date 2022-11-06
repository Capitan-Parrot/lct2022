import json

with open('backend/config.json') as file:
    main_config = json.load(file)


def correct_bid_adjustment():
    return main_config['bid adjustment']


def correct_floors(analog, main_flat):
    correction = 0
    config = main_config['apartment floor']
    if main_flat['floor'] == 1:
        if analog['correcting']['floor'] == 1:
            correction = config['first floor']['ff']
        elif analog['correcting']['floor'] == analog['required']['building_num_floors']:
            correction = config['first floor']['lf']
        else:
            correction = config['first floor']['mf']
    elif main_flat['floor'] == main_flat['building_num_floors']:
        if analog['correcting']['floor'] == 1:
            correction = config['last floor']['ff']
        elif analog['correcting']['floor'] == analog['required']['building_num_floors']:
            correction = config['last floor']['lf']
        else:
            correction = config['last floor']['mf']
    else:
        if analog['correcting']['floor'] == 1:
            correction = config['middle floor']['ff']
        elif analog['correcting']['floor'] == analog['required']['building_num_floors']:
            correction = config['middle floor']['lf']
        else:
            correction = config['middle floor']['mf']
    return correction


def correct_apartment_area(analog, main_flat):
    correction = 0
    config = main_config['apartment area']
    if main_flat['square_flat'] < 30:
        if analog['correcting']['square_flat'] < 30:
            correction = config['<30']['<30']
        elif analog['correcting']['square_flat'] < 50:
            correction = config['<30']['30-50']
        elif analog['correcting']['square_flat'] < 65:
            correction = config['<30']['50-65']
        elif analog['correcting']['square_flat'] < 90:
            correction = config['<30']['65-90']
        elif analog['correcting']['square_flat'] < 120:
            correction = config['<30']['90-120']
        else:
            correction = config['<30']['>120']
    elif main_flat['square_flat'] == 30 - 50:
        if analog['correcting']['square_flat'] < 30:
            correction = config['<50']['<30']
        elif analog['correcting']['square_flat'] < 50:
            correction = config['<50']['30-50']
        elif analog['correcting']['square_flat'] < 65:
            correction = config['50']['50-65']
        elif analog['correcting']['square_flat'] < 90:
            correction = config['<50']['65-90']
        elif analog['correcting']['square_flat'] < 120:
            correction = config['<50']['90-120']
        else:
            correction = config['50']['>120']
    elif main_flat['square_flat'] == 50 - 65:
        if analog['correcting']['square_flat'] < 30:
            correction = config['<65']['<30']
        elif analog['correcting']['square_flat'] < 50:
            correction = config['<65']['30-50']
        elif analog['correcting']['square_flat'] < 65:
            correction = config['<65']['50-65']
        elif analog['correcting']['square_flat'] < 90:
            correction = config['<65']['65-90']
        elif analog['correcting']['square_flat'] < 120:
            correction = config['<65']['90-120']
        else:
            correction = config['<65']['>120']
    elif main_flat['square_flat'] == 65 - 90:
        if analog['correcting']['square_flat'] < 30:
            correction = config['<90']['<30']
        elif analog['correcting']['square_flat'] < 50:
            correction = config['<90']['30-50']
        elif analog['correcting']['square_flat'] < 65:
            correction = config['<90']['50-65']
        elif analog['correcting']['square_flat'] < 90:
            correction = config['<90']['65-90']
        elif analog['correcting']['square_flat'] < 120:
            correction = config['<90']['90-120']
        else:
            correction = config['<90']['>120']
    elif main_flat['square_flat'] == 90 - 120:
        if analog['correcting']['square_flat'] < 30:
            correction = config['<120']['<30']
        elif analog['correcting']['square_flat'] < 50:
            correction = config['<120']['30-50']
        elif analog['correcting']['square_flat'] < 65:
            correction = config['<120']['50-65']
        elif analog['correcting']['square_flat'] < 90:
            correction = config['<120']['65-90']
        elif analog['correcting']['square_flat'] < 120:
            correction = config['<120']['90-120']
        else:
            correction = config['<120']['>120']
    else:
        if analog['correcting']['square_flat'] < 30:
            correction = config['<120']['<30']
        elif analog['correcting']['square_flat'] < 50:
            correction = config['<120']['30-50']
        elif analog['correcting']['square_flat'] < 65:
            correction = config['<120']['50-65']
        elif analog['correcting']['square_flat'] < 90:
            correction = config['<120']['65-90']
        elif analog['correcting']['square_flat'] < 120:
            correction = config['<120']['90-120']
        else:
            correction = config['<120']['>120']
    return correction


def correct_kitchen_area(analog, main_flat):
    correction = 0
    config = main_config['kitchen area']
    if main_flat['square_kitchen'] < 7:
        if analog['correcting']['square_kitchen'] < 7:
            correction = config['<7']['<7']
        elif analog['correcting']['square_kitchen'] < 10:
            correction = config['<7']['7-10']
        else:
            correction = config['<7']['10-15']
    elif main_flat['square_kitchen'] < 10:
        if analog['correcting']['square_kitchen'] < 7:
            correction = config['7-10']['<7']
        elif analog['correcting']['square_kitchen'] < 10:
            correction = config['7-10']['7-10']
        else:
            correction = config['7-10']['10-15']
    else:
        if analog['correcting']['square_kitchen'] < 7:
            correction = config['10-15']['<7']
        elif analog['correcting']['square_kitchen'] < 10:
            correction = config['10-15']['7-10']
        else:
            correction = config['10-15']['10-15']
    return correction


def correct_balcony(analog, main_flat):
    correction = 0
    config = main_config['balcony / loggia']
    if main_flat['has_balcony'] == 'no':
        if analog['correcting']['balcony / loggia'] == 'no':
            correction = config['no']['no']
        else:
            correction = config['no']['there is']
    else:
        if analog['correcting']['balcony / loggia'] == 'there is':
            correction = config['there is']['no']
        else:
            correction = config['there is']['there is']
    return correction


def correct_metro(analog, main_flat):
    correction = 0
    config = main_config['metro']
    if main_flat['metro_distance'] < 5:
        if analog['correcting']['metro_distance'] < 5:
            correction = config['<5']['<5']
        elif analog['correcting']['metro_distance'] < 10:
            correction = config['<5']['5-10']
        elif analog['correcting']['metro_distance'] < 15:
            correction = config['<5']['10-15']
        elif analog['correcting']['metro_distance'] < 30:
            correction = config['<5']['15-30']
        elif analog['correcting']['metro_distance'] < 60:
            correction = config['<5']['30-60']
        else:
            correction = config['<5']['60-90']
    elif main_flat['metro_distance'] == '5-10':
        if analog['correcting']['metro_distance'] < 5:
            correction = config['5-10']['<5']
        elif analog['correcting']['metro_distance'] < 10:
            correction = config['5-10']['5-10']
        elif analog['correcting']['metro_distance'] < 15:
            correction = config['5-10']['10-15']
        elif analog['correcting']['metro_distance'] < 30:
            correction = config['5-10']['15-30']
        elif analog['correcting']['metro_distance'] < 60:
            correction = config['5-10']['30-60']
        else:
            correction = config['5-10']['60-90']
    elif main_flat['metro_distance'] == '10-15':
        if analog['correcting']['metro_distance'] < 5:
            correction = config['10-15']['<5']
        elif analog['correcting']['metro_distance'] < 10:
            correction = config['10-15']['5-10']
        elif analog['correcting']['metro_distance'] < 15:
            correction = config['10-15']['10-15']
        elif analog['correcting']['metro_distance'] < 30:
            correction = config['10-15']['15-30']
        elif analog['correcting']['metro_distance'] < 60:
            correction = config['10-15']['30-60']
        else:
            correction = config['10-15']['60-90']
    elif main_flat['metro_distance'] == '15-30':
        if analog['correcting']['metro_distance'] < 5:
            correction = config['15-30']['<5']
        elif analog['correcting']['metro_distance'] < 10:
            correction = config['15-30']['5-10']
        elif analog['correcting']['metro_distance'] < 15:
            correction = config['15-30']['10-15']
        elif analog['correcting']['metro_distance'] < 30:
            correction = config['15-30']['15-30']
        elif analog['correcting']['metro_distance'] < 60:
            correction = config['15-30']['30-60']
        else:
            correction = config['15-30']['60-90']
    elif main_flat['metro_distance'] == '30-60':
        if analog['correcting']['metro_distance'] < 5:
            correction = config['30-60']['<5']
        elif analog['correcting']['metro_distance'] < 10:
            correction = config['30-60']['5-10']
        elif analog['correcting']['metro_distance'] < 15:
            correction = config['30-60']['10-15']
        elif analog['correcting']['metro_distance'] < 30:
            correction = config['30-60']['15-30']
        elif analog['correcting']['metro_distance'] < 60:
            correction = config['30-60']['30-60']
        else:
            correction = config['30-60']['60-90']
    else:
        if analog['correcting']['metro_distance'] < 5:
            correction = config['60-90']['<5']
        elif analog['correcting']['metro_distance'] < 10:
            correction = config['60-90']['5-10']
        elif analog['correcting']['metro_distance'] < 15:
            correction = config['60-90']['10-15']
        elif analog['correcting']['metro_distance'] < 30:
            correction = config['60-90']['15-30']
        elif analog['correcting']['metro_distance'] < 60:
            correction = config['60-90']['30-60']
        else:
            correction = config['60-90']['60-90']
    return correction


def correct_condition(analog, main_flat):
    correction = 0
    config = main_config['finishing condition']
    if main_flat['condition'] == 'without':
        if analog['correcting']['condition'] == 'without':
            correction = config['without']['w']
        elif analog['correcting']['condition'] == 'economy':
            correction = config['without']['e']
        else:
            correction = config['without']['i']
    elif main_flat['condition'] == 'economy':
        if analog['correcting']['condition'] == 'without':
            correction = config['economy']['w']
        elif analog['correcting']['condition'] == 'economy':
            correction = config['economy']['e']
        else:
            correction = config['economy']['i']
    else:
        if analog['correcting']['condition'] == 'improved':
            correction = config['improved']['w']
        elif analog['correcting']['condition'] == 'economy':
            correction = config['improved']['e']
        else:
            correction = config['improved']['i']
    return correction
