# file for random testing

from explainer import Explainer
from forgetHeuristics import forgetFromList

forgetHeuristics = forgetFromList([ "http://www.co-ode.org/ontologies/pizza/pizza.owl#hasTopping"])
explainer = Explainer("datasets/pizza_super_simple.owl", forgetHeuristics)
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