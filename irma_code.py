import csv
import os


def csv_to_dict(file_path):
    """
    Function to read in a csv file and create a dict based on the first two columns.

    Parameters
    ----------
    - file_path : string
        The filepath to the CSV file.
    
    Returns
    -------
    - csv_dict : dict
        The dict created from the CSV file.

    Tipps
    -------
    - Read in the CSV file from the path
    - For each row, add an entry to a dict (first column is key, second column is value)
    - Return the dict
    """
    with open(file_path) as file:
        dictionary = {}

        for line in file:
            if not line[0].isnumeric():
                continue

            key, content = line.split(';')
            dictionary[key] = content[:-1]

    return dictionary


class IRMA:
    """
    Class to retrieve the IRMA code and information for a given file.
    """
    labels_long = ["Technical code for imaging modality", "Directional code for imaging orientation",
                   "Anatomical code for body region examined", "Biological code for system examined"]
    labels_short = ["Imaging modality", "Imaging orientation", "Body region", "System"]

    def __init__(self, dir_path=f'website{os.sep}static{os.sep}data{os.sep}irma_data{os.sep}'):
        """
        Constructor of an IRMA element.

        Parameters
        ----------
        - dir_path : string
            The path where the irma data is. There should be a "A.csv", "B.csv", "C.csv", "D.csv" and "image_codes.csv" file in the directory.

        Tips
        -------
        - Create a dict for part A, B, C, and D of the IRMA code (user csv_to_dict(file_path))
        - Save the dicts (list) as class variable
        - Save "image_codes.csv" as dict in a class variable
        """

        self.a_dict = csv_to_dict(dir_path + 'A.csv')
        self.b_dict = csv_to_dict(dir_path + 'B.csv')
        self.c_dict = csv_to_dict(dir_path + 'C.csv')
        self.d_dict = csv_to_dict(dir_path + 'D.csv')

        self.dicts = [self.a_dict, self.b_dict, self.c_dict, self.d_dict]

        self.image_dict = csv_to_dict(dir_path + 'image_codes.csv')

    def get_irma(self, image_names):
        """
        Function to retrieve irma codes for given image names.

        Parameters
        ----------
        - image_names : list
            List of image names.

        Returns
        -------
        - irma codes : list
            Retrieved irma code for each image in 'image_list'

        Tipps
        -------
        - Remove file extension and path from all names in image_names. Names should be in format like first column of 'image_codes.csv'
        - Use self.image_dict to convert names to codes. ('None' if no associated code can be found)
        - Return the list of codes
        """
        code_list = []

        for image in image_names:
            image = image[:-4]

            if not self.image_dict.__contains__(image):
                code_list.append(None)
                continue

            code_list.append(self.image_dict[image])

        return code_list

    def decode_as_dict(self, irma_code) -> dict:
        """
        Function to decode an irma code to a dict.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : dict

        Tipps
        -------
        - Make use of 'labels_short'
        - Possible solution: {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], ...}
        - Solution can look different
        """
        print(irma_code)

        result = {}

        if not irma_code:
            return result

        for code, label, dictionary in zip(irma_code.split('-'), self.labels_short, self.dicts):
            if code[0] == '0':
                result[label] = [dictionary['0']]
                break

            code_acc = ''
            list_acc = []

            for number in code:
                if number == '0':
                    break
                else:
                    code_acc += number
                    try:
                        list_acc.append(dictionary[code_acc])
                    except KeyError:
                        list_acc.append(f'Invalid key: {code_acc}')

            result[label] = list_acc

        return result

    def decode_as_str(self, irma_code):
        """
        Function to decode an irma code to a str.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : str
            List of decoded strings.

        Tipps
        -------
        - Make use of 'decode_as_dict'
        - Possible solution: ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
        - Solution can look different -> FLASK will use this representation to visualize the information on the webpage.
        """
        dictionary = self.decode_as_dict(irma_code)

        result = []

        for key, value in dictionary.items():
            value = ', '.join(value)
            result.append(f'{key}: {value}')

        return result


if __name__ == '__main__':
    image_names = ["9550.png"]

    irma = IRMA()

    codes = irma.get_irma(image_names)

    print('Codes: ')
    print('-' * len('Codes:'))
    print(str(codes) + '\n')

    if codes is not None:
        code = codes[0]
        print(f'Dict:\n' + '-' * len('Dict:'))
        print(str(irma.decode_as_dict(code)) + '\n')

        print(f'String: \n' + '-' * len('String:'))
        [print(elem) for elem in irma.decode_as_str(code)]

    '''
    Result could look like this:


    Codes:  ['1121-127-700-500']
    Dict:
    {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], 'Imaging orientation': ['coronal', 'anteroposterior (AP, coronal)', 'supine'], 'Body region': ['abdomen', 'unspecified'], 'System': ['uropoietic system', 'unspecified']}


    String:
    ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
    '''
