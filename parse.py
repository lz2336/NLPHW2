from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
	
sentence = DependencyGraph.from_sentence('Hi, this is a test')
tp = TransitionParser.load(model)
parsed = tp.parse([sentence])
print parsed[0].to_conll(10).encode('utf-8')


        # parsing arbitrary sentences (english):