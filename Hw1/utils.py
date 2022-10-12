import logging
import csv
import time
from pathlib import Path
from typing import Any, List, Union


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running {func.__name__} ...", end='\r')
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} Done in {end - start:.2f} seconds")
        return result
    return wrapper


@timer
def read_file(filename: Union[str, Path]) -> List[List[int]]:
    """read_file

    Args:
        filename (Union[str, Path]): The filename to read

    Returns:
        List[List[int]]: The data in the file
    """
    # return [
    #     [int(x) for x in line.split()]
    #     for line in Path(filename).read_text().splitlines()
    # ]
    with open(filename) as in_f:
        data = in_f.readlines()
    with open("converted_from_.data.txt", "w") as out_f:
        out_f.writelines([','.join(d.split())+'\n' for d in data])
    with open("converted_from_.data.txt", "r") as f:
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


@timer
def write_file(data: List[List[Any]], filename: Union[str, Path]) -> None:
    """write_file writes the data to a csv file and
    adds a header row with `relationship`, `support`, `confidence`, `lift`.

    Args:
        data (List[List[Any]]): The data to write to the file
        filename (Union[str, Path]): The filename to write to
    """
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["relationship", "support", "confidence", "lift"])
        writer.writerows(data)


def setup_logger():
    l = logging.getLogger('l')

    log_dir: Path = Path(__file__).parent / "logs"

    # create log directory if not exists
    log_dir.mkdir(parents=True, exist_ok=True)

    # set log file name
    log_file_name = f"{time.strftime('%Y%m%d_%H%M%S')}.log"

    l.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(
        filename=log_dir / log_file_name,
        mode='w'
    )
    streamHandler = logging.StreamHandler()

    allFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s"
    )

    fileHandler.setFormatter(allFormatter)
    fileHandler.setLevel(logging.INFO)

    streamHandler.setFormatter(allFormatter)
    streamHandler.setLevel(logging.INFO)

    l.addHandler(streamHandler)
    l.addHandler(fileHandler)

    return l


l = setup_logger()
