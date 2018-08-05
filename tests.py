from intercom import *
import unittest2

class GeoTestCase(unittest2.TestCase):

    #### parse_input_data ####

    def test_parse_input_data_all_valid(self):

        input_data = '''{"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle", "longitude": "-6.043701"}
            {"latitude": "51.92893", "user_id": 1, "name": "Alice Cahill", "longitude": "-10.27699"}
            {"latitude": "51.8856167", "user_id": 2, "name": "Ian McArdle", "longitude": "-10.4240951"}
            {"latitude": "52.3191841", "user_id": 3, "name": "Jack Enright", "longitude": "-8.5072391"}
            {"latitude": "53.807778", "user_id": 28, "name": "Charlie Halligan", "longitude": "-7.714444"}
            {"latitude": "52.833502", "user_id": 25, "name": "David Behan", "longitude": "-8.522366"}'''

        result = parse_input_data(input_data)

        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 6)

    def test_parse_input_data_some_valid(self):

        input_data = '''{"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle", "longitude": "-6.043701"}
            {"latitude": "51.92893", "user_id": 1, "name": "Alice Cahill", "longitude": "-10.27699"}
            {"latitude": 'invalid', "user_id": 2, "name": "Ian McArdle", "longitude": "-10.4240951"}
            {"latitude": "52.3191841", "user_id": 3, "name": "Jack Enright", "longitude": "-8.5072391"}
            {"latitude": "53.807778", "user_id": null, "name": "Charlie Halligan", "longitude": "-7.714444"}
            {"latitude": "52.833502", "user_id": 25, "name": "Nick Enright", "longitude": "-8.522366"}'''

        result = parse_input_data(input_data)

        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 4)

    def test_parse_input_data_empty(self):

        input_data = ''

        result = parse_input_data(input_data)

        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 0)

    #### parse_and_validate_record ####

    def test_parse_and_validate_record_valid(self):

        input = '{"latitude": "52.833502", "user_id": 25, "name": "Jack Enright", "longitude": "-8.522366"}'

        result = parse_and_validate_record(input)

        self.assertEqual(type(result), dict)

    def test_parse_and_validate_record_invalid_lat(self):

        input = '{"latitude": null, "user_id": 25, "name": "Jack Enright", "longitude": "-8.522366"}'

        with self.assertRaises(Exception) as context:
            result = parse_and_validate_record(input)

        self.assertTrue('argument must be a string or a number' in str(context.exception))

    def test_parse_and_validate_record_invalid_lng(self):

        input = '{"latitude": "52.833502", "user_id": 25, "name": "Jack Enright", "longitude": null}'

        with self.assertRaises(Exception) as context:
            result = parse_and_validate_record(input)

        self.assertTrue('argument must be a string or a number' in str(context.exception))

    def test_parse_and_validate_record_invalid_user_id(self):

        input = '{"latitude": "52.833502", "user_id": null, "name": "Jack Enright", "longitude": "-8.522366"}'

        with self.assertRaises(Exception) as context:
            result = parse_and_validate_record(input)

        self.assertTrue('argument must be a string or a number' in str(context.exception))

    def test_parse_and_validate_record_invalid_name(self):

        input = '{"latitude": "52.833502", "user_id": 25, "name": null, "longitude": "-8.522366"}'

        with self.assertRaises(Exception) as context:
            result = parse_and_validate_record(input)

        self.assertTrue('Invalid name field' in str(context.exception))

    #### absolute_difference ####

    def test_absolute_difference(self):
        result = absolute_difference((54, 4), (20, 10))

        self.assertEqual(result[0], -34)
        self.assertEqual(result[1], 6)

    #### to_radians ####

    def test_to_radians(self):
        result = to_radians((10, 20))

        self.assertEqual("{0:.2f}".format(result[0]), '0.17')
        self.assertEqual("{0:.2f}".format(result[1]), '0.35')

    #### central_angle ####

    def test_central_angle(self):
        result = central_angle((10, 20), (50, 5))

        self.assertEqual("{0:.2f}".format(result), '0.71')

    #### arc_length ####

    def test_arc_length(self):
        result = arc_length(6000, 25)

        self.assertEqual(result, 150000)

    # #### distance ####

    def test_distance(self):
        result = distance((20, 5), (22, 7))

        self.assertEqual(int(result), 304)

    #### filter_records ####

    def test_filter_records_all_match(self):
        input = [
            {"latitude": 53.2451022, "user_id": 4, "name": "Ian Kehoe", "longitude": -6.238335},
            {"latitude": 53.1302756, "user_id": 5, "name": "Nora Dempsey", "longitude": -6.2397222},
            {"latitude": 53.1229599, "user_id": 6, "name": "Theresa Enright", "longitude": -6.2705202},
            {"latitude": 54.0894797, "user_id": 8, "name": "Eoin Ahearn", "longitude": -6.18671}
        ]

        result = filter_records((53.339428, -6.257664), 100, input)

        self.assertEqual(type(result), list)
        self.assertEqual(len(list(result)), 4)

    def test_filter_records_some_match(self):
        input = [
            {"latitude": 53.2451022, "user_id": 4, "name": "Ian Kehoe", "longitude": -6.238335},
            {"latitude": 53.1302756, "user_id": 5, "name": "Nora Dempsey", "longitude": -6.2397222},
            {"latitude": 53.1229599, "user_id": 6, "name": "Theresa Enright", "longitude": -6.2705202},
            {"latitude": 54.0894797, "user_id": 8, "name": "Eoin Ahearn", "longitude": -6.18671},
            {"latitude": 51.92893, "user_id": 1, "name": "Alice Cahill", "longitude": -10.27699},
            {"latitude": 51.8856167, "user_id": 2, "name": "Ian McArdle", "longitude": -10.4240951},
            {"latitude": 52.3191841, "user_id": 3, "name": "Jack Enright", "longitude": -8.5072391}
        ]

        result = filter_records((53.339428, -6.257664), 100, input)

        self.assertEqual(type(result), list)
        self.assertEqual(len(list(result)), 4)

    def test_filter_records_no_matches(self):
        input = [
            {"latitude": 51.92893, "user_id": 1, "name": "Alice Cahill", "longitude": -10.27699},
            {"latitude": 51.8856167, "user_id": 2, "name": "Ian McArdle", "longitude": -10.4240951},
            {"latitude": 52.3191841, "user_id": 3, "name": "Jack Enright", "longitude": -8.5072391}
        ]

        result = filter_records((53.339428, -6.257664), 100, input)

        self.assertEqual(type(result), list)
        self.assertEqual(len(list(result)), 0)

    def test_filter_records_empty_input(self):
        input = []

        result = filter_records((53.339428, -6.257664), 100, input)

        self.assertEqual(type(result), list)
        self.assertEqual(len(list(result)), 0)
