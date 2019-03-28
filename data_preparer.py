import json


class CryptoDataPreparer:

    @staticmethod
    def parse_file_data_to_json_object(filepath):
        with open(filepath) as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip() is not ""]

       # headers = lines[0].replace("=", "").split("|")
       # headers[2] = headers[2].strip().split(":")[1].lower()
       # headers[3] = headers[3].strip().split(" ")[1]
       # headers_dict = {"symbol": headers[2].strip(), "timetype": headers[1].strip().replace("timetype", ""), "quantity": headers[3]}
       # headers_dict = json.dumps(headers_dict) '''

        print(lines[1])
        data = [json.loads(line.replace("'", "\"")) for line in lines[1:]]
        my_json = json.loads("{\"data\": [0]}")
        my_json['data'] = data
        return my_json

    @staticmethod
    def delete_empty_elements_from_json_object(json_object):
        json_object['data'] = [x for x in json_object['data'] if (x['close'] + x['high'] + x['volumeto']) > 0]

        return json_object

    @staticmethod
    def parse_json_array_to_array_of_feature_vectors(json_array):
        return [[value for key, value in object.items()] for object in json_array]

    @staticmethod
    def save_array_of_feature_vectors_to_file(array_of_vectors, filepath, file_open_option='a', header=None, save_with_brackets=False):
        with open(filepath, file_open_option) as file:
            if header is not None:
                file.write(header + "\n")

            for vector in array_of_vectors:
                if save_with_brackets:
                    file.write(str(vector) + "\n")
                else:
                    file.write(str(vector)[1:-1] + "\n")

    @staticmethod
    def prepare_data_file_for_ML(filepath, append_data_to_existing_file=False):
        json_object = CryptoDataPreparer.parse_file_data_to_json_object(filepath)
        clear_json_object = CryptoDataPreparer.delete_empty_elements_from_json_object(json_object)
        array_of_feature_vectors = CryptoDataPreparer.parse_json_array_to_array_of_feature_vectors(clear_json_object['data'])

        file_open_option = 'a' if append_data_to_existing_file else 'w'
        CryptoDataPreparer.save_array_of_feature_vectors_to_file(array_of_feature_vectors, filepath, file_open_option)


