import xml.etree.ElementTree as ET

class ForgetHeuristics:
    def __init__(self, ontology_path):
        # the ontology path from which the signatures should be choosen (string)
        self.ontology_path = ontology_path
        self.set_ontology(ontology_path)

    def set_ontology(self, ontology_path):
        self.ontology_path = ontology_path
        with open(ontology_path) as onto:
            self.ontology = onto.read()

    def choose_next(self):
        """
        Must return the filename in which the next signature is stored and the signature.
        """
        raise NotImplementedError()

    def has_next(self):
        raise NotImplementedError()

    def get_available_signatures(self):
        """
        Scans the ontology for available signatures and returns them
        :return: list of signatures
        """
        # set namespaces and load ontology as XML
        rds_ns = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
        owl_ns = "{http://www.w3.org/2002/07/owl#}"
        onto = ET.parse(self.ontology_path)
        root = onto.getroot()
        signatures = []

        for cla in root.findall(owl_ns+'Class') + root.findall('Class'):
            # if not an anonymous class
            try:
                signatures.append(cla.attrib[rds_ns+'about'])
            except KeyError:
                pass
        return signatures


class ForgetFromList(ForgetHeuristics):
    def __init__(self, ontology_path, signature_list):
        super().__init__(ontology_path)
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


class AndiHeuristic(ForgetHeuristics):
    def __init__(self, ontology_path, subsumption):
        """
        constructor
        :param ontology_path: path to the ontology file
        :param subsumption: the subsumption which we want to proof. tuple(A, B) where we want to show A <= B
        """
        super().__init__(ontology_path)
        self.subsumption = subsumption

    def set_subsumption(self, subsumption):
        self.subsumption = subsumption

    def has_next(self):
        # delete signatures we want to derive from the signature list
        signatures = self.get_available_signatures()
        for sub in self.subsumption:
            if signatures.count(sub) >= 1:
                signatures.remove(sub)

        if len(signatures) == 0:
            return False
        else:
            return True

    def choose_next(self):
        """
        The idea here is that it is quite easy to understand simple subsumption chains.
        e.g.: inferring from A < B, B < C, C < D that A < D. Therefore such inferences should be choosen first
        and also executed all at the same time.

        :return: the signatures to forget and the file in which they are stored
        """
        signatures = []

        # set namespaces and load ontology as XML
        rds_ns = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
        owl_ns = "{http://www.w3.org/2002/07/owl#}"
        rdfs_ns = "{http://www.w3.org/2000/01/rdf-schema#}"
        onto = ET.parse(self.ontology_path)
        root = onto.getroot()

        #get the node with the class we are looking at. The left signature of the subsumption.
        subsumes = None
        for child in root:
            if child.tag == owl_ns+'Class' and child.attrib[rds_ns+'about'] == self.subsumption[0]:
                subsumes = child
                break

        #get its subsumption chain
        next_subsumption = subsumes
        while(True):
            # Find the first node of which our subsumption is a subclass of
            child = next_subsumption.find(rdfs_ns+'subClassOf')
            if child != None:
                # save the signature
                signatures.append(child.attrib[rds_ns+'resource'])
                # find the element in which that child class is defined to find further subsumptions
                for cla in root.findall(owl_ns+'Class'):
                    if cla.attrib[rds_ns+'about'] == child.attrib[rds_ns+'resource']:
                        next_subsumption = cla
                        break
            else:
                break

        if len(signatures) == 0 and self.has_next():
            # If no child was found, save the first sigature of the list of still available signatues
            signatures.append(self.get_available_signatures().pop())


        # delete signatures we want to derive from the signature list
        for sub in self.subsumption:
            if signatures.count(sub) >= 1:
                signatures.remove(sub)

        # save signatures
        with open('datasets\signature.txt', 'w+') as file:
            for s in signatures:
                file.write(s + '\n')

        return (signatures, 'datasets\signature.txt')


class StandardHeuristics(AndiHeuristic):
    def __init__(self, ontology_path, subsumption):
        super(StandardHeuristics, self).__init__(ontology_path, subsumption)

    def choose_next(self):
        # delete signatures we want to derive from the signature list
        signatures = self.get_available_signatures()
        for sub in self.subsumption:
            if signatures.count(sub) >= 1:
                signatures.remove(sub)

        # return the first list element if the list is not empty
        if len(signatures) == 0:
            return None
        else:
            # save signatures
            with open('datasets\signature.txt', 'w+') as file:
                 file.write(signatures[0] + '\n')

            return (signatures[0], 'datasets\signature.txt')

