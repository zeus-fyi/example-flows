import json

from mockingbird.mockingbooks_py.schemas import create_or_update_schema


def schema_create():
    with open('mocks/schema.json', 'r') as file:
        data = json.load(file)
    create_or_update_schema(data)


if __name__ == '__main__':
    schema_create()
