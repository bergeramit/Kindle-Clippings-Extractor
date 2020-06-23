"""
Kindle Notes are saved in a specific format.
Kindle Note Entry Structure:

line 1:     Book Title (Author)
line 2:     Page | location | datetime => timestamps
line 3:
line 4:     note data - the actual highlight
line 5:     ...
line n-1:   note data - the actual highlight
line n:     ==========

line n+1:   Next Book Title (Author)
and so on...

"""
import string

class KindleNote:
    SEPARATOR = "\n=================================\n\n\n"
    MINIMUM_CHARACTERS_FOR_NOTE = 2

    @staticmethod
    def remove_kindles_prefix(title):
        """This is because kindle has decided to add random prefixes
            to the titles
        """
        clean_title = title.replace(title[0], "") if title[0] not in string.ascii_letters else title
        return clean_title

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

    def _is_empty(self):
        return len(self._data) <= KindleNote.MINIMUM_CHARACTERS_FOR_NOTE

    def __str__(self):
        if self._is_empty():
            return ""

        return "\n".join([self._data, self._timestamps, KindleNote.SEPARATOR])


class KindleNotesIterator:
    KINDLE_END_NOTE = "=========="

    def __init__(self, notes_file_path):
        self._handler = open(notes_file_path, "rb")

    def __iter__(self):
        return self

    def _readline(self):
        return self._handler.readline().decode("utf-8").strip()

    def _read_note_data(self):
        raw_data = []
        line = self._readline()
        while line != KindleNotesIterator.KINDLE_END_NOTE:
            raw_data.append(line)
            line = self._readline()
        return raw_data

    def __next__(self):
        """
        Reads a note block every time called.
        The notes are formed according to the format
        in the __doc__ of this module.
        """
        try:
            title = self._readline()

            if not title:
                self._handler.close()
                raise StopIteration

        except ValueError:
            self._handler.close()
            raise StopIteration

        raw_timestamps = self._readline()

        # blank line - useless for parsing
        self._readline()
        raw_data = self._read_note_data()

        return KindleNote(title, raw_timestamps, raw_data)
