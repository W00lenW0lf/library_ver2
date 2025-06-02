from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json, os
import urllib.parse

BOOKS_PER_PAGE = 10


def source_input():
    data_file_path = input('Введите путь к файлу с данными (по умолчанию: meta_data.json): ').strip()
    if not data_file_path:
        data_file_path = 'meta_data.json'

    config_file_path = input('Введите путь к конфигурационному файлу (по умолчанию: template.html): ').strip()
    if not config_file_path:
        config_file_path = 'template.html'

    return data_file_path, config_file_path


def main(data_file_path, config_file_path):
    books_on_page = 10
    with open(data_file_path, 'r', encoding='utf-8') as my_file:
        library = json.load(my_file)

    os.makedirs('pages', exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.filters['urlencode'] = urlencode_filter
    template = env.get_template(config_file_path)

    chunked_books = [library[i:i + 10] for i in range(0, len(library), 10)]
    total_pages = len(chunked_books)

    for page_num, books_chunk in enumerate(chunked_books, 1):
        rendered_page = template.render(
            books=books_chunk,
            current_page=page_num,
            total_pages=total_pages
        )
        page_filename = f'pages/page_{page_num}.html'
        with open(page_filename, 'w', encoding='utf-8') as page_file:
            page_file.write(rendered_page)


def urlencode_filter(value):
    return urllib.parse.quote(value)


if __name__ == '__main__':
    data_path, config_path = source_input()
    main(data_path, config_path)

    server = Server()
    server.watch(config_path, lambda: main(data_path, config_path))
    server.watch(data_path, lambda: main(data_path, config_path))
    server.serve(root='.')
