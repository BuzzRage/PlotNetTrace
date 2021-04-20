#!/bin/python

def raw_to_csv():
    with open('data.csv', 'w') as csv_file, open('input.data', 'r') as raw_file:
        for line in raw_file:
            csv_file.write(line.replace(" ", ""))

raw_to_csv()
