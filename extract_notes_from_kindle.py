"""Usage: extract_notes_from_kindle.py <kindle_notes_file> <output_dir>

TODO: add more explanation, "split file into different files by book"

Options:
    kindle_notes_file        The My_Clippings.txt from kindle file system
    output_dir               Where to save the notes from the books
"""
import os
import string
from itertools import groupby
import docopt
from kindle_notes import KindleNotesIterator


def get_clean_file_name(name):
    clean_name = "".join("_" if char not in string.ascii_letters else char for char in name)
    return clean_name + "_notes.txt"


def save_notes_to_file(title, notes, output_dir):
    title_file_path = os.path.join(output_dir, get_clean_file_name(title))

    with open(title_file_path, "w+", encoding="utf-8") as title_file_handler:
        title_file_handler.write(title + "\n\n")

        for note in notes:
            title_file_handler.write(str(note))


def extract_notes(notes_file_path, output_dir):
    titles = []
    kindle_notes_iterator = KindleNotesIterator(notes_file_path)
    for title, notes in groupby(kindle_notes_iterator, lambda x: x.title):
        save_notes_to_file(title, notes, output_dir)
        titles.append(title)

    print("Finished. Saved {} files to {}".format(len(titles), output_dir))


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    extract_notes(args["<kindle_notes_file>"], args["<output_dir>"])
