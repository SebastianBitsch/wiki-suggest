"""
Create an index file of the .bz2 file that logs the byte location of every N rows
Takes around 3 hours to run on a single cpu on hpc. 
Is a one time operation that allows to faster look revisions and grab random ones, so it is worth the upfront cost
"""
import bz2

ROWS_PER_REVISION = 14      # Should never change
INDEX_RESOLUTION = 1000     # How many rows should there be between indices
INDEX_ROWS_SPACING = ROWS_PER_REVISION * INDEX_RESOLUTION

file_path = '/work3/s204163/enwiki-20080103.main.bz2'

index = {}

# Crete the index
with bz2.open(file_path, 'rb') as file:
    byte_position = file.tell()
    for i, line in enumerate(file):
        if i % INDEX_ROWS_SPACING == 0:        
            # Add the true row number, revision number, and byte position to the index
            index[i // ROWS_PER_REVISION] = byte_position
            print(f"Read {i}/~3500M lines")

        byte_position = file.tell() # Get the position of the row in bytes PRIOR to reading it        

# Save the index
with open('index_file', 'w') as f:
    for line_num, byte_pos in index.items():
        f.write(f"{line_num}, {byte_pos}\n")