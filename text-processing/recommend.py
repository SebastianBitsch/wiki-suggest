import numpy as np

from utils.read_data import read_article_ids_file, read_articles_file

def _find_closest_articles(idx: int, n: int, X: np.ndarray, labels: np.ndarray) -> list[int]:
    """
    Finds and returns the indices of the N closest articles to a specified article index,
    within the same class, sorted by distance.

    Parameters
    ----------
    idx : int
        Index of the article in the dataset for which closest articles are to be found.
    n : int
        Number of closest articles to return.
    X : np.ndarray
        Array of feature vectors for all articles in the dataset.
    labels : np.ndarray
        Array of class labels corresponding to each article in the dataset.

    Returns
    -------
    list[int]
        A list of indices of the N closest articles in the same class, sorted by distance.
        The first element is the index of the article itself.
    """


    # Get the vector and the label we are looking for
    vec = X[idx]
    label = labels[idx]

    # Find indices of vectors in the same class in the original dataset
    same_class_indices = np.where(labels == label)[0]
    same_class = X[same_class_indices]

    # calculate and sort by distance
    dists = np.linalg.norm(same_class - vec, axis=1)
    original_indices = same_class_indices[dists.argsort()]

    return original_indices[:n]


def recommend(ids: list[int], n: int = 10, embedding_method: str = 'tfidf', cluster_method: str = 'kmeans', article_ids_path: str = "/work3/s204163/wiki/article_ids") -> list[int]:
    """
    Provides recommendations for a user who has edited a list of articles. 
    Finds similar article based on precomputed feature-vectors and class labels from clustering.

    Parameters
    ----------
    ids : list[int]
        The unique identifier of the article(s) to recommend for
    n : int, optional
        Number of recommendations to return per article, default is 10.
    embedding_method : str, default = 'tfidf'
        The embedding to use when recommending, choices are: 'tfidf', 'sbert'
    cluster_method : str, default = 'k-means'
        The clustering method to use, choices are: 'kmeans', 'dbscan'
    article_ids_path : str, optional
        Path to the article IDs, default is '/work3/s204163/wiki/article_ids'.

    Returns
    -------
    set[int]
        A set of article IDs representing the recommended articles.

    Examples
    --------
    >>> recommend([12345], n=5)
    # Returns a list of IDs for 5 articles recommended based on the article with ID 12345.
    """
    
    # Read the article_ids from the dataset
    article_ids = read_article_ids_file(article_ids_path)
    
    # Get the paths of features and labels based on function input
    base_path = "/work3/s204163/wiki/"
    features_path = f"{base_path}{embedding_method}features.csv"
    text_labels_path = f"{base_path}text_labels_{embedding_method}_{cluster_method}.csv"
    
    # Read the labels from clustering (so we dont have to compute them for every recommendation), 
    # Also read the features vectors we dont have to compute them every time
    labels = np.genfromtxt(text_labels_path, dtype=np.int32, delimiter=",")
    features = np.loadtxt(features_path, delimiter= ",")

    # Create a maping from position in array to id of article and vice versa
    id2index = {id : i for (i, id) in enumerate(article_ids)}
    index2id  = {i : id for (i, id) in enumerate(article_ids)}
    
    # Do recommendations
    recommendations = set()
    for id in ids:
        idx = id2index[id]                                                          # get the index of the id
        r = [index2id[i] for i in _find_closest_articles(idx, n, features, labels)] # add recommendations for this id
        recommendations.update(r)
    
    # Return the ids of the closest articles
    return recommendations


if __name__ == "__main__":

    # Read the data 
    article_texts_path = "/work3/s204163/wiki/article_texts"
    article_ids_path = "/work3/s204163/wiki/article_ids"
    all_articles = read_articles_file(article_texts_path, read_titles = True, return_titles = False)
    article_ids = read_article_ids_file(article_ids_path)

    # Test it works, get the 20 closest articles to some random articles
    neighbours_idx = recommend([11920088], n = 20, embedding_method='sbert', cluster_method='kmeans')
    for id in neighbours_idx:
        print(f"{id} : {all_articles[id][:100]}")