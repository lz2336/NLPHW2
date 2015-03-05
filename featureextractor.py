from nltk.compat import python_2_unicode_compatible
import math

printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def get_word_distance(idx1, idx2):
        """
        Get distance between two words
        """
        return str(math.fabs(idx1 - idx2))

    @staticmethod
    def get_num_intervening_NV(idx1, idx2, tokens):
        if idx1 < idx2:
            i, j = idx1, idx2
        else:
            i, j = idx2, idx1

        num_intervening_VV = 0
        num_intervening_NN = 0
        for token_idx in range(i, j + 1):
            token = tokens[token_idx]
            if 'tag' in token:
                if token['tag'] == 'VV':
                    num_intervening_VV += 1
                if token['tag'] == 'NN':
                    num_intervening_NN += 1
        return str(num_intervening_NN), str(num_intervening_VV)


    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    @staticmethod
    def get_num_children(idx, arcs):
        left_children = 0
        right_children = 0
        for (wi, r, wj) in arcs:
            if wi == idx:
                if wj > wi:
                    right_children += 1
                if wj < wi:
                    left_children += 1
        return str(left_children), str(right_children)

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            print("This is not a very good feature extractor!")
            printed = True

        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

            # if 'lemma' in token and FeatureExtractor._check_informative(token['lemma']):
            #     result.append('STK_0_LEMMA_' + token['lemma'])

            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                result.append('STK_0_POSTAG_' + token['tag'])

            if 'ctag' in token and FeatureExtractor._check_informative(token['ctag']):
                result.append('STK_0_CPOSTAG_' + token['ctag'])

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

            #Number of left and right children for STK_0
            num_leftchildren, num_rightchildren= FeatureExtractor.get_num_children(stack_idx0, arcs)
            result.append('STK_0_LCHILDREN_' + num_leftchildren)
            result.append('STK_0_RCHILDREN_' + num_rightchildren)

            if len(stack) > 1:
                stack_idx1 = stack[-2]
                token_1 = tokens[stack_idx1]

                if FeatureExtractor._check_informative(token_1['word'], True):
                    result.append('STK_1_FORM_' + token_1['word'])

                if 'tag' in token_1 and FeatureExtractor._check_informative(token_1['tag']):
                    result.append('STK_1_POSTAG_' + token_1['tag'])

                if 'feats' in token_1 and FeatureExtractor._check_informative(token_1['feats']):
                    feats = token_1['feats'].split("|")
                    for feat in feats:
                        result.append('STK_1_FEATS_' + feat)

                # if 'ctag' in token_1 and FeatureExtractor._check_informative(token_1['ctag']):
                #     result.append('STK_1_CPOSTAG_' + token_1['ctag'])


        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            
            # print token

            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            # if 'lemma' in token and FeatureExtractor._check_informative(token['lemma']):
            #     result.append('BUF_0_LEMMA_' + token['lemma'])

            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                result.append('BUF_0_POSTAG_' + token['tag'])

            if 'ctag' in token and FeatureExtractor._check_informative(token['ctag']):
                result.append('BUF_0_CPOSTAG_' + token['ctag'])

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

            #Number of left and right children for BUF_0
            num_leftchildren, num_rightchildren = FeatureExtractor.get_num_children(buffer_idx0, arcs)
            result.append('BUF_0_LCHILDREN_' + num_leftchildren)
            result.append('BUF_0_RCHILDREN_' + num_rightchildren)

            if len(buffer) > 1:
                buffer_idx1 = buffer[1]
                token_1 = tokens[buffer_idx1]

                if FeatureExtractor._check_informative(token_1['word'], True):
                    result.append('BUF_1_FORM_' + token_1['word'])

                if 'tag' in token_1 and FeatureExtractor._check_informative(token_1['tag']):
                    result.append('BUF_1_POSTAG_' + token_1['tag'])

                if 'feats' in token_1 and FeatureExtractor._check_informative(token_1['feats']):
                    feats = token_1['feats'].split("|")
                    for feat in feats:
                        result.append('BUF_1_FEATS_' + feat)

                # if 'ctag' in token_1 and FeatureExtractor._check_informative(token_1['ctag']):
                #     result.append('BUF_1_CPOSTAG_' + token_1['ctag'])

            if len(buffer) > 2:
                buffer_idx2 = buffer[2]
                token_2 = tokens[buffer_idx2]

                if FeatureExtractor._check_informative(token_2['word'], True):
                    result.append('BUF_2_FORM_' + token_2['word'])

                if 'tag' in token_2 and FeatureExtractor._check_informative(token_2['tag']):
                    result.append('BUF_2_POSTAG_' + token_2['tag'])

                # if 'ctag' in token_2 and FeatureExtractor._check_informative(token_2['ctag']):
                #     result.append('BUF_2_CPOSTAG_' + token_2['ctag'])

            if len(buffer) > 3:
                buffer_idx3 = buffer[3]
                token_3 = tokens[buffer_idx3]

                if FeatureExtractor._check_informative(token_3['word'], True):
                    result.append('BUF_3_FORM_' + token_3['word'])

                if 'tag' in token_3 and FeatureExtractor._check_informative(token_3['tag']):
                    result.append('BUF_3_POSTAG_' + token_3['tag'])

                # if 'ctag' in token_3 and FeatureExtractor._check_informative(token_3['ctag']):
                #     result.append('BUF_3_CPOSTAG_' + token_3['ctag'])

            if stack:
                stack_idx0 = stack[-1]
                word_distance_0 = FeatureExtractor.get_word_distance(stack_idx0, buffer_idx0)
                num_intervening_NN, num_intervening_VV = FeatureExtractor.get_num_intervening_NV(stack_idx0, buffer_idx0, tokens)
                result.append('STK_BUF_DIST_0_' + word_distance_0)
                result.append('STK_BUF_INTV_NN' + num_intervening_NN)
                result.append('STK_BUF_INTV_VV_' + num_intervening_VV)

        return result
