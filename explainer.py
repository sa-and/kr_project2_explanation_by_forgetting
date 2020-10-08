import os
import glob
from shutil import copy


class Explainer:
    '''
    Class mainly to provide a wrapper for the functions provided in kr_functions.jar to make them
    accessable more easily.
    '''

    def __init__(self, ontology, forgetHeuristics):
        self.ontology = ontology
        self.working_ontology = ontology
        self.forgetHeuristics = forgetHeuristics

    def set_ontology(self, ontology):
        self.ontology = ontology

    def set_working_ontology(self, ontology):
        self.working_ontology = ontology

    def set_forget_heuristics(self, forgetHeuristics):
        self.forgetHeuristics = forgetHeuristics

    '''print all subClass statements (explicit and inferred) Ontology    '''
    def print_all_subclasses(self):
        os.system('java -jar kr_functions.jar ' + 'printAllSubClasses' + " " + self.working_ontology)

    ''' save all subClass statements (explicit and inferred) in the inputOntology to file datasets/subClasses.nt'''
    def save_all_subclasses(self):
        os.system('java -jar kr_functions.jar ' + 'saveAllSubClasses' + " " + self.working_ontology)

    '''print all explanations for the subclass satements defined in a 'subclassStatements' file'''
    def print_all_explanations(self, subclass_statements_path):
        os.system('java -jar kr_functions.jar ' + 'printAllExplanations' + " " + self.working_ontology + " " + subclass_statements_path)

    '''save all explanations for the subclass satements defined in a 'subclassStatements' file to file datasets/exp-#.owl
    Caution: this clears all the previously saved explanations. Takes the intermediate step of first saving them all
    and them loading them again.'''
    def save_all_explanations(self, subclass_statements_path):
        # clear already present explanations
        all_paths = glob.glob("datasets/exp-*.owl")

        for file in all_paths:
            if os.path.exists(file):
                os.remove(file)

        os.system('java -jar kr_functions.jar ' + 'saveAllExplanations' + " " + self.working_ontology + " " + subclass_statements_path)

    '''load all explanations from datasets/exp-#.owl and return them.
    returns only one explanation for each subclass statement.'''
    def load_all_explanations(self):

        all_paths = glob.glob("datasets/exp-*.owl")
        all_explanations = []
        if len(all_paths) == 0:
            all_explanations.append("no justification")

        for filename in all_paths:
            with open(filename) as curr_exp:
                all_explanations.append(curr_exp.read())

        return all_explanations

    def get_all_explanations(self, subclass_statements_path):
        '''
        get all explanations for the subclass satements defined in a 'subclassStatements' file stored as datasets/subClasses.nt.
        Caution: this clears all the previously saved explanations. Takes the intermetiate step of first saving them all
        and them loading them again.

        :param subclass_statements_path: filepath of the file containing the subclass statements which are to be
                                        explained.
        :return: list of string representing one explanation for each statement in subClasses.nt
        '''
        # save the explainations for the current subclasses
        self.save_all_explanations(subclass_statements_path)

        # load them and return them
        return self.load_all_explanations()

    def forget_signature(self, signatures, method='2'):
        '''
        For running LETHE forget command and store resulting ontology in result.owl

        :param signatures: .txt file in which the signatures are stored which you want to forget.
        :param method:  Decide on a method for the forgetter (check the papers of LETHE to understand the different options).
                        1 - ALCHTBoxForgetter
                        2 - SHQTBoxForgetter
                        3 - ALCOntologyForgetter
        '''
        os.system('java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication'
                  ' --owlFile ' + self.working_ontology +
                  ' --method ' + method +
                  ' --signature ' + signatures)

    def get_proove(self, subclass_statement):
        """
        Generates the forgetting-based proove for a subclass statement. This statement must be entailed by the ontology.

        :param subclass_statement: The statement for which a proove should be generated.
        :type subclass_statement: str
        :return: A list of ontologies with the corresponding signature that was forgotten at each step.
        :type return: list(tuple(string, owl_ontology))
        """
        # store the shortest of the justifications
        justification = min(self.get_all_explanations(subclass_statement), key=len)
        proove = [(None, justification)]

        while(self.forgetHeuristics.has_next()):

            #save the justification to work with it.
            with open("datasets/result.owl", 'w+') as result:
                result.write(justification)

            self.set_working_ontology('datasets/result.owl')

            signature_to_forget, path = self.forgetHeuristics.choose_next()
            self.forgetHeuristics.set_ontology('datasets/result.owl')

            self.forget_signature(path)  # the resulting ontology is saved in result.owl
            # unfortunately I could not figure out why it can be saved to datasets\result.owl. So we need to copy it.
            copy('result.owl', 'datasets/result.owl')

            # set the working ontology to be the first justification for the statement.
            justification = min(self.get_all_explanations(subclass_statement), key=len)

            # save ontology and signature
            with open("datasets/result.owl") as o:
                proove.append((signature_to_forget, o.read()))

        # reset working ontology
        self.working_ontology = self.ontology

        return proove

    def get_prooves(self, subclass_statements_path):
        """
        Provides proofs for all the subclass statements in the 'subclass_statements_path' file. Each step of the proof
        is calculated by forgetting a signature.

        :param subclass_statements_path: path to the file in which all the subclass statements are we want to proof.
        :return: the resulting ontologies for each step paired with the signature that was forgotten at this step.
        :type return: list(tuple(string, owl_ontology))
        """
        prooves = []
        with open(subclass_statements_path) as statements:
            for statement in statements:
                prooves.append(self.get_proove(statement))

        return prooves


