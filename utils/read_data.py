from itertools import zip_longest
from datetime import datetime
from random import randint

import pandas as pd
import bz2

# Prefixes of the properties, see: https://snap.stanford.edu/data/wiki-meta.html
PREFIXES = ["CATEGORY", "IMAGE ", "MAIN", "TALK", "USER ", "USER_TALK", "OTHER", "EXTERNAL", "TEMPLATE", "COMMENT", "MINOR", "TEXTDATA"]

ROWS_PER_REVISION = 14                      # The number of rows in a single revision object, should never change
REVISIONS_PER_INDEX = 50                    # How many revisions should there be between indexing
N_ROWS = 1632271984                         # The number of rows in the .bz2 file, takes hours to calculate
N_REVISIONS = N_ROWS // ROWS_PER_REVISION   # The number of revisions, each revision is 14 rows long


def read_revisions(file_path: str, N: int = None, start: int = None, end: int = None, random: bool = False) -> pd.DataFrame:
    """
    Read and parse N lines of a (large) bzip2 file on the format given in Wikipedia Edits dataset 
    seen in: https://snap.stanford.edu/data/wiki-meta.html
    
    Parameters
    ----------
    file_path : str
        Path to the .bz2 compressed Wikipedia revisions file.
    N : int, optional
        Number of rows to read. Ignored is `start`and `end`are specified
    start : int, optional
        The starting index from which to read revisions has to be specified with `end`
    end : int, optional
        The ending index up to which to read revisions. Ignored if
        `start` is not provided.
    random : bool, default False
        Will read `N` random entries from the file if true.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the revision data read from the file. Each row in the
        DataFrame corresponds to a single revision entry, with the following columns:
        
        - "article_id" (int): id of the article.
        - "revision_id" (int): id of the revision.
        - "user_id" (str): id of the user, stripped of ip: prefix.
        - "article_title" (str): Title
        - "timestamp" (datetime): Timestamp
        - "username" (str): username, stripped of ip: prefix.
        - "category" (set of str): A set containing the categories of the article.
        - "main_linked" (set of str): A set containing the main links of the article.
        - "other_linked" (set of str): A set containing other links associated with the article
        - "comment" (str): The comment made by the user during the revision.
        - "minor" (bool): Boolean indicating whether the revision was minor.
        - "num_words" (int): The number of words in the text of the revision.

    Examples
    --------
    >>> read_revisions('/path/to/dump.bz2', N=10) # Returns a DataFrame with the first 10 revision entries.

    >>> read_revisions('/path/to/dump.bz2', start=100, end=200) # Returns a DataFrame with revisions 100 to 200.

    >>> read_revisions('/path/to/dump.bz2', N=5, random=True) # Returns a DataFrame with 5 random revision entries.

    Notes
    -----
    For `random` access and access between `start` and `end` a index file has already
    been created and will be used to significantly speed up look up.
    """
    if random and N:
        return _read_revisions_random(file_path, N)
    elif start and end:
        return _read_revisions_between(file_path, start, end)
    elif N:
        return _read_revisions_from_start(file_path, N)
    else:
        raise Exception("Error: pass at least N or start+end")
    

def _read_revisions_from_start(file_path: str, N: int = None) -> pd.DataFrame:
    """ """
    with bz2.open(file_path, 'rt') as file:
        revisions = []
    
        # There are EXACTLY 14 fields in every revision, we group / bundle them together in a tuple for speed
        for i, line in enumerate(groups(file, 14)):
            if N <= i:
                break

            revisions.append(parse_line(line))
        
        return pd.DataFrame(revisions)
    

def _read_revisions_between(file_path: str, start: int = None, end: int = None) -> pd.DataFrame:
    """ """
    with bz2.open(file_path, 'rt') as file:
        revisions = []

        # Get the position of the index 
        index = read_index_file(f"/work3/s204163/wiki/index_file{REVISIONS_PER_INDEX}") # TODO: Move elsewhere
        index_number, index_byte_position = byte_position_of_closest_index(index, start)

        # Go to the location of the closest index number
        file.seek(index_byte_position)

        # There are EXACTLY 14 fields in every revision, we group / bundle them together in a tuple for speed
        for i, line in enumerate(groups(file, 14), start = index_number):
            if i < start:
                continue
            if end <= i:
                break

            revisions.append(parse_line(line))
        
        return pd.DataFrame(revisions)


