**************************************************
COMS4705 Natural Language Processing Spring 2015
		Assignment 2
		Lingzi Zhuang
	     lz2336@columbia.edu
**************************************************

Submission
~lz2336/hidden/9770232605/Homework2/

NOTE: TO TEST ON DIFFERENT LANGUAGES: COMMENT IN THE FOLLOWING LINES IN TEST.PY CORRESPONDING TO THE LANGUAGE:
	data = dataset.get_$LANGUAGE_train_corpus().parsed_sents()
	tp.save(‘$LANGUAGE.model')
	testdata = dataset.get_$LANGUAGE_test_corpus().parsed_sents()
	conllFile = ‘$LANGUAGE.conll'


Output and Comments

1b. 
  Projective sentences are ones whose dependency structure does not contain crossed arcs (when graphed). Linguistically speaking, it means that the dependency relationships (i.e. phrasal structures and inter-phrasal nesting relationships) are uninterrupted everywhere in the sentence.
  To determine if there are crossed arcs in a dependency graph, we iterate through a list of the arcs in the graph. For each arc starting at parentIdx and terminating at childIdx, we find all the arcs originating from, or terminating in, the region between parentIdx and childIdx, whose other end falls outside of said region (and thus creates a cross with the current arc in question).

1c.
  Example sentence with projective dependency graph:
	Mary had a little lamb.
  Example sentence with non-projective dependency graph:
	He is wise who fears God and knows the nature of men.

2b.
  Using badfeatures.model, the program returns
  UAS: 0.229038040231 
  LAS: 0.125473013344
  - This means: 12.5% of the tokens were assigned both the correct HEAD and the correct dependency RELation; 23% were assigned the correct HEAD, regardless of the correctness of RELation. This is pretty lousy performance.

3a.
  Below is the list of features in my feature extractor:
  - STK_0: form, feats, postag, ldep, rdep, leftchildren, rightchildren
  - STK_1: form, postal, feats
  - BUF_0: form, feats, postag, ldep, rdep, leftchildren, rightchildren
  - BUF_1: form, feats, postag, ldep, rdep
  - non-static features: POS-measured distance btw STK_0 and BUF_0: # intervening nouns, # intervening verbs

  Complexities:
  - FORM, FEATS, POSTAG: O(1), because dict has constant time accessing
  - LDEP, RDEP: O(n), because to find the leftmost and rightmost dependencies of a token, the entire list of arcs is traversed once.
  - LCHILDREN, RCHILDREN: O(n), because to count the number of left and right dependencies of a token, the entire list of arcs is traversed once.
  - INTV_NN, INTV_VV: O(n), because to count the number of NN/VV-annotated words between STK_0 and BUF_0, the entire range between the two is traversed once.

  Individual features and performance
  - Adding POSTAG features (especially for STK_0 and BUF_0) dramatically increases performance [from (<30, <20) to (~70, ~60)]. This is obviously because the POS tag for each word is the most relevant basis for determining dependencies. For example, it’s much easier to determine a AJ->NN dependency than, say, a “profound”->”perplexity” dependency. Adding subsequent POSTAG features for words deeper in the stack and buffer gave single-digit increases: (70, 60) to (74, 63.5)
 - The FORM feature gives small increases (e.g. adding STK_0 and STK_1_FORM brought scores from (74.0, 63.5) to (74.2, 63.9)). This is because words themselves can carry information for parsing: “the” is very likely a children of the word immediately following it.
 - The L/RCHILDREN feature (for STK_0 and BUF_0) also gives meaningful increases (>1%). This is likely because the number of children contains information about the position of the word within the dependency “hierarchy” (e.g. the main verb likely has more children than a noun)
 - POS-measured distance between STK_0 and BUF_0 gave small increases (VV ~0.3%, NN ~0.2). This is also because the number of VVs and NNs in between can be a hint for the likely relationship of the parsed vs unparsed portions in the hierarchy (again thinking in terms of syntactic trees).

3c. 

Swedish:
  UAS: 0.792471619199 
  LAS: 0.682931686915
Danish:
  UAS: 0.803592814371 
  LAS: 0.717964071856
English:
  UAS: 0.762962962963 
  LAS: 0.733333333333
Korean:
  UAS: 0.754731556586 
  LAS: 0.626110467362

3d.
  The Arc-Eager shift-reduce parser has a complexity of O(n). This is because  for each sentence, the parser moves through all the tokens in the sentence once over, by shifting the sentence onto the stack token by token and reducing lower-level nodes to their heads. Specifically, to construct the dependency graph of a projective sentence (or, equivalently, a binary-branching syntactic tree) with n words, the parser adds at most n-1 dependencies (or, in terms of tree structure, adds at most n-1 binary-branching phrasal roots). This says that the worst-case complexity of the Arc-Eager shift-reduce parser is O(2n) (O(n) shifts + O(n) reductions). In any case, the overall complexity is linear.
  Tradeoff: The Arc-Eager shift-reduce parser constructs a dependency graph from bottom up. Given a configuration, an Arc-Eager shift-reduce parser determines an optimal transition based on its training (which is dependent on the features specified). Therefore:
	- it assumes projectivity (and works well only when the sentence is projective), while in fact the sentence might not be projective.
	- it might not be particularly sensitive to “deceptive” sentences whose correct parsing is different from what the front portion of the words might suggest. (Something like “She is pretty / fat” but longer than what the features can capture. Our features in this model do not go very deep.)