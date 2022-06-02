import io
import json
import pandas as pd
from jsonschema import validate
from jsonschema.exceptions import ValidationError

schema = open('default.json', 'r')
schema = json.load(schema)
dados = open('massa.txt', 'rb')
dados = dados.read()


def open_file():
    file = pd.read_csv(io.BytesIO(dados),encoding='utf-8',
                       header=0, sep=';').to_dict(orient='records')
    lista_ok, lista_nok, count = [], [], 2
    for i in file:
        is_valid = validate_schema(i)
        if is_valid[0]:
            lista_ok.append(i)
        else:
            erro = is_valid[1]
            lista_nok.append(f'linha {count}, campo: {erro.path[0]}, descrição do erro: {erro.args[0]}')
        count += 1
    for i in lista_nok:
        print(i)


def validate_schema(line):
    try:
        validate(instance=line, schema=schema)
        return True, ''
    except ValidationError as err:
        return False, err


open_file()
