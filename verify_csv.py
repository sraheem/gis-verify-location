import csv
import json
import requests


def reverse_geocode(latitude, longitude):
    endpoint = 'https://alie3fceui.execute-api.us-east-1.amazonaws.com/TEST/reverse-geocode/countrystate'
    query = f'?latitude={latitude}&longitude={longitude}'
    response = requests.get(endpoint + query)
    place = json.loads(response.content)
    country = place['country']
    state = place['gadm1']
    return country, state


def same_country(orig, ret):
    if orig == 'USA' and ret == 'United States':
        return True
    elif orig == ret:
        return True
    else:
        return False


def same_gadm1(orig, ret, country):
    if country == 'Bangladesh':
        if orig == ret + ' ' + 'Division':
            return True
        else:
            return False
    elif orig == ret:
        return True
    else:
        return False


# Main
malformed = 0
errors = 0
with open('all_locations.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        location = row[0]
        latitude = row[1]
        longitude = row[2]

        normalized_location = location.split(',')

        if len(normalized_location) < 3:
            print(f"Not enough elements in Location  -  {location}")
            malformed = malformed + 1
            continue
        else:
            orig_country = normalized_location[-1].strip()
            orig_state = normalized_location[-2].strip()
            geocode = reverse_geocode(latitude, longitude)
            returned_country = geocode[0]
            returned_state = geocode[1]

            if same_country(orig_country, returned_country) and same_gadm1(orig_state, returned_state, orig_country):
                print(f'PASS   -   {location}')
            else:
                errors = errors + 1
                print(f'Mismatch   -  {location}   -   {latitude},{longitude} is in {returned_state}, {returned_country}')


print(f'Total malformed records - {malformed}')
print(f'Errors - {errors}')

