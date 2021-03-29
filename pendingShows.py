import collections
import config
import secrets
import os
from os.path import isdir, isfile, join, split, splitext
import re
import shutil

def __canonize(series_name):
    return series_name.replace('.', ' ').strip()

Episode = collections.namedtuple('Episode', 'show number filepath')

PENDING_EPISODES_DIR = join(
    secrets.PENDING_EPISODES_BASEDIR,
    config.storage['Common']["EPISODES_DIR"]
)

TARGET_DIR = join(
    secrets.TARGET_BASEDIR,
    config.storage['Common']["TARGET_DIR"]
)

def __get_available_episodes():
    stream = os.popen(f"find {PENDING_EPISODES_DIR}")
    found = [path.strip() for path in stream.readlines()]
    media_files = [filepath for filepath in found if isfile(filepath) and filepath.endswith(('.mp4', '.mkv'))]

    episodes =[]
    for filepath in media_files:
        filename = splitext(split(filepath)[1])[0]
        series_name = re.sub('S\d\d(E\d\d)+', '', filename)
        episode = filename[len(series_name):].strip()
        episodes.append(Episode(__canonize(series_name), episode, filepath))

    return episodes

def __get_next_episode(show: str) -> Episode:
    show_episodes = list(filter(lambda s: s.show == show, __get_available_episodes()))
    show_episodes.sort(key=lambda e: e.number)
    return next(iter(show_episodes), None)

def __get_verbose_number(episode_short_number):
    season = episode_short_number[0:3].replace('S', 'Season ').replace(' 0', ' ')
    # TODO: handle multiple episodes
    episode = episode_short_number[3:].replace('E', 'Episode ').replace(' 0', ' ')
    return (season, episode)

def __get_folder(episode: Episode) -> str:
    show_folder = config.SHOW_TO_FOLDER.get(episode.show, episode.show)
    season_folder = __get_verbose_number(episode.number)[0]
    return join(show_folder, season_folder)

def get_shows():
    return {e.show for e in __get_available_episodes()}

def get_next_episode_number(show):
    episode = __get_next_episode(show)
    return __get_verbose_number(episode.number)

def prepare_next_episode(show: str) -> str:
    episode = __get_next_episode(show)
    if not episode:
        return f"No episodes of '{show}' were found."

    episode_folder = __get_folder(episode)
    target_dir = join(TARGET_DIR, episode_folder)
    if isdir(target_dir):
        print(f'{episode_folder} exists at target path')
    else:
        os.makedirs(target_dir, exist_ok=True)
        print(f'Created {target_dir}')

    print(split(episode.filepath))
    shutil.move(episode.filepath, target_dir)

    filename = split(episode.filepath)[1]
    if not isfile(join(target_dir, filename)):
        return f"File {filename} doesn't exist in the target directory."

    return None
