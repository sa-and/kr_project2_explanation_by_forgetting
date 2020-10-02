import os
import glob


class Explainer:
    '''
    Class mainly to provide a wrapper for the functions provided in kr_functions.jar to make them
    accessable more easily.
    '''

    def __init__(self, ontology):
        self.ontology = ontology

    def set_ontology(self, ontology):
        self.ontology = ontology

    '''print all subClass statements (explicit and inferred) Ontology    '''
    def print_all_subclasses(self):
        os.system('java -jar kr_functions.jar ' + 'printAllSubClasses' + " " + self.ontology)

    ''' save all subClass statements (explicit and inferred) in the inputOntology to file datasets/subClasses.nt'''
    def save_all_subclasses(self):
        os.system('java -jar kr_functions.jar ' + 'saveAllSubClasses' + " " + self.ontology)

    '''print all explanations for the subclass satements defined in a 'subclassStatements' file'''
    def print_all_explanations(self, subclass_statements_path):
        os.system('java -jar kr_functions.jar ' + 'printAllExplanations' + " " + self.ontology + " " + subclass_statements_path)

    '''save all explanations for the subclass satements defined in a 'subclassStatements' file to file datasets/exp-#.owl
    Caution: this clears all the previously saved explanations. Takes the intermediate step of first saving them all
    and them loading them again.'''
    def save_all_explanations(self, subclass_statements_path):
        # clear already present explanations
        all_paths = glob.glob("datasets/exp-*.owl")

        for file in all_paths:
            if os.path.exists(file):
                os.remove(file)

        os.system('java -jar kr_functions.jar ' + 'saveAllExplanations' + " " + self.ontology + " " + subclass_statements_path)

    '''load all explanations from datasets/exp-#.owl and return them.
    returns only one explanation for each subclass statement.'''
    def load_all_explanations(self):

        all_paths = glob.glob("datasets/exp-*.owl")
        all_explanations = []

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
                  ' --owlFile ' + self.ontology +
                  ' --method ' + method +
                  ' --signature ' + signatures)

