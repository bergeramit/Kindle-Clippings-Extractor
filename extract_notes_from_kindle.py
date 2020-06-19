"""Usage: extract_notes_from_kindle.py <kindle_notes_file> <output_dir>

Options:
    kindle_notes_file     The My_Clippings.txt from kindle file system
    output_dir               Where to save the notes from the books
"""
import os
import string
from itertools import groupby
import docopt


class KindleNote:
    SEPARATOR = "\n=================================\n\n\n"
    MINIMUM_CHARACTERS_FOR_NOTE = 2

    @staticmethod
    def remove_kindles_prefix(title):
        if title[0] not in string.ascii_letters:
            title = title.replace(title[0], "")
        return title

    def __init__(self, title, raw_timestamp, raw_data):
        self._title = self.remove_kindles_prefix(title)
        self._timestamps = raw_timestamp
        self._data = "\n".join(raw_data)

    @property
    def title(self):
        return self._title

    @property
    def timestamps(self):
        return self._timestamps

    @property
    def data(self):
        return self._data

    def is_empty(self):
        return len(self._data) <= KindleNote.MINIMUM_CHARACTERS_FOR_NOTE

    def __str__(self):
        if self.is_empty():
            return ""

        return "\n".join([self._data, self._timestamps, KindleNote.SEPARATOR])


class KindleNoteGenerator:
    KINDLE_END_NOTE = "=========="

    def __init__(self, notes_file_path):
        self._handler = open(notes_file_path, "rb")

    def __iter__(self):
        return self

    def read_note(self):
        """
        each note is formatted as follows:
        Title
        Timestamps

        Note data
        ...
        Note data
        ==========
        """
        title = self._handler.readline().decode("utf-8").strip()
        if not title:
            raise ValueError

        raw_timestamps = self._handler.readline().decode("utf-8").strip()

        # comment line - useless for parsing
        self._handler.readline().decode("utf-8").strip()

        raw_data = []
        line = self._handler.readline().decode("utf-8").strip()
        while line != KindleNoteGenerator.KINDLE_END_NOTE:
            raw_data.append(line)
            line = self._handler.readline().decode("utf-8").strip()

        return KindleNote(title, raw_timestamps, raw_data)

    def __next__(self):
        try:
            note = self.read_note()
        except ValueError:
            self._handler.close()
            raise StopIteration

        return note


def get_file_name(name):
    for char in name:
        if char not in string.ascii_letters:
            name = name.replace(char, "_")
    return name + "_notes.txt"


def save_notes_to_file(title, notes, output_dir):
    title_file_path = os.path.join(output_dir, get_file_name(title))

    with open(title_file_path, "w+", encoding="utf-8") as title_file_handler:
        title_file_handler.write(title + "\n\n")

        for note in notes:
            title_file_handler.write(str(note))


def extract_notes(notes_file_path, output_dir):
    for title, notes in groupby(KindleNoteGenerator(notes_file_path), lambda x: x.title):
        save_notes_to_file(title, notes, output_dir)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    extract_notes(args["<kindle_notes_file>"], args["<output_dir>"])
