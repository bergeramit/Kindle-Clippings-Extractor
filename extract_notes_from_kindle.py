"""Usage: extract_notes_from_kindle.py <kindle_notes_file> <output_dir>

Options:
    kindle_notes_file     The My_Clippings.txt from kindle file system
    output_dir               Where to save the notes from the books
"""
import os
import string
import docopt


class Note:
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
        return len(self._data) <= Note.MINIMUM_CHARACTERS_FOR_NOTE

    def __str__(self):
        if self.is_empty():
            return ""

        return "\n".join([self._data, self._timestamps, Note.SEPARATOR])


class Title:

    def __init__(self, name):
        self.name = name
        self._notes = set()

    @property
    def notes(self):
        return self._notes

    def get_file_name(self):
        for char in self.name:
            if char not in string.ascii_letters:
                self.name = self.name.replace(char, "_")
        return self.name + "_notes.txt"

    def add_note(self, note):
        self._notes.add(note)

    def __iter__(self):
        self.remove_duplications()
        return self

    def __next__(self):
        try:
            return self._notes.pop()
        except KeyError:
            raise StopIteration

    def remove_duplications(self):
        pass


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

        return Note(title, raw_timestamps, raw_data)

    def __next__(self):
        try:
            note = self.read_note()
        except ValueError:
            self._handler.close()
            raise StopIteration

        return note


def get_notes_per_title(notes_file_path):
    titles = {}
    for note in KindleNoteGenerator(notes_file_path):
        titles[note.title] = titles.get(note.title, Title(note.title))
        titles[note.title].add_note(note)
    return titles


def save_notes_to_files(titles, output_notes_dir):
    for title in titles.values():

        title_file_path = os.path.join(output_notes_dir, title.get_file_name())
        with open(title_file_path, "w+", encoding="utf-8") as title_file_handler:
            title_file_handler.write(title.name + "\n\n")
            for note in title:
                title_file_handler.write(str(note))


def extract_notes(notes_file_path, output_notes_dir):
    titles = get_notes_per_title(notes_file_path)
    save_notes_to_files(titles, output_notes_dir)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    extract_notes(args["<kindle_notes_file>"], args["<output_dir>"])
