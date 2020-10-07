import re

class forgetHeuristics:

    def __init__(self, ontology):
        # the ontology from which the signatures should be choosen (string)
        self.ontology = ontology

    def choose_next(self):
        """
        Must return the filename in which the next signature is stored and the signature.
        """
        raise "not implemented"

    def has_next(self):
        raise "not implemented"

    def get_available_signatures(self):
        """
        Scans the ontology for available signatures and returns them
        :return: list of signatures
        """
        # get the owl namespace
        ns_regex =r"xmlns=\S* "
        ns = re.findall(ns_regex, self.ontology)[0][7:-2]
        regex = ns + r"[\Sa-zA-Z0-1]{2,}\""
        signatures = set(re.findall(regex, self.ontology))
        signatures = [signature[:-1] for signature in signatures]
        return signatures



class forgetFromList(forgetHeuristics):
    def __init__(self, ontology, signature_list):
        super().__init__(ontology)
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