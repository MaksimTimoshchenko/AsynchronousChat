import yaml


def write_to_yaml():
    dict_to_yaml = {
        'list': ['some', 'list'],
        'integer': 1,
        'dict': {'1€': 'dict'}
    }

    with open('file.yaml', 'w') as f_n:
        yaml.dump(dict_to_yaml, f_n, default_flow_style=False, allow_unicode=True)

    with open('file.yaml') as f_n:
        dict_from_yaml = yaml.load(f_n)

    return print("Словари", dict_to_yaml, "и", dict_from_yaml, ('разные', 'идентичные')[dict_to_yaml == dict_from_yaml])

if __name__ == '__main__':
    write_to_yaml()