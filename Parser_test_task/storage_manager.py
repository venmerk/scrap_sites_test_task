import csv
from natsort import natsorted

def save_to_csv(content, path, headers=None):
    """
    Write parsed content to csv file.
    :param content: List of dicts.
    :param path: String with relative filename path.
    :param headers: Custom csv headers (if needed).
    """

    # keys to group columns by
    keys = set()
    for dict in content:
        for key in dict.keys():
            keys.add(key)

    keys = natsorted(keys)

    # clean headers
    if not headers:
        headers = {
            k: k.replace('_', ' ').upper()
            for k
            in natsorted(keys)
        }

    # writefile
    with open(path, 'w') as file:
        writer = csv.DictWriter(file, keys, extrasaction='ignore')
        writer.writerow(headers)
        for row in content:
            writer.writerow(row)