# fake_dataset = [
#     ["f", "c", "a", "m", "p"],
#     ["f", "c", "a", "b", "m"],
#     ["f", "b"],
#     ["c", "b", "p"],
#     ["f", "c", "a", "m", "p"]
# ]
class node:
    def __init__(self, item, count=1):
        self.item = item
        self.count = count
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
    return dataset


# 掃描全dataset一次，統計每個item出現的次數
def first_scan(dataset):
    weights = dict()
    for transaction in dataset:
        for item in transaction:
            if weights.get(item):
                weights[item] += 1
            else:
                weights[item] = 1
    return weights


# 排序transaction內的item，並刪除小於最小最小支持度的item
def reorder(dataset, weights, min_sup):
    for tid in range(len(dataset)):
        dataset[tid] = [item for item in dataset[tid] if weights[item] >= min_sup]
        dataset[tid].sort(key=lambda x: weights[x], reverse=True)


# 建立FP tree，傳root代表update tree
def create_tree(dataset, root=node(None), count=1):
    pre_node = root
    for transaction in dataset:
        for item in transaction:
            for c in pre_node.children:
                if item == c.item:
                    c.count += count
                    pre_node = c
                    break
            else:  # new node
                # print("new node:", item, "parent:", pre_node.item)
                current_node = node(item, count)
                current_node.parent = pre_node
                pre_node.children.append(current_node)
                pre_node = current_node
        pre_node = root
        # print("========================================================")
        # show_tree(root)  # current tree after insert one transaction
        # print("========================================================")
    return root


# header_table key=item, value=list of node
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


# 用header_table的list找所有的parent path
def find_path(header_table, target):
    path_dict = dict()
    for k, v in header_table.items():
        if k == target:
            for node in v:
                path = list()
                parent = node.parent
                while parent.item != None:  # get parent
                    path.append(parent.item)
                    parent = parent.parent
                path.reverse()
                if len(path) != 0:  # first child of root
                    path_dict[tuple(path)] = node.count
            return path_dict


# 建立combination tree
def mine_tree(path_dict):
    # sort dict by value
    combination_dataset, counts = zip(*[(dict[0], dict[1])
                                      for dict in sorted(path_dict.items(), key=lambda x:x[1], reverse=True)])
    # print("@@@combination_dataset@@@", combination_dataset)
    # print("@@@counts@@@", counts)

    root = node(None)
    for transaction, count in zip(combination_dataset, counts):
        root = create_tree([transaction], root=root, count=count)
    print("@@@Combination FP tree@@@")
    show_tree(root)
    return root


def del_bad_node(node, min_sup):
    if node.item != None:  # skip root node
        pass
    for c in node.children[::-1]:
        if c.count < min_sup:
            node.children.remove(c)
        else:
            del_bad_node(c, min_sup)


def find_freq_item_set(node, freq_item_set, foo_dict):
    # if node.item==None or node.parent.item==None:
    #     print("清空", node.item)
    #     freq_item_set = dict()
    for c in node.children:
        new_freq_item_set = freq_item_set.copy()
        if c.parent.item == None:
            # print("清空")
            new_freq_item_set = dict()
        # print("不選", c.item, ", parent", c.parent.item)
        find_freq_item_set(c, new_freq_item_set, foo_dict)
        # print("選", c.item, c.parent.item)
        # print("有前", new_freq_item_set)
        if new_freq_item_set.get(c.item):
            new_freq_item_set[c.item] += c.count
        else:
            new_freq_item_set[c.item] = c.count
        # print("有後", new_freq_item_set)
        find_freq_item_set(c, new_freq_item_set, foo_dict)
        print("freq_item_set", new_freq_item_set)

        s = frozenset()
        temp_min = 999
        for k, v in new_freq_item_set.items():
            s = s.union(frozenset((k,)))
            v = min(temp_min, v)
        if foo_dict.get(s):
            foo_dict[s] += v
        else:
            foo_dict[s] = v


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


def fp_growth(input_data, args):
    min_sup = args.min_sup
    min_conf = args.min_conf
    fake_dataset = input_data

    weights = first_scan(fake_dataset)
    print(weights)
    print("before ordering:", fake_dataset)
    reorder(fake_dataset, weights, min_sup)
    print("after ordering:", fake_dataset)

    root = create_tree(fake_dataset)
    print("@@@FP tree@@@")
    show_tree(root)

    header_table = create_header_table(root)
    print("@@@header table@@@")
    show_header_table(header_table)

    # freq_itemset = list()
    print("@@@path@@@")
    final_list = list()
    for header in header_table:
        print("@@@", header, "的pattern @@@")
        tmp = list()
        path_dict = find_path(header_table, header)
        for k, v in path_dict.items():
            print(k, v)
        if len(path_dict) > 0:
            root = mine_tree(path_dict)
            # del_bad_node(root, min_sup)
            # print("@@@after remove bad node@@@")
            # show_tree(root)
            print("@@@ 選或不選的各種組合 @@@")
            foo = dict()
            foo_dict = dict()
            # 會順便把找到的組合如{k1:v1, k2:v2} 變成 {frozenset(k1, k2): min(v1,v2)}，存到foo_dict
            find_freq_item_set(root, foo, foo_dict)
            for k, v in foo_dict.items():
                if v >= min_sup:
                    tmp.append([k.union(frozenset((header,))), v])  # remove小於min_sup的，然後把自己加進去
        if len(tmp) > 0:  # 避免掉空陣列
            final_list.extend(tmp.copy())

    # 加入one item set
    tmp = list()
    for k, v in weights.items():
        if v >= min_sup:
            tmp.append([frozenset((k,)), v])
    
    if len(tmp)>0:
        final_list.extend(tmp.copy())

    print(len(final_list))
    final_list = sorted(final_list, key=lambda x: len(x[0]))

    trans_len = 1
    tmp = list()
    tmp_final_list = list()
    print("@@@ 相同的key加起來後 @@@")
    for i in final_list:
        if len(i[0]) == trans_len:
            tmp.append(i.copy())
        else:
            print("tmp",tmp)
            tmp_final_list.append(tmp.copy())
            tmp = list()
            tmp.append(i.copy())
            trans_len += 1
    tmp_final_list.append(tmp.copy())
    final_list = tmp_final_list

    print(final_list)

    ans = list()
    print("@@@ 4層for loop @@@")
    for i in range(len(final_list)):
        for j in range(i+1, len(final_list)):
            for x in final_list[i]:
                for y in final_list[j]:
                    x_set, y_set = set(x[0]), set(y[0])
                    x_spt, y_spt, z = x[1], y[1], y[0]-x[0]
                    conf = y_spt/x_spt
                    total_trans_len = len(input_data)
                    if x_set.issubset(y_set) and conf >= min_conf:
                        for trans in final_list[len(z)-1]:
                            if z == trans[0]:
                                z_spt = trans[1]
                                break
                        ans.append(
                            [x_set,
                             set(z),
                             format(y_spt / total_trans_len, '.3f'),
                             format(conf, '.3f'),
                             format(y_spt/(x_spt*z_spt),'.3f')])
                        print(ans[-1])
    return ans
