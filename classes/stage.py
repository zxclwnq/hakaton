
rules = [(False,["admin"],False),(True,["admin",'moderation'],False),
         (False,["admin",'experts'],True),(False,["admin"],True)]
class Stage():
    def __init__(self):
        self.stage = 1
        self.rules = rules[self.stage-1]
        self.can_make_proposes = rules[0]
        self.allowed_roles = rules[1]
        self.show_result_table = rules[2]
    def inc_stage(self):
        self.stage+=1
        self.rules = rules[self.stage-1]
        self.can_make_proposes = rules[0]
        self.allowed_roles = rules[1]
        self.show_result_table = rules[2]

