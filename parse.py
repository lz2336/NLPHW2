from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
import sys

for line in sys.stdin:
	tp = TransitionParser.load(sys.argv[1])
	sentence = DependencyGraph.from_sentence(line)
	parsed = tp.parse([sentence])
	print parsed[0].to_conll(10).encode('utf-8')


        