import csv

import pandas as pd

from maps import PANDAS_TO_ARFF

arff_comments = [['% This is a comment'], ['% This is also a comment'], ['%']]


def main():
    data_frame = pd.read_csv('./tests/test_input.csv')
    output_file = open('./tmp/output.arff', 'w+')
    writer = csv.writer(output_file, delimiter=',', quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)

    for comment in arff_comments:
        writer.writerow(comment)

    writer.writerow(['@RELATION "test_relation"'])
    writer.writerow([])

    arff_header = convert_header(data_frame)

    for line in arff_header:
        writer.writerow(line)

    writer.writerow([])
    writer.writerow(['@DATA'])

    for row in arff_rows(data_frame):
        writer.writerow(row)

    output_file.close()


def convert_header(data_frame):
    """
    Converts header from data_frame to arff
    :param data_frame: pandas data_frame
    :param output_file: arff output file
    :return: list of lines
    """
    arff_header = []

    for column in data_frame.columns:
        attribute_name = column
        pd_dtype = str(data_frame[attribute_name].dtype)

        arff_dtype = map_data_types(pd_dtype, data_frame, column)

        line = ['@ATTRIBUTE {} {}'.format(attribute_name, arff_dtype)]
        arff_header.append(line)

    print arff_header
    return arff_header


def map_data_types(pd_dtype, data_frame, column):
    """
    Converts a pandas data type to the corresponding arff data type
    :param pd_dtype: pandas data type as string
    :return: arff data type as string
    """
    try:
        arff_dtype = PANDAS_TO_ARFF[pd_dtype]
    except KeyError:
        if pd_dtype == 'bool':
            # TODO: Implement this
            arff_dtype = map_column_to_arff_class(data_frame, column)
        else:
            raise

    return arff_dtype


def map_column_to_arff_class(data_frame, column):
    """
    Converts 'bool' data type to arff format
    :return: arff class format
    """
    return "NOT YET IMPLEMENTED"


def arff_rows(data_frame):
    """
    Generator that yields arff rows from pandas dataframe
    :param data_frame: pandas dataframe
    :return: arff row
    """
    for pd_row in data_frame.values:
        row = [str(item) for item in pd_row if not isinstance(item, str) or item]
        yield row

if __name__ == '__main__':
    main()