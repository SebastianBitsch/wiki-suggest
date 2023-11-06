import bz2

# https://stackoverflow.com/a/28712742
import sys
sys.path.insert(0, '..')
from read_revisions import groups, parse_line

# TODO: Could be parallel

def keep_revision(ids_of_text_articles: set, revision: dict) -> bool:
    return revision['article_id'] in ids_of_text_articles

def delete_revisions(input_file_path: str, output_file_path: str, article_ids_file_path: str) -> None:

    # Read the list of article ids for articles that have long text (i.e. are in kaggle dataset)
    raw_data = open(article_ids_file_path, "r").read()
    ids_of_text_articles = set(raw_data.replace('\n', ' ').split("."))

    with bz2.open(input_file_path, 'rt') as input_file, bz2.open(output_file_path, 'wt') as output_file:
        
        for i, line in enumerate(groups(input_file, 14)):
            if keep_revision(ids_of_text_articles, parse_line(line)):
                output_file.write("".join(line))

            if i % 100000 == 0:
                print(f"Read {i}/1632271984 lines")

            # TODO: temporary as to not run on entire dataset
            # if 100 < i:
            #     break


if __name__ == "__main__":
    input_file_path  = '/work3/s204163/wiki/wiki-revisions-dataset.bz2'
    output_file_path = '/work3/s204163/wiki/wiki-revisions-filtered.bz2'
    article_ids_file_path = '/work3/s204163/wiki/article_ids'

    delete_revisions(input_file_path, output_file_path, article_ids_file_path)

