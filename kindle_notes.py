import string

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


class KindleNotesGenerator:
    KINDLE_END_NOTE = "=========="

    def __init__(self, notes_file_path):
        self._handler = open(notes_file_path, "rb")

    def __iter__(self):
        return self

    def _read_clean_line(self):
        return self._handler.readline().decode("utf-8").strip()

    def _read_note_data(self):
        raw_data = []
        line = self._read_clean_line()
        while line != KindleNotesGenerator.KINDLE_END_NOTE:
            raw_data.append(line)
            line = self._read_clean_line()
        return raw_data

    def __next__(self):
        """
        each note is formatted as follows:
        Title
        Timestamps

        Note data
        Note data
        ...
        Note data
        ==========
        """
        try:
            title = self._read_clean_line()

            if not title:
                raise ValueError
        except ValueError:
            self._handler.close()
            raise StopIteration

        raw_timestamps = self._read_clean_line()

        # comment line - useless for parsing
        self._read_clean_line()
        raw_data = self._read_note_data()

        return KindleNote(title, raw_timestamps, raw_data)

