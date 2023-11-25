from context import Context

class InteractionAuthor:
    def __init__(self,data):
        self.name = data['name']
        self.id = data['id']
        self.display_name = data['display_name'] if data['display_name'] else None


class Interaction:
    def __init__(self,
                 _cmd_json:dict):
        self._json = _cmd_json
        self._token = _cmd_json['token']
        self.options = _cmd_json['options']
        self.interaction_id = _cmd_json['id']
        self.deffered = False
        self.author:InteractionAuthor = _cmd_json['author']
