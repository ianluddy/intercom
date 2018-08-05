# coding=utf-8

import urllib
import json
from math import cos, sin, radians, acos

DATA_SOURCE = "https://s3.amazonaws.com/intercom-take-home-test/customers.txt"
EARTH_RADIUS = 6378 # km
TARGET = 53.339428, -6.257664
MAX_DISTANCE = 100 # km

def parse_input_data(raw_data):
    # Parse and validate the input data
    parsed_data = []
    for record in raw_data.split('\n'):
        try:
            parsed_data.append(parse_and_validate_record(record))
        except (ValueError, TypeError, AttributeError) as e:
            print 'Error parsing record %s - %s' % (record, str(e))

    if not parsed_data:
        print 'No valid records found in input data'

    return parsed_data

def parse_and_validate_record(record):
    json_record = json.loads(record.strip())
    validated_json_record = {
        'latitude': float(json_record.get('latitude')),
        'longitude': float(json_record.get('longitude')),
        'user_id': int(json_record.get('user_id')),
        'name': json_record.get('name')
    }
    assert validated_json_record['name'], 'Invalid name field'
    return validated_json_record

def absolute_difference(x, y):
    # Get absolute distance between two tuple points
    return y[0] - x[0], y[1] - x[1]

def to_radians(point):
    # Convert degrees point tuple to radian point tuple
    return radians(point[0]), radians(point[1])

def central_angle(x, y):
    # Calculate central angle between two tuple points given those points and their absolute difference
    return acos(sin(x[0]) * sin(y[0]) + cos(x[0]) * cos(y[0]) * cos(absolute_difference(x, y)[1]))

def arc_length(sphere_radius, point_angle):
    # Calculate arc length for point angle within sphere of given radius
    return sphere_radius * point_angle

def distance(x, y):
    # Calculate distance between two points on a sphere
    return arc_length(EARTH_RADIUS, central_angle(to_radians(x), to_radians(y)))

def filter_records(target, max_distance, record_list):
    # Filter records by distance and return user_id + name
    filtered = []
    for record in record_list:
        user_distance = distance((record["latitude"], record["longitude"]), target)
        if user_distance < max_distance:
            filtered.append({
                'name': record['name'],
                'user_id': int(record['user_id']),
                'distance': user_distance
            })
    return filtered

def run():
    # Get the raw data
    raw_data = urllib.urlopen(DATA_SOURCE).read()
    if not raw_data:
        print 'Error reading data from source: %s' % DATA_SOURCE
        return

    # Parse and validate the data
    parsed_data = parse_input_data(raw_data)

    # Sort and filter the data
    sorted_filtered_data = sorted(filter_records(TARGET, MAX_DISTANCE, parsed_data), key=lambda k: k['user_id'])

    # Output the results
    for record in sorted_filtered_data:
        print '{user_id}: {name} ({distance} km)'.format(**record)

if __name__ == "__main__":
    run()
