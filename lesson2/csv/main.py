import csv
import re
import getopt, sys


def write_to_csv(path):
    data = get_data()
    with open(path, 'w') as f_n:
        f_n_writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        f_n_writer.writerows(data)

    return

def get_data():
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    os_prod_list, os_name_list, os_code_list, os_type_list = ([] for _ in range(4))
    lists = {'Изготовитель системы': os_prod_list, 'Название ОС': os_name_list, 'Код продукта': os_code_list, 'Тип системы': os_type_list}

    for info_file in files:
        with open(info_file, 'r') as f:
            for line in f:
                result = re.search(r'(Изготовитель системы|Название ОС|Код продукта|Тип системы): ([\w\s_.]+)$', line)
                
                if result:
                    value = result.group(2).replace('\n', '')
                    lists[result.group(1)].append(value)

    main_data = [[*lists]]
    for i, _ in enumerate(files):
        main_data.append([value[i] for value in [os_prod_list, os_name_list, os_code_list, os_type_list]])

    return main_data


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:v", ["output="])

        output = None
        verbose = False
        for o, a in opts:
            if o in ("-o", "--output"):
                output = a
            else:
                assert False, "Unhandled option"
                
        if output:
            write_to_csv(output)
        else:
            print('main.py -o <path/to/csv/file.csv>')
            sys.exit(2)
    except getopt.GetoptError as err:
        print('Error while getting options')
        sys.exit(2)