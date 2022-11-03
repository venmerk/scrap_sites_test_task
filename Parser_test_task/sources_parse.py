
from Parser_test_task.parser import BaseParser
from Parser_test_task.storage_manager import save_to_csv

from datetime import datetime

now = datetime.now()
date_string = now.strftime("_%d_%m_%Y")


def parse_and_save(source_class):
    """
    Parse all mocked-db sources and save results to csv by category.
    :param source_class: class from sources_mock_db script. should be changed to db/file in future.
    """

    source_url = source_class.url
    file_tag = source_class.name_util

    for category, params in source_class.categories.items():
        print(f'Parsing category:{category}, for {source_class}')

        # params
        link = source_url + params['link_rel']
        links_class = params['nested_links_class']
        context_dict = params['context_dict']

        # parse
        content = BaseParser.parse_pages(link, links_class, context_dict)

        # save
        print(f'Saving parsed data to file... "storage/{file_tag}_{category}_{date_string}.csv"')
        save_to_csv(content, f'storage/{file_tag}_{category}_{date_string}.csv')
