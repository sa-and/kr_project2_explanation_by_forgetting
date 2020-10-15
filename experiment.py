from forgetHeuristics import StandardHeuristics
from explainer import Explainer
import glob
import os
from xmldiff import main as xmldiff

############# METHODS #####################
def get_sub_from_nt(nt_string):
    comp = nt_string.split()
    return comp[0][1:-1], comp[2][1:-1]

def save_proof(proof, file_prefix):
    # clear previous proof
    all_paths = glob.glob("datasets/proof"+file_prefix+"*.owl")

    for file in all_paths:
        if os.path.exists(file):
            os.remove(file)

    count = 1
    for line in proof:
        with open('datasets/proof'+file_prefix+'_line_'+str(count)+'.owl', 'w+') as f:
            f.write(line[1])

        count += 1

def print_proof(proof):
    #print the proove
    for line in proof:
        print('forgetting ' + str(line[0]))
        print(str(line[1]))


############# SCRIPT #################
# set up things
ontology = 'datasets/snomed_organism_1.1.owl'
all_subclasses_file = "datasets/snomed_orga_all_subClasses.nt"
heuristic = StandardHeuristics(ontology, ('dummy', 'dummy'))
explainer = Explainer(ontology, heuristic)

# container for amount of differences for each subsumption. 100 if lines of proofs differ. -1 if there was an error
differences = []
processed_proofs = 0
num_samples = 50

# loop over all subclasses entailed by the ontology
with open(all_subclasses_file) as f:
    for subclass in f.readlines():
        # Load the current subsumption for heuristics and explainer
        subsumbtion_signatures = get_sub_from_nt(subclass)
        heuristic.set_subsumption(subsumbtion_signatures)
        with open('datasets/subClasses.nt', 'w+') as curr_sub_f:
            curr_sub_f.write(subclass)

        # get the proofs
        try:
            proof_just = explainer.get_proove('datasets/subClasses.nt', justification_step=True)
            proof_no_just = explainer.get_proove('datasets/subClasses.nt', justification_step=False)
        except Exception:  # this is really bad... but for the timeframe necessary
            # reset working ontology
            explainer.working_ontology = ontology
            heuristic.set_ontology(ontology)
            differences.append(-1)
            print("\n\n############################ ERROR ####################################\n\n")
            continue

        # compare proofs
        if len(proof_just) != len(proof_no_just):  # different number of lines in the proof
            differences.append(100)
        else:
            printing = False
            for i in range(len(proof_just)):
                # gets the number of changes that would be needed to transform the left ontology into the right one.
                diffs = xmldiff.diff_texts(proof_just[i][1], proof_no_just[i][1])
                # Ignore the order of the nodes. They do not change what is entailed by the Ontology
                diffs = [diff for diff in diffs if str(diff)[:10] == 'InsertNode']
                differences.append(len(diffs))
                if len(diffs) > 0:
                    printing = True

            print_proof(proof_no_just)
            print_proof(proof_just)

        # save differences after each step so they are available even when program is aborted
        with open('datasets/differences.txt', 'w+') as diff_f:
            diff_f.write(str(differences))

        processed_proofs += 1
        print("\n\n!!!!!!!!!! proofs compared: " + str(processed_proofs) + " out of " + str(num_samples))
        if processed_proofs == num_samples:
            print("##########EXPERIMENT FINISHED!################")
            break


