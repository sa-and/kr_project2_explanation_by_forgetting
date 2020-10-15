from explainer import Explainer
from forgetHeuristics import StandardHeuristics
import sys

ontology_file = sys.argv[2]
subsumption_file = sys.argv[4]
justification_step = sys.argv[6]
if justification_step == 'False':
    justification_step = False
else:
    justification_step = True

# load subsumption
with open(subsumption_file) as f:
    nt_string = f.readline()

comp = nt_string.split()
subsumption = (comp[0][1:-1], comp[2][1:-1])

heuristic = StandardHeuristics(ontology_file, subsumption)
explainer = Explainer(ontology_file, heuristic)

proof = explainer.get_proove(subsumption_file, justification_step)

for line in proof:
    print("justification after forgetting " + str(line[0]))
    print(str(line[1]))