import json
import sqlite3
import argparse

def populate_database(file_path, file_index):
    conn = sqlite3.connect('knowledge_graph.db')
    cursor = conn.cursor()

    with open(file_path, 'r') as file:
        data = json.load(file)
        tuples = data['complete_tuples']

        for t in tuples:
            key, relation, value, type_of_key, type_of_value = t
            cursor.execute('''
            INSERT INTO tuples (key, relation, value, file)
            VALUES (?, ?, ?, ?)
            ''', (key, relation, value, file_index))

            cursor.execute('''
            INSERT INTO types (key, type_of_key, type_of_value)
            VALUES (?, ?, ?)
            ''', (key, type_of_key, type_of_value))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate database with JSON data')
    parser.add_argument('file1', type=str, help='Path to the first JSON file')
    parser.add_argument('file2', type=str, help='Path to the second JSON file')
    
    args = parser.parse_args()
    
    populate_database(args.file1, 1)
    populate_database(args.file2, 2)
