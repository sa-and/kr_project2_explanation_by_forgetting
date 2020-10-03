# file for random testing

from explainer import Explainer
from forgetHeuristics import forgetFromList

forgetHeuristics = forgetFromList([ "http://www.co-ode.org/ontologies/pizza/pizza.owl#American",
                                    "http://www.co-ode.org/ontologies/pizza/pizza.owl#NamedPizza",
                                    "http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza"])
explainer = Explainer("datasets/test.owl", forgetHeuristics)
#explainer.print_all_subclasses()
#explainer.save_all_subclasses()
#explainer.print_all_explanations('datasets/subClasses.nt')
#explainer.save_all_explanations('datasets/subClasses.nt')
#explanations = explainer.load_all_explanations()
#explanations = explainer.get_all_explanations('datasets/subClasses.nt')
#print(explanations)
proove = explainer.get_proove("datasets/subClasses.nt")