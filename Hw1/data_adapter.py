DATASET_PATH = "dataset.txt"


def convert_data(filename):
    with open(filename) as in_f:
        data = in_f.readlines()
    with open(DATASET_PATH, "w") as out_f:
        out_f.writelines([','.join(d.split())+'\n' for d in data])
    with open(DATASET_PATH, "r") as f:
        data = f.readlines()
        last_trans = 1
        final_data_list = list()
        temp_list = list()
        for d in data:
            row = d.split(',')
            if int(row[1]) == last_trans:
                temp_list.append(row[2].replace('\n', ''))
            else:
                final_data_list.append(temp_list.copy())
                temp_list.clear()
                temp_list.append(row[2].replace('\n', ''))
                last_trans += 1
        final_data_list.append(temp_list.copy())
        print(final_data_list)
        return final_data_list


def export_data(dataset, filename):
    pass


if __name__ == "__main__":
    convert_data("gen/output.data")
