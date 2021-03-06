class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        if not conf.buffer or not conf.stack:
            return -1

        idx_s = conf.stack[-1]

        if not idx_s == 0:
            
            for arc in conf.arcs:
                if arc[2] == idx_s:
                    return -1
                    break
            idx_b = conf.buffer[0]
            conf.arcs.append((idx_b, relation, idx_s))
            conf.stack.pop(-1)

        else:
            return -1
        

        #raise NotImplementedError('Please implement left_arc!')
        #return -1

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.stack:
            return -1

        idx_wi = conf.stack[-1]

        has_head = 0
        
        for arc in conf.arcs:
            if arc[2] == idx_wi:
                has_head = 1
                break

        if has_head:
            conf.stack.pop(-1)
        else:
            return -1


        #raise NotImplementedError('Please implement reduce!')
        #return -1

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        if not conf.buffer:
            return -1
        
        idx_i = conf.buffer.pop(0)
        conf.stack.append(idx_i)

        #raise NotImplementedError('Please implement shift!')
        #return -1