# OBS OBS OBS TODO: Takes 90 seconds to grab 10 random revisions, should be revised to be faster
def _read_revisions_random(file_path: str, N: int = None) -> pd.DataFrame:
    """ """
    index = read_index_file(f"/work3/s204163/wiki/index_file{REVISIONS_PER_INDEX}") # TODO: Move elsewhere
    n_indices = len(index)
    revisions = []

    with bz2.open(file_path, 'rt') as file:
        for _ in range(N):
            random_index = randint(0, n_indices - 1)
            random_offset = randint(0, REVISIONS_PER_INDEX)

            # Get the position of the index and go to the byte location in the file
            _, index_byte_position = byte_position_of_closest_index(index, random_index)
            file.seek(index_byte_position)

            # There are EXACTLY 14 fields in every revision, we group / bundle them together in a tuple for speed
            for i, line in enumerate(groups(file, 14)):

                # If we found the revision, save and move on
                if i == random_offset:
                    revisions.append(parse_line(line))
                    break
        
        return pd.DataFrame(revisions)


def parse_line(line: tuple) -> dict:
    """ Parse a single line (a tuple) into a dictionary"""
    # Split the line and revision-field for at least a bit of readability
    revision, category, _image, main, _talk, _user, _user_talk, other, _external, _template, comment, minor, textdata, _ = line
    revision_tag, article_id, revision_id, article_title, timestamp, username, user_id = revision.split(" ")
    
    assert revision_tag == "REVISION" # Sanity check

    # This code looks kinda horrendous, but does what it should in a concise and fast way. dont hate
    return {
        "article_id"    : int(article_id),
        "revision_id"   : int(revision_id),
        "user_id"       : user_id.split(":")[-1],
        "article_title" : article_title,
        "timestamp"     : datetime.fromisoformat(timestamp.rstrip("Z")),
        "username"      : username.split(":")[-1],
        "category"      : set(strip_prefix(category, PREFIXES).split()),
        "main_linked"   : set(strip_prefix(main, PREFIXES).split()),
        "other_linked"  : set(strip_prefix(other, PREFIXES).split()),
        "comment"       : strip_prefix(comment, PREFIXES),
        "minor"         : bool(int(strip_prefix(minor, PREFIXES))),
        "num_words"     : int(strip_prefix(textdata, PREFIXES)),
    }


# Cheeky function shamelessly stolen from: https://stackoverflow.com/a/312644
def groups(iterable, n, padvalue=None):
    """grouper('abcdefg', 3, 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"""
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def strip_prefix(text, prefixes):
    """
    Remove the prefix of a line, but also clean the string slightly. i.e.
    strip_prefix('CATEGORY American_mathematicians\\n', PREFIXES) --> 'American_mathematicians'
    """
    for prefix in prefixes:
        if text.startswith(prefix):
            return text.removeprefix(prefix).removeprefix(" ").removesuffix("\n")
    return text


# https://stackoverflow.com/a/51980706
def round_down(x, k=3):
    """
    Round down to nearest 1000. We want to get the closest PRIOR index location, this is useful for that
    e.g. round_down(1900) --> 1000
    """
    n = 10**k
    return x // n * n


def byte_position_of_closest_index(index: dict, current_position: int) -> int:
    """
    Get the byte position of the closest prior index position. i.e. if we are in row 1200 our closest index is in
    row 1000. We want to get the index number and its byte position in the file.
    """
    index_number = round_down(current_position)
    index_byte_position = index[index_number]

    return (index_number, index_byte_position)


def read_index_file(file_path: str) -> dict:
    """ Read the index file for the revisions """
    index = {}
    with open(file_path, 'r') as file:
        for line in file:
            row_number, byte_position = map(int, line.strip().split(', '))
            index[row_number] = byte_position
    return index


def read_articles_file(file_path: str) -> dict:
    """ Read the index file for the revisions """
    articles = {}
    
    # TODO: Implement

    return articles
