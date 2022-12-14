import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# fake_dataset = [
#     ["f", "c", "a", "m", "p"],
#     ["f", "c", "a", "b", "m"],
#     ["f", "b"],
#     ["c", "b", "p"],
#     ["f", "c", "a", "m", "p"]
# ]

# fake_dataset = [
#     ["milk", "bread", "beer"],
#     ["bread", "coffee"],
#     ["bread", "egg"],
#     ["milk", "bread", "coffee"],
#     ["milk", "egg"],
#     ["bread", "egg"],
#     ["milk", "egg"],
#     ["milk", "bread", "egg", "beer"],
#     ["milk", "bread", "egg"],
# ]

# fake_dataset = [
#     ["A", "C", "D"],
#     ["B", "C", "E"],
#     ["A", "B", "C", "E"],
#     ["B", "E"]
# ]

# fake_dataset = [
#     [0, 2, 3],
#     [1, 2, 4],
#     [0, 1, 2, 4],
#     [1, 4]
# ]

# fake_dataset = convert_data("gen/output.data")


# 第一次掃描所有的1-freq itemset，並刪除小於min_sup
def create_one_freq_itemset(dataset, min_sup):
    list_of_itemset = list()
    weights = dict()
    for transaction in dataset:
        for item in transaction:
            if weights.get(item):
                weights[item] += 1
            else:
                weights[item] = 1
    # 刪小於min_sup
    for k, v in weights.items():
        if v >= min_sup:
            list_of_itemset.append([frozenset((k,)), v])
    return list_of_itemset


def scan(dataset, targets, min_sup):
    list_of_itemset = list()
    weights = dict()
    # 找出現次數
    for transaction in dataset:
        trans_set = set(transaction)
        for target in targets:
            if (target.issubset(trans_set)):
                if weights.get(target):
                    weights[target] += 1
                else:
                    weights[target] = 1
    # 刪小於min_sup
    for k, v in weights.items():
        if v >= min_sup:
            print(k, v)
            list_of_itemset.append([frozenset(k), v])
    return list_of_itemset


def itemset_union(dataset, list_of_itemset, min_sup, final_list):
    if len(list_of_itemset) <= 1:
        print("no freq itemset")
        return
    targets = set()
    current_freq = len(list_of_itemset[0][0])
    print(f"@@@ current_freq: {current_freq+1} @@@")
    # 組合1-freq itemset產生2-freq itemset
    for i in range(len(list_of_itemset)-1):
        for j in range(i+1, len(list_of_itemset)):
            k = list_of_itemset[i][0].union(list_of_itemset[j][0])  # 2-freq itemset
            if len(k) == current_freq+1 and k not in targets:
                targets.add(k)
    # scan並刪除<min_sup
    targets = list(targets)
    temp = scan(dataset, targets, min_sup)
    final_list.append(temp)
    itemset_union(dataset, temp, min_sup, final_list)


def apriori(input_data, args):
    min_sup = args.min_sup
    min_conf = args.min_conf
    fake_dataset = input_data
    min_sup = min_sup*len(fake_dataset)
    list_of_itemset = create_one_freq_itemset(fake_dataset, min_sup)
    print("first:", list_of_itemset)
    final_list = [list_of_itemset]
    itemset_union(fake_dataset, list_of_itemset, min_sup, final_list)

    # # pop 最後一個空集合
    # final_list.pop()

    print("@@@ final_list @@@")
    for i in final_list:
        print(len(i))
        print(i)

    ans = list()
    print("@@@ 4層for loop @@@")
    logging.info("apr "+str(len(final_list)))
    for i in range(len(final_list)):
        for j in range(i+1, len(final_list)):
            for x in final_list[i]:
                for y in final_list[j]:
                    x_set, y_set = x[0], y[0]
                    x_spt, y_spt, z = x[1], y[1], y[0]-x[0]
                    
                    conf = y_spt/x_spt
                    total_trans_len = len(input_data)
                    if x_set.issubset(y_set) and conf >= min_conf:
                        for trans in final_list[len(z)-1]:
                            if z == trans[0]:
                                z_spt = trans[1]
                                break
                        ans.append(
                            [str(set(x_set)).replace(",","").replace("\'",""),
                             str(set(z)).replace(",","").replace("\'",""),
                             format(y_spt / total_trans_len, '.3f'),
                             format(conf, '.3f'),
                             format(y_spt*total_trans_len/(x_spt*z_spt),'.3f')])
                        print(ans[-1])
    return ans
