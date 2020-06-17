"""Usage: extract_notes_from_kindle.py <kindle_clipping_file> <output_dir>

Options:
	kindle_clipping_file     The My_Clippings.txt from kindle file system
"""
import docopt
import os
import itertools
from collections import namedtuple

class KindleClip:
	def __init__(self, book_name, book_location, date_added, note_data):
		self.book_name = book_name
		self.book_location = book_location
		self.date_added = date_added
		self.note_data = note_data


class KindleClippingsGenerator:
	KINDLE_END_NOTE = "=========="

	def __init__(self, clippings_file_path):
		self.clippings_file_handler = open(clippings_file_path, "r")

	def __iter__(self):
		return self

	def __next__(self):
		book_name = self.clippings_file_handler.readline().strip()

		if not book_name:
			self.clippings_file_handler.close()
			raise StopIteration

		meta_data = self.clippings_file_handler.readline().strip().split("|")

		# blank line
		self.clippings_file_handler.readline().strip()
		
		note_data = ""
		note_data_line = self.clippings_file_handler.readline().strip()
		while note_data_line != KindleClippingsGenerator.KINDLE_END_NOTE:
			note_data = "\n".join([note_data, note_data_line])
			note_data_line = self.clippings_file_handler.readline().strip()

		if len(meta_data) == 1:
			date_added = meta_data
			return (book_name, date_added, note_data)
		elif len(meta_data) == 2:
			book_location, date_added = meta_data
			return (book_name, book_location, date_added, note_data)
		elif len(meta_data) == 3:
			book_page, book_location, date_added = meta_data
			return (book_name, book_page, book_location, date_added, note_data)


def format_clip(clip):
	try:
		return "\n".join(clip)
	except TypeError:
		import ipdb; ipdb.set_trace()


def extract_notes(clippings_file_path, output_notes_dir):
	for book_name, book_clips in itertools.groupby(KindleClippingsGenerator(clippings_file_path), lambda x: x[0]):
		book_notes_file_name = "".join([book_name.replace(" ", "_"), "_notes.txt"])

		with open(os.path.join(output_notes_dir, book_notes_file_name), "w+") as current_book_notes:
			for clip in book_clips:
				current_book_notes.write(format_clip(clip))
				current_book_notes.write("\n-----------------\n")

if __name__ == '__main__':
	args = docopt.docopt(__doc__)
	extract_notes(args["<kindle_clipping_file>"], args["<output_dir>"])
