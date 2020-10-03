class forgetHeuristics:

    def has_next(self):
        raise "not implemented"

    def choose_next(self):
        raise "not implemented"


class forgetFromList(forgetHeuristics):

    def __init__(self, signature_list):
        self.signature_list = signature_list

    def has_next(self):
        if not self.signature_list:
            return False
        else:
            return True

    def choose_next(self):
        return self.signature_list.pop()