class forgetHeuristics:

    def choose_next(self):
        """
        Must return the filename in which the next signature is stored and the signature.
        """
        raise "not implemented"

    def has_next(self):
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
        curr_sig = self.signature_list.pop()
        with open('datasets\signature.txt', 'w+') as f:
            f.write(curr_sig)
        return (curr_sig, 'datasets\signature.txt')