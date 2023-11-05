import bz2

from create_index import groups, parse_line

def keep_revision(revision: dict) -> bool:
    # TODO: Implment logic to determine whether a row should be kept
    # - no neighbours ?
    # - no category ?
    # - few words ? 
    return True

def delete_revisions(input_file_path: str, output_file_path: str) -> None:
    with bz2.open(input_file_path, 'rt') as input_file, bz2.open(output_file_path, 'wt') as output_file:
        
        for i, line in enumerate(groups(input_file, 14)):
            if keep_revision(parse_line(line)):
                output_file.write("".join(line))

            # TODO: temporary as to not run on entire dataset
            if 100 < i:
                break


if __name__ == "__main__":
    input_file_path  = '/work3/s204163/wiki/wiki-revisions-dataset.bz2'
    output_file_path = '/work3/s204163/wiki/wiki-revisions-filtered.bz2'

    delete_revisions(input_file_path, output_file_path)

