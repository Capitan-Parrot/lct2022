def filter_floors(floor):
    return {"type": "range", "value": {"gte": floor, "lte": floor}}


def filter_segment(segment):
    segment = segment.lower()
    match segment:
        case 'новостройка':
            return {"type": "range", "value": {"gte": 2020}}
        case 'старый жилой фонд':
            return {"type": "range", "value": {"lte": 1988}}
        case 'современное жилье':
            return {"type": "range", "value": {"gte": 1989, "lte": 2019}}


def filter_material(material):
    material = material.lower()
    materials = {'кирпич': [1],
                 'монолит': [2, 8],
                 'панель': [3]}
    return {"type": "terms", "value": materials[material]}
