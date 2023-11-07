# import sys
# sys.path.insert(0, '..')
from utils import read_data

article_texts_path = "/work3/s204163/wiki/article_texts"

N = 10
articles = read_data.read_articles_file(article_texts_path, N = N)

print(list(articles.items())[0])