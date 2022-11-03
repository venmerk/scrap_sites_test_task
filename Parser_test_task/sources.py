

from Parser_test_task.sources_context import DouContext, DjinniContext


class Dou(DouContext):
    # this should be transferred to database or document

    url = 'https://jobs.dou.ua/'

    name = 'Dou.ua'
    name_util = 'dou'

    categories = {
        'vacancy': {
            'link_rel': 'vacancies/',
            'nested_links_class': 'vt',
            'context_dict': DouContext.context_dict_vacancy
        },

        'company': {
            'link_rel': 'companies/',
            'nested_links_class': 'cn-a',
            'context_dict': DouContext.context_dict_company
        }
    }


class Djinni(DjinniContext):
    # this should be transferred to database or document

    url = 'https://djinni.co/'

    name = 'Djinni.co'
    name_util = 'djinni'

    categories = {
        'vacancy': {
            'link_rel': 'jobs/',
            'nested_links_class': 'profile',
            'context_dict': DjinniContext.context_dict_vacancy
        }
    }
