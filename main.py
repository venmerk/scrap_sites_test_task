
from Parser_test_task.sources import Dou, Djinni
from Parser_test_task.sources_parse import parse_and_save

parse_and_save(Dou)
parse_and_save(Djinni)

print('All done.')


# # to test methods separately
# main_page_html = BaseParser.get_html(Dou.url + 'companies/')
# links = BaseParser.get_page_follow_links(main_page_html, 'cn-a')
# html = BaseParser.get_html(links[6])
# content = BaseParser.get_page_content(html, DouContext.context_dict_company)
#
# # content = BaseParser.parse_pages(Dou.url+'companies/', 'cn-a', DouContext.context_dict_company)
# # print(content)