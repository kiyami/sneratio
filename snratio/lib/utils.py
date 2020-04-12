import os
import snratio


def check_and_create_directory(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


def generate_package_path(path):
    return os.path.join(os.path.abspath(os.path.dirname(snratio.__path__[0])), path)


def merge_tables(*tables):
    merged_table = tables[0]
    if len(tables) > 1:
        for table in tables[1:]:
            merged_table = merged_table.merge(table, on='Element')

    return merged_table


def division_error(x, x_err, y, y_err):
    x = float(x)
    x_err = float(x_err)
    y = float(y)
    y_err = float(y_err)

    z = x/y
    z_err = z * ((x_err / x) ** 2.0 + (y_err / y) ** 2.0) ** 0.5

    return z, z_err
