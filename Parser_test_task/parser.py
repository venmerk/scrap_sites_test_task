import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class BaseParser:
    BASE_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    @classmethod
    def encrypt_cloudfare_email(cls, cf):
        try:
            r = int(cf[:2], 16)
            email = ''.join([chr(int(cf[i:i + 2], 16) ^ r) for i in range(2, len(cf), 2)])
            return email
        except (ValueError):
            pass

    @classmethod
    def get_html(cls, url, headers=BASE_HEADERS, params='') -> str:
        """
        Get requests.models.Response obj from specified.
        :param url: The url of the request.
        :param headers: A dictionary of HTTP headers to send to the specified url.
        :param params: A dictionary, list of tuples or bytes to send as a query string.
        :return: Unicode string with html contents.
        """
        response = requests.get(url, headers=headers, params=params)
        response.encoding = 'utf-8'
        return response.text

    @classmethod
    def get_html_soup(cls, html):
        """
        Return Soup out of given html string.
        :param html: Unicode string with html contents.
        :return: Soup
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @classmethod
    def get_page_follow_links(cls, html, a_class: str) -> list:
        """
        Get list with link pointers.
        :param html: Unicode string with html contents.
        :param a_class: Class to search links.
        :return: list
        """
        soup = cls.get_html_soup(html)
        parsed_items = soup.find_all('a', class_=a_class, href=True)

        urls_list = []
        for item in parsed_items:

            url = item.get('href')
            url = cls.get_absolute_link(soup, url)  # if parsed link is relative

            urls_list.append(url)

        return urls_list

    @classmethod
    def get_absolute_link(cls, soup, url: str, raw=False) -> str:
        """
        Check if parsed link is relative and return absolute if possible.
        :param url: String with relative or absolute url.
        :return: Absolute url as a string.
        """
        if url.startswith('/'):

            try:
                url_base = soup.find('meta', {'property': 'og:url'}).attrs['content']
            except:
                try:
                    url_base = soup.find('link', {'rel': 'canonical'}).get('href')
                except:
                    url_base = ''
                    # add logger.log with info

            if raw:
                url = url_base + url[1:]
            else:
                url = urljoin(url_base, url)

        return url

    @classmethod
    def get_page_content(cls, html, context_dict) -> dict:

        parsed_content_dict = {}
        for entity, context_params in context_dict.items():

            find_params = context_params['find_params']

            # open submenu page if needed
            soup = cls.get_html_soup(html)
            if context_params.get('follow_relative'):
                new_link = cls.get_absolute_link(soup, context_params['follow_relative'], raw=True)
                nested_html = cls.get_html(new_link)
                soup = cls.get_html_soup(nested_html)

            # if many items need to be taken
            parsed_list = [soup.find(**find_params), ]
            if context_params.get('find_all'):
                parsed_list = soup.find_all(**find_params)

            # parse stuff
            for index, parsed_base in enumerate(parsed_list, 1):

                if parsed_base:
                    parsed_clean = ''

                    if context_params.get('nested'):
                        for tag in context_params['nested']:
                            parsed_base = parsed_base.find(tag)

                    # Get clean info
                    if context_params.get('href'):  # if link
                        parsed_clean = parsed_base.get('href')
                        parsed_clean = cls.get_absolute_link(soup, parsed_clean)  # if parsed link is relative

                        # if parsed link is relative
                        if parsed_clean.startswith('/'):
                            url_base = soup.find('link', {"rel": "canonical"}).get('href')
                            parsed_clean = urljoin(url_base, parsed_clean)

                    elif context_params.get('attrs'):  # if get attrs
                        parsed_clean = parsed_base.attrs[context_params['attrs']]

                    else:  # if text
                        if isinstance(context_params.get('contents_index'), int):
                            parsed_base = parsed_base.contents[context_params['contents_index']]

                        get_text_params = {'strip': True}
                        if context_params.get('keep_breaks'):
                            get_text_params['separator'] = "\n"

                        parsed_clean = parsed_base.get_text(**get_text_params)

                    # If regex specified
                    if context_params.get('regex'):
                        parsed_clean = re.search(context_params['regex'], parsed_clean).group()

                    # if encrypting needed
                    if context_params.get('encrypt_email'):
                        parsed_clean = cls.encrypt_cloudfare_email(parsed_clean)

                # if check images
                if context_params.get('check_images'):
                    if not parsed_clean:
                        parsed_base = soup.find(**find_params)
                        images = parsed_base.find_all('img')

                        parsed_clean = ''
                        for image in images:
                            parsed_clean += image['src'] +'\n '

                # add entity + parsed info to output dict
                content_header = '0_' + entity
                if context_params.get('find_all'):
                    content_header = f'{index}_' + entity


                parsed_content_dict[content_header] = parsed_clean

        return parsed_content_dict

    @classmethod
    def parse_pages(cls, url, follow_links_class, context_dict) -> list:
        """
        Parse pages in bulk.
        :param url: The url of the request.
        :param follow_links_class: Class containing nested pages links.
        :param context_dict: Context to parse nested pages.
        :return: List of dicts with parsed data.
        """
        print(f'Parsing link:{url}')

        html = BaseParser.get_html(url)
        follow_links = BaseParser.get_page_follow_links(html, follow_links_class)

        parsed_content_list = []
        for link in follow_links:
            print(f'Parsing link:{link}')

            html = BaseParser.get_html(link)
            content = BaseParser.get_page_content(html, context_dict)
            parsed_content_list.append(content)

        return parsed_content_list


