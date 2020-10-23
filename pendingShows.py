import collections
import config
import os
from os.path import isfile, split, splitext
import re

def __canonize(series_name):
	return series_name.replace('.', ' ').strip()

def get_shows():
	stream = os.popen(f"find {config.PENDING_EPISODES_DIR}")
	found = [path.strip() for path in stream.readlines()]
	media_files = [filepath for filepath in found if isfile(filepath) and filepath.endswith(('.mp4', '.mkv'))]
	# print(len(media_files))

#	file_names = [split(filepath)[1] for filepath in media_files]

	Episode = collections.namedtuple('Episode', 'show number filepath')

	episodes =[]
	for filepath in media_files:
		filename = splitext(split(filepath)[1])[0]
		series_name = re.sub('S\d\d(E\d\d)+', '', filename)
		episode = filename[len(series_name):].strip()
		episodes.append(Episode(__canonize(series_name), episode, filepath))
		#print(f'{__canonize(series_name)} {episode}')

		#print({e.show for e in episodes})

	return {e.show for e in episodes}
