"""Usage: extract_notes_from_kindle.py <kindle_notes_file> <output_dir>

Options:
    kindle_notes_file     The My_Clippings.txt from kindle file system
    output_dir               Where to save the notes from the books
"""
import os
import string
from itertools import groupby
import docopt
from kindle_notes import KindleNotesGenerator


def get_clean_file_name(name):
    for char in name:
        if char not in string.ascii_letters:
            name = name.replace(char, "_")
    return name + "_notes.txt"


def save_notes_to_file(title, notes, output_dir):
    title_file_path = os.path.join(output_dir, get_clean_file_name(title))

    with open(title_file_path, "w+", encoding="utf-8") as title_file_handler:
        title_file_handler.write(title + "\n\n")

        for note in notes:
            title_file_handler.write(str(note))


def extract_notes(notes_file_path, output_dir):
    kindle_notes_iterator = KindleNotesGenerator(notes_file_path)
    for title, notes in groupby(kindle_notes_iterator, lambda x: x.title):
        save_notes_to_file(title, notes, output_dir)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    extract_notes(args["<kindle_notes_file>"], args["<output_dir>"])
