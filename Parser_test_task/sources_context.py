"""
Context dict format, for each parsed attribute:

context_dict = {
    '<attribute_name>': {

        'find_params': {                 # parameters for soup.find(<x>) method
            'name': '<tag_name>',
            'attrs': {'class': 'date'}   # same as: class_='date'
        },

        'attrs': 'content',              # optional, get tag attribute, for soup.attrs[<x>] method
        'href': True,                    # optional, for soup.get('href') method
        'nested': ['a', 'div'],          # optional, would return same as '<tag_name>.a.div'
        'regex': r"(\d+)",               # optional, performs regex.search after all operations above
        'keep_breaks': True,             # optional, don't strip text formatting
        'check_images': True             # optional, get image links if text is not available
        'follow_relative': '/offices/'   # optional, if need to open relative link from the page
        'find_all': True                 # optional, create an array will all found occurrences
        'encrypt_email': True            # used for cloudfare protection cf
        'contents_index': 0              # when you have <div>text1<span>text2</span><div> it gives text1
    },
}

"""


class DouContext:
    # ---------------------------------------------------------------------
    context_dict_vacancy = {

        'published_date': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'date'}
            },
        },

        'job_title': {
            'find_params': {
                'name': 'h1',
                'attrs': {'class': 'g-h2'}
            },
        },

        'job_link': {
            'find_params': {
                'name': 'meta',
                'attrs': {'property': 'og:url'}
            },
            'attrs': 'content'
        },

        'company': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'l-n'},
            },
            'nested': ['a', ]
        },

        'link_company': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'l-n'},
            },
            'nested': ['a', ],
            'href': True
        },

        'place_type': {
            'find_params': {
                'name': 'span',
                'attrs': {'class': 'place'}
            },
        },

        'description': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'text b-typo vacancy-section'}
            },
            'keep_breaks': True
        }

    }

    # ---------------------------------------------------------------------
    context_dict_company = {

        'company': {
            'find_params': {
                'name': 'h1',
                'attrs': {'class': 'g-h2'},
            },
        },

        'company_link_dou': {
            'find_params': {
                'name': 'meta',
                'attrs': {'property': 'og:url'}
            },

            'attrs': 'content'
        },


        'company_link': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'site'}
            },
            'nested': ['a'],
            'href': True
        },

        'company_size': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'company-info'},
            },

            'regex': r"\d+(\.+)?(\d+)?"
        },

        'description': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'b-typo'}
            },

            'keep_breaks': True,
            'check_images': True
        },

        'company_office_city': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'city'},
            },

            'follow_relative': '/offices/',
            'find_all': True,
            'nested': ['h4', ]
        },


        'company_office_address': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'address'},
            },

            'follow_relative': '/offices/',
            'find_all': True,
            'contents_index': 0,

        },

        'company_email': {
            'find_params': {
                'name': 'span',
                'attrs': {'class': '__cf_email__'},
            },


            'attrs': 'data-cfemail',
            'follow_relative': '/offices/',
            'find_all': True,
            'encrypt_email': True
        },

        'company_phone': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'phones'},
            },

            'follow_relative': '/offices/',
            'find_all': True,
            'keep_breaks': True
        },


    }


class DjinniContext:
    # ---------------------------------------------------------------------
    context_dict_vacancy = {

        'published_date': {
            'find_params': {
                'name': 'p',
                'attrs': {'class': 'text-muted'},
            },
            'regex': r"((0?[1-9]|[12][0-9]|3[01])\s+[^\s]+\s+\d+)"
        },

        'job_title': {
            'find_params': {
                'name': 'h1',
            },
        },

        'job_link': {
            'find_params': {
                'name': 'meta',
                'attrs': {'property': 'og:url'}
            },
            'attrs': 'content'
        },

        'company': {
            'find_params': {
                'name': 'a',
                'attrs': {'class': 'job-details--title'},
            },
        },

        'link_company': {
            'find_params': {
                'name': 'a',
                'attrs': {'class': 'job-details--title'},
            },
            'href': True
        },

        'description': {
            'find_params': {
                'name': 'div',
                'attrs': {'class': 'profile-page-section'}
            },
            'keep_breaks': True
        }

    }
