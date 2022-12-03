
rules = [(False,["admin"],0),(True,["admin",'moderation'],0),
         (False,["admin",'experts'],1),(False,["admin"],2)]
class Stage():
    def __init__(self):
        self.stage = 1
        self.rules = rules[self.stage-1]
        self.can_make_proposes = self.rules[0]
        self.allowed_roles = self.rules[1]
        self.result_table_state = self.rules[2]
    def set_stage(self,id):
        self.stage = id
        self.rules = rules[self.stage-1]
        self.can_make_proposes = self.rules[0]
        self.allowed_roles = self.rules[1]
        self.result_table_state = self.rules[2]

