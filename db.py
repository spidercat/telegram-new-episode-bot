from tinydb import TinyDB, Query, where

class Db:
    
    def __init__(self):
        self.groups = TinyDB('tinydb/groups-db.json')
        self.actions = TinyDB('tinydb/actions-db.json')

    def is_family(self, id):
        family = self.groups.search(where('name') == 'Family')
        assert len(family) == 1, f"Expected 1 Family object. Found {len(family)}."
        return str(id) in family[0]['members']

    def is_kid(self, id):
        qourum = self.groups.search(where('name') == 'Kids Quorum')
        assert len(qourum) == 1, f"Expected 1 Kids Quorum object. Found {len(qourum)}."
        return str(id) in qourum[0]['members']

    def get_quorum(self, ids=[]):
        qourum = self.groups.search(where('name') == 'Kids Quorum')
        assert len(qourum) == 1, f"Expected 1 Kids Quorum object. Found {len(qourum)}."
        return [ident for ident in qourum[0]['members'] if ident not in [str(i) for i in ids]]

    def get_name(self, id):
        user = self.groups.search(where('chat_id') == str(id))
        assert len(user) == 1, f"No one with chat_id={id} is found."
        return user[0]['name']

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
