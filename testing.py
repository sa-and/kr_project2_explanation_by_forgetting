# file for random testing

from explainer import Explainer
from forgetHeuristics import ForgetFromList, AndiHeuristic
import glob
import os


def save_proof(proof):
    # clear previous proof
    all_paths = glob.glob("datasets/proof*.owl")

    for file in all_paths:
        if os.path.exists(file):
            os.remove(file)

    count = 1
    for line in proof:
        with open('datasets/proof_line_'+str(count)+'.owl', 'w+') as f:
            f.write(line[1])

        count += 1

def print_proof(proof):
    #print the proove
    for line in proof:
        print('forgetting ' + str(line[0]))
        print(str(line[1]))



# Pizza example
heur = ForgetFromList('datasets/pizza.owl', ["http://www.co-ode.org/ontologies/pizza/pizza.owl#SundriedTomatoTopping"])

explainer = Explainer("datasets/pizza.owl", heur)

# university example
#heur = ForgetFromList('datasets/university-example.owl', ["http://example.com/myOntology/Professor"])
#explainer = Explainer('datasets/university-example.owl', heur)

#explainer.print_all_subclasses()
#explainer.save_all_subclasses()
#explainer.print_all_explanations('datasets/subClasses.nt')
#explainer.save_all_explanations('datasets/subClasses.nt')
#explanations = explainer.load_all_explanations()
#explanations = explainer.get_all_explanations('datasets/subClasses.nt')
#print(explanations)
# proove = explainer.get_proove("datasets/subClasses.nt")

# save_proof(proove)


# testing heuristic
heur = AndiHeuristic('datasets/pizza.owl',
                     ("http://www.co-ode.org/ontologies/pizza/pizza.owl#CheeseyVegetableTopping", "http://www.co-ode.org/ontologies/pizza/pizza.owl#Food"))

explainer = Explainer('datasets/pizza.owl', heur)

proof = explainer.get_proove('datasets/subClasses.nt')

save_proof(proof)
print_proof(proof)