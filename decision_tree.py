import math
class Node:
    def __init__(self, value=None, children=None):
        self.value = value
        if children is None:
            self.children = dict()
        else:
            self.children = children
    def classify(self, example):
        if len(self.children):
            return self.children[example[self.value]].classify(example)
        return self.value
    def print(self):
        print(self.value, {key:self.children[key].value for key in self.children})
        for key in self.children:
            self.children[key].print()

def arg_max(sequence):
    maxi = -1
    for i,x in enumerate(sequence):
        if maxi == -1 or x > sequence[maxi]:
            maxi = i
    return maxi
def classification_counts(examples):
    count = [0,0]
    for x in examples:
        count[int(x['class'])] += 1
    return count
def plurality_value(examples):
    count = classification_counts(examples)
    return count[1] > count[0]
def all_same(examples):
    count = classification_counts(examples)
    return count[0] == 0 or count[1] == 0
def get_values(a, examples):
    output = set()
    for x in examples:
        output.add(x[a])
    return output
def B(q):
    output = 0
    if q != 0:
        output -= q*math.log2(q)
    if 1-q != 0: 
        output -= (1-q)*math.log2(1-q)
    return output
def importance(a, examples):
    values = get_values(a, examples)
    p = len([x for x in examples if x["class"]])
    n = len([x for x in examples if not x["class"]])
    entropy = 0
    for v in values:
        pk = len([x for x in examples if x[a] == v and x["class"]])
        nk = len([x for x in examples if x[a] == v and not x["class"]])
        #print(p,n,pk,nk)
        entropy += (pk+nk)/(p+n)*B(pk/(pk+nk))
    gain = B(p/(p+n))-entropy
    return gain

def decision_tree_learning(examples, attributes, parent_examples):
    if not len(examples):
        return Node(plurality_value(parent_examples))
    elif not len(attributes):
        return Node(plurality_value(examples))
    elif all_same(examples):
        return Node(bool(arg_max(classification_counts(examples))))
    else:
        print([importance(a, examples) for a in attributes])
        A = attributes[arg_max([importance(a, examples) for a in attributes])]
        node = Node(A)
        values = get_values(A, examples)
        for v in values:
            exs = [x for x in examples if x[A] == v]
            attributes.remove(A)
            node.children[v] = decision_tree_learning(exs,attributes,examples)
            attributes.append(A)
        return node

attributes = ["alt", "bar", "fri", "hun", "pat", "price", "rain", "res", "type", "est"]
examples = []
examples.append({"alt":True,
                 "bar":False,
                 "fri":False,
                 "hun":True,
                 "pat":"Some",
                 "price":"$$$",
                 "rain":False,
                 "res":True,
                 "type":"French",
                 "est":"0-10",
                 "class":True})
examples.append({"alt":True,
                 "bar":False,
                 "fri":False,
                 "hun":True,
                 "pat":"Full",
                 "price":"$",
                 "rain":False,
                 "res":False,
                 "type":"Thai",
                 "est":"30-60",
                 "class":False})
tree = decision_tree_learning(examples, attributes, examples)
print(tree.classify(examples[0]))
