# file for random testing

from explainer import Explainer
from forgetHeuristics import ForgetFromList
import glob
import os


def save_proof(proof):
    # clear previous proof
    all_paths = glob.glob("datasets/proof*.owl")

    for file in all_paths:
        if os.path.exists(file):
            os.remove(file)

    count = 1
    for line in proove:
        with open('datasets/proof_line_'+str(count)+'.owl', 'w+') as f:
            f.write(line[1])

        count += 1


# Pizza example
with open('datasets/pizza_super_simple.owl') as ont:
    heur = ForgetFromList(ont.read(), [ "http://www.co-ode.org/ontologies/pizza/pizza.owl#SundriedTomatoTopping",
                                    "http://www.co-ode.org/ontologies/pizza/pizza.owl#GoatCheeseTopping",
                                    "http://www.co-ode.org/ontologies/pizza/pizza.owl#hasTopping"])

explainer = Explainer("datasets/pizza_super_simple.owl", heur)

# university example
#with open('datasets/university-example.owl') as ont:
#    heur = ForgetFromList(ont.read(), ["http://example.com/myOntology/Professor"])
#explainer = Explainer('datasets/university-example.owl', heur)

#explainer.print_all_subclasses()
#explainer.save_all_subclasses()
#explainer.print_all_explanations('datasets/subClasses.nt')
#explainer.save_all_explanations('datasets/subClasses.nt')
#explanations = explainer.load_all_explanations()
#explanations = explainer.get_all_explanations('datasets/subClasses.nt')
#print(explanations)
proove = explainer.get_proove("datasets/subClasses.nt")
#print the proove
for line in proove:
    print('forgetting ' + str(line[0]))
    print(str(line[1]))

save_proof(proove)
