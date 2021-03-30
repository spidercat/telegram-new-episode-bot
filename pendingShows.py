import collections
import config
import secrets
import os
from os.path import isdir, isfile, join, split, splitext
import re
import shutil

def __canonize(series_name):
    series_name = series_name.replace('.', ' ').strip()
    if series_name.endswith('-'):
        series_name = series_name[:-1]

    return series_name.strip()

Episode = collections.namedtuple('Episode', 'show number filepath')

def __get_episodes_dir(bucket_name):
    bucket = config.storage.get(bucket_name)
    if bucket:
        return join(secrets.PENDING_EPISODES_BASEDIR, bucket['EPISODES_DIR'])

def __get_target_dir(bucket_name):
    bucket = config.storage.get(bucket_name)
    if bucket:
        return join(secrets.TARGET_BASEDIR, bucket['TARGET_DIR'])

def __get_available_episodes(bucket_name):
    episodes_dir = __get_episodes_dir(bucket_name)
    if not episodes_dir:
        return []

    stream = os.popen(f"find {episodes_dir}")
    found = [path.strip() for path in stream.readlines()]
    media_files = [filepath for filepath in found if isfile(filepath) and filepath.endswith(('.mp4', '.mkv'))]

    episodes =[]
    numbering_pattern = re.compile('[sS]\d\d[eE]\d+')
    for filepath in media_files:
        filename = splitext(split(filepath)[1])[0]
        series_name = numbering_pattern.split(filename)[0]
        episode = numbering_pattern.search(filename)[0].upper()
        episodes.append(Episode(__canonize(series_name), episode, filepath))

    return episodes

def __get_next_episode(show: str, bucket_name) -> Episode:
    show_episodes = list(filter(lambda s: s.show == show, __get_available_episodes(bucket_name)))
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

def get_shows(bucket_name = 'Common'):
    return {e.show for e in __get_available_episodes(bucket_name)}

def get_next_episode_number(show, bucket_name = 'Common'):
    episode = __get_next_episode(show, bucket_name)
    return __get_verbose_number(episode.number)

def prepare_next_episode(show: str, bucket_name = 'Common') -> str:
    episode = __get_next_episode(show, bucket_name)
    if not episode:
        return f"No episodes of '{show}' were found."

    episode_folder = __get_folder(episode)
    target_dir = join(__get_target_dir(bucket_name), episode_folder)
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
