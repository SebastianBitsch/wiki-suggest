import bz2

ROWS_PER_REVISION = 14                                          # The number of rows in a single revision object, should never change
REVISIONS_PER_INDEX = 50                                        # How many revisions should there be between indexing
INDEX_ROWS_SPACING = ROWS_PER_REVISION * REVISIONS_PER_INDEX    # How many rows of the .bz2 file should pass between indexing

def create_index_file(file_path: str) -> dict:
    """
    Create an index file that allow for faster look up in the gzip2 file by logging the
    byte location at every N rows.
    An index file is just the byte location of every N row in the file
    Is a one time operation that allows to faster look revisions and grab random ones, so it is worth the upfront cost
    Takes around ~3 hours to run on a single cpu on hpc.
    """

    index = {}

    # Crete the index
    with bz2.open(file_path, 'rb') as file:
        byte_position = file.tell()
        for i, _ in enumerate(file):
            if i % INDEX_ROWS_SPACING == 0:        
                # Add the true row number, revision number, and byte position to the index
                index[i // ROWS_PER_REVISION] = byte_position
                # print(f"Read {i}/1632271984 lines")

            byte_position = file.tell() # Get the position of the row in bytes PRIOR to reading it        

    return index

if __name__ == "__main__":
    file_path = '/work3/s204163/wiki/wiki-revisions-dataset.bz2'
    index = create_index_file(file_path)

    # Save the index
    with open('index_file50', 'w') as f:
        for line_num, byte_pos in index.items():
            f.write(f"{line_num}, {byte_pos}\n")
