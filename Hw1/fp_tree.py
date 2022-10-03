from itertools import combinations

# fake_dataset = [
#     ["f", "c", "a", "m", "p"],
#     ["f", "c", "a", "b", "m"],
#     ["f", "b"],
#     ["c", "b", "p"],
#     ["f", "c", "a", "m", "p"]
# ]

fake_dataset = [
    ["milk", "bread", "beer"],
    ["bread", "coffee"],
    ["bread", "egg"],
    ["milk", "bread", "coffee"],
    ["milk", "egg"],
    ["bread", "egg"],
    ["milk", "egg"],
    ["milk", "bread", "egg", "beer"],
    ["milk", "bread", "egg"],
]


class node:
    def __init__(self, item):
        self.item = item
        self.count = 1
        self.parent = None
        self.children = list()

    def __str__(self):
        return f'id={id(self)}, item={self.item}, count={self.count}, parent={self.parent.item}, children_num={len(self.children)}'


# nx3 list, [0]=Customer ID, [1]=Transaction ID, [2] Item ID
def load_data(filename):
    dataset = list()
    with open(filename) as f:
        tid = 1  # transaction id
        temp_item = list()
        for i in f.readlines():
            item = i.replace("\n", "").split(",")
            if tid < int(item[1]):
                tid = int(item[1])
                dataset.append(temp_item.copy())
                temp_item.clear()
            temp_item.append(item[2])
    # for i in dataset:
    #     print(i)
    return dataset


def first_scan(dataset):
    weights = dict()
    for transaction in dataset:
        for item in transaction:
            if weights.get(item):
                weights[item] += 1
            else:
                weights[item] = 1
    return weights


def reorder(dataset, weights):
    for transaction in dataset:
        transaction.sort(key=lambda x: weights[x], reverse=True)


def create_tree(dataset):
    root = node(None)
    pre_node = root
    for transaction in dataset:
        for item in transaction:
            for c in pre_node.children:
                if item == c.item:
                    c.count += 1
                    pre_node = c
                    break
            else:  # new node
                print("new node:", item, "parent:", pre_node.item)
                current_node = node(item)
                current_node.parent = pre_node
                pre_node.children.append(current_node)
                pre_node = current_node

                # create header table link
                # if header_table.get(item):
                #     header_table[item].append(current_node)
                # else:
                #     header_table[item] = [current_node]
        pre_node = root
        print("============================")
        show_tree(root)  # current tree after insert one transaction
        print("============================")

    # print("@@@FP tree@@@")
    # show_tree(root)  # final tree
    # print("@@@header table@@@")
    # show_header_table(header_table)  # final header table
    return root


def create_header_table(node, header_table=dict()):
    if node.item != None:  # skip root node
        # create header table link
        if header_table.get(node.item):
            header_table[node.item].append(node)
        else:
            header_table[node.item] = [node]
    for c in node.children:
        create_header_table(c, header_table)
    return header_table


def find_path(header_table, target):
    path_list = list()
    for k, v in header_table.items():
        if k == target:
            for node in v:
                path = list()
                parent = node.parent
                while parent.item != None:  # get parent
                    path.append([parent.item, node.count])
                    parent = parent.parent
                path.reverse()
                if len(path) != 0:  # first child of root
                    path_list.append(path)
            return path_list

    # if node.item != None and node.item == target:  # skip root node
    #     path = list()
    #     parent = node.parent
    #     while parent.item != None: # get parent
    #         path.append([parent.item, node.count])
    #         parent = parent.parent
    #     path.reverse()
    #     path_list.append(path)
    #     return path_list
    # for c in node.children:
    #     path_list = find_path(c, target, path_list)
    # return path_list


def mine_tree(path_list, min_sup, freq_itemset):
    # path_list EX:
    # [
    #   [['bread', 2], ['milk', 2]]
    #   [['bread', 2]]
    #   [['milk', 2]]
    # ]
    temp_foo_dataset = list()
    final_foo_dataset= list()
    for path in path_list:
        for p in path:
            temp_foo_dataset.extend([p[0]]*p[1])
        final_foo_dataset.append(temp_foo_dataset.copy())
        temp_foo_dataset.clear()
    

    for i in final_foo_dataset:
        print(i)

    weights = first_scan(final_foo_dataset)
    print(weights)
    print("before ordering:", final_foo_dataset)
    reorder(final_foo_dataset, weights)
    print("after ordering:", final_foo_dataset)

    root = create_tree(final_foo_dataset)
    print("@@@FP tree@@@")
    show_tree(root)
    header_table = create_header_table(root)
    print("@@@header table@@@")
    show_header_table(header_table)
        


def show_tree(node):
    if node.item != None:  # skip root node
        print(node)
    for c in node.children:
        show_tree(c)


def show_header_table(header_table):
    for k, v in header_table.items():
        print("item:", k)
        for node in v:
            print(id(node))


if __name__ == "__main__":
    # dataset = load_data("gen/output.txt")
    weights = first_scan(fake_dataset)
    print(weights)
    print("before ordering:", fake_dataset)
    reorder(fake_dataset, weights)
    print("after ordering:", fake_dataset)

    root = create_tree(fake_dataset)
    # print("@@@FP tree@@@")
    # show_tree(root)

    header_table = create_header_table(root)
    # print("@@@header table@@@")
    # show_header_table(header_table)

    freq_itemset = list()
    min_sup = 2
    for i in find_path(header_table, "egg"):
        print(i)
    mine_tree(find_path(header_table, "egg"), min_sup, freq_itemset)
