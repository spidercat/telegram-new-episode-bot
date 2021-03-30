from tinydb import TinyDB, Query, where
import config
import people

class Db:
    def __init__(self):
        self.groups = TinyDB('tinydb/groups-db.json')
        self.actions = TinyDB('tinydb/actions-db.json')

    def __is_member(self, group, id):
        group = self.groups.search(where('name') == group)
        assert len(group) == 1, f"Expected 1 '{group}' object. Found {len(group)}."
        return str(id) in group[0]['members']

    def is_family(self, id):
        name = people.CHAT_ID_TO_NAME.get(id)
        return name and name in config.Family

    def is_guest(self, id):
        name = people.CHAT_ID_TO_NAME.get(id)
        return name and name in config.Guests

    def is_kid(self, id):
        name = people.CHAT_ID_TO_NAME.get(id)
        return name and name in config.Kids

    def get_quorum(self, ids=[]):
        """ returns chat ids of qourum members """
        return [self.get_id(name) for name in config.Kids if self.get_id(name) not in ids]

    def get_name(self, id):
        name = people.CHAT_ID_TO_NAME.get(id)
        assert name, f"No one with chat_id={id} is found."
        return name

    def get_id(self, name):
        for key, value in people.CHAT_ID_TO_NAME.items():
         if name == value:
             return key

    def whoami(self, id):
        name = self.get_name(id)
        if name:
            return config.Whoami.get(name, None) or f"{name}, you're just a child."
        else:
            return f"{id}, I don't know you."

    def __get_pending_episode(self):
        pending = self.actions.search(where('name') == 'Pending Episode')
        if len(pending) != 1:
            return None
        return str(id) in pending[0]

    @property
    def pending_episode(self):
        self.__get_pending_episode()

    @pending_episode.setter
    def pending_episode(self, show, requester_id):
        assert not self.__get_pending_episode(), "can't set pending episode until the previous one is resolved."
        self.actions.insert({'name': 'Pending Episode', 'chat_id': str(requester_id)})
