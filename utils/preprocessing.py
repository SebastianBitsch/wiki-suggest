import json
import zipfile

def extract_article_texts(zip_path:str) -> dict:
    """
    Function for extracting the text field of the dataset: https://www.kaggle.com/datasets/jacksoncrow/wikipedia-multimodal-dataset-of-good-articles/data
    Returns a dictionary of article-id : title + text pairs that can be saved to a file for 
    faster access. The resulting dictionary is 600MB.
    """
    articles = {}

    with zipfile.ZipFile(zip_path, 'r') as z:
        for _, file_info in enumerate(z.infolist()):

            # We ignore meta.json and images and read only text.json
            if file_info.filename.endswith('text.json'):
                
                # Read the file content
                with z.open(file_info) as file:
                    data = json.loads(json.load(file))
                    
                    # Use article_id as key and text as value
                    key = data['id']
                    text = " ||| ".join((data['title'], data['text'])) # TODO: text cleaning !!!
                    
                    articles[key] = text
    return articles


if __name__ == "__main__":
    file_path = "/work3/s204163/wiki/wikipedia-good-articles.zip"
    articles = extract_article_texts(file_path)

    # Save the article texts as id, text
    with open('/work3/s204163/wiki/article_texts1', 'w') as f:
        for article_id, article_text in articles.items():
            f.write(f"{article_id}, {article_text}\n")

    # Save all the ids as a "list"
    with open('/work3/s204163/wiki/article_ids1', 'w') as f:
        for article_id, _ in articles.items():
            f.write(f"{article_id}\n")


