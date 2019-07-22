class suffixNode:
    def __init__(self,tree,id):
        self.tree       = tree
        self.id         = id
        self.start      = None
        self.end        = None
        self.parent     = None
        self.note       = None # suffix link (internal node) OR origin (leaf)
        self.children   = dict()
    def __len__(self):
        if self.start is None: return 0
        return self.end - self.start
    def __str__(self):
        out = ""
        if self.start is None:
            out += "ROOT"
        else:
            out += "\"{}\"".format(self.tree.string[self.start:self.end])
        out += " ["
        for child in self.children.values(): out += " {}".format(child)
        out += "]"
        if len(self.children) and self.id: out += " ({})".format(self.note)
        return out
class suffixTree:
    def __init__(self,string):
        string = string + '\0'
        # setup empty tree
        self.string     = string
        self.nodes      = [suffixNode(self,0)]
        # loop variables
        look = self.nodes[0]
        suffixTail = None #
        old_end = 0
        for path_start in range(len(string)-1):
            # ASCEND
            if look.note is None and look.id:
                path_end -= len(look)
                look = self.nodes[look.parent]
            if not look.id: path_end = path_start
            else:           look = self.nodes[look.note]
            # DESCEND
            while True:
                split = 0
                # check if this is the suffixHead for a hanging tail
                if suffixTail and old_end == path_end:
                    suffixTail.note = look.id
                    suffixTail = None
                # end of string in tree, break out to create leaf
                if string[path_end] not in look.children: break
                # continue descent along appropriate branch
                chld = self.nodes[look.children[string[path_end]]]
                # count+skip
                if path_end + len(chld) <= old_end:
                    path_end += len(chld)
                    look = chld
                    continue
                elif path_end < old_end:
                    split = chld.start  + (old_end - path_end)
                    path_end = path_end + (old_end - path_end)
                else:
                    split = chld.start + 1
                    path_end += 1
                # char by char comparison (worst case)
                while split < chld.end and string[split] == string[path_end]:
                    split += 1
                    path_end += 1
                if split == chld.end:
                    look = chld
                    continue
                else: break
            # CREATE INNER NODE
            if split:
                look = self.createNode(look,chld,split)
                if suffixTail: suffixTail.note = look.id
                suffixTail = look
            # CREATE LEAF/OUTER NODE
            self.createLeaf(look,path_end,path_start)
            old_end = path_end
            # END
            #print(self)
    def createNode(self,prnt,chld,split):
        # create new node
        node = suffixNode(self,len(self.nodes))
        self.nodes.append(node)
        node.start  = chld.start
        node.end    = split
        node.parent = prnt.id
        node.children[self.string[split]] = chld.id
        # update child
        chld.start  = split
        chld.parent = node.id
        # update parent
        prnt.children[self.string[node.start]] = node.id
        # suffix tail special case
        if len(node) == 1 and node.parent == 0: node.note = 0
        # send new node
        return node
    def createLeaf(self,prnt,suffix,origin):
        node = suffixNode(self,len(self.nodes))
        node.start  = suffix
        node.end    = len(self.string)
        node.parent = prnt.id
        node.note   = origin
        prnt.children[self.string[node.start]] = node.id
        self.nodes.append(node)
    def __str__(self):
        out = self.string + "\n"
        for n,node in enumerate(self.nodes):
            out = out + "{:2}: {}\n".format(n,str(node))
        return out + "------------------------------------------"
if __name__=="__main__":
    print(suffixTree("abacb"))
    print(suffixTree("abacbaba"))
    print(suffixTree("ababa"))
    print(suffixTree("ababacde"))
    print(suffixTree("abaa"))
    print(suffixTree("abcdecdeabcdecd"))
    #print(suffixTree("i'm just going to write a whole bunch and than this will be tested beacause it is this thing which is in need of this testing"))
    print(suffixTree(""))
