# file for random testing

from explainer import Explainer

explainer = Explainer("datasets/pizza.owl")
#explainer.print_all_subclasses()
explainer.save_all_subclasses()
#explainer.print_all_explanations('datasets/subClasses.nt')
#explainer.save_all_explanations('datasets/subClasses.nt')
#explanations = explainer.load_all_explanations()
explanations = explainer.get_all_explanations('datasets/subClasses.nt')
print(explanations)