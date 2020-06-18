"""Usage: extract_notes_from_kindle.py <kindle_clipping_file> <output_dir>

Options:
    kindle_clipping_file     The My_Clippings.txt from kindle file system
    output_dir               Where to save the notes from the books
"""
import os
import itertools
import string
import docopt


class KindleClippingsGenerator:
    KINDLE_END_NOTE = "=========="

    def __init__(self, clippings_file_path):
        self.handler = open(clippings_file_path, "rb")

    def __iter__(self):
        return self

    def _extract_clip_data(self):
        note_data = ""
        note_data_line = self.handler.readline().decode("utf-8").strip()
        while note_data_line != KindleClippingsGenerator.KINDLE_END_NOTE:
            note_data = "\n".join([note_data, note_data_line])
            note_data_line = self.handler.readline().decode("utf-8").strip()
        return note_data

    def __next__(self):
        try:
            title = self.handler.readline().decode("utf-8").strip()
        except ValueError:
            self.handler.close()
            raise StopIteration

        meta_data = self.handler.readline().decode("utf-8").strip()

        # comment line - useless for parsing
        self.handler.readline()
        note_data = self._extract_clip_data()
        return title, meta_data, note_data


def format_clip(clip):
    return "\n".join(clip[1:])

def format_title(title_name):
    for char in title_name:
        if char not in string.ascii_letters:
            title_name = title_name.replace(char, "_")
    return title_name

def is_empty_note(note):
    return len(note[2]) <= 1

def extract_notes(clippings_file_path, output_notes_dir):
    for title_name, title_clips in itertools.groupby(KindleClippingsGenerator(clippings_file_path), lambda x: x[0]):
        title_notes_file_name = "".join([format_title(title_name), "_notes.txt"])

        title_file_path = os.path.join(output_notes_dir, title_notes_file_name)
        with open(title_file_path, "w+", encoding="utf-8") as title_file_handler:
            title_file_handler.write("{} - Notes".format(title_name))
            for clip in title_clips:
                if not is_empty_note(clip):
                    title_file_handler.write(format_clip(clip))
                    title_file_handler.write("\n\n{}\n\n".format("-" * 100))


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    extract_notes(args["<kindle_clipping_file>"], args["<output_dir>"])
