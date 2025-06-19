import yaml


def select_token(key='tinybird', file_path='ree_data_tracker/src/.connections.yaml'):
    with open(file_path, 'r') as file:
        body = yaml.safe_load(file)

    return body['credentials'][key]
