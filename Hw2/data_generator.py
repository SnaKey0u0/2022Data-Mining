import random
import csv


class pizza():
    def __init__(self):
        choice = random.randint(0, 1)
        if choice == 0:
            self.good_pizza()
        else:
            self.bad_pizza()
        pass

    def good_pizza(self):
        is_add = [True, False]
        self.high_flour = round(random.uniform(130, 150), 2)
        self.low_flour = round(random.uniform(90, 110), 2)
        self.warm_water = round(random.uniform(130, 150), 2)
        self.sugar = round(random.uniform(5, 7), 2)
        self.yeast = round(random.uniform(4, 6), 2)  # 酵母粉
        self.olive_oil = round(random.uniform(5, 25), 2)
        self.salt = round(random.uniform(2, 4), 2)
        self.standstill = round(random.uniform(20, 40), 2)
        self.temp = round(random.uniform(210, 230), 2)
        self.bake_time = round(random.uniform(9, 13), 2)
        # evil
        self.extra_effort = random.choices(is_add, weights=[90, 10])[0]
        self.pineapple = random.choices(is_add, weights=[10, 90])[0]
        self.pearl = random.choices(is_add, weights=[10, 90])[0]
        # non-relevant
        self.elec_power = random.randint(0, 1)
        self.cooker_age = random.randint(18, 100)
        self.cooker_gender = random.randint(0, 1)
        # label
        mutation = random.randint(0, 2)
        if mutation != 0:
            self.label = 1
        else:
            self.label = 0

    def bad_pizza(self):
        is_add = [True, False]
        self.high_flour = round(random.uniform(30, 250), 2)
        while self.high_flour >= 130 and self.high_flour <= 150:
            self.high_flour = round(random.uniform(30, 250), 2)

        self.low_flour = round(random.uniform(-10, 210), 2)
        while self.low_flour >= 90 and self.low_flour <= 110:
            self.low_flour = round(random.uniform(-10, 210), 2)

        self.warm_water = round(random.uniform(30, 250), 2)
        while self.warm_water >= 130 and self.warm_water <= 150:
            self.warm_water = round(random.uniform(30, 250), 2)

        self.sugar = round(random.uniform(-5, 17), 2)
        while self.sugar >= 5 and self.sugar <= 7:
            self.sugar = round(random.uniform(-5, 17), 2)

        self.yeast = round(random.uniform(-6, 16), 2)  # 酵母粉
        while self.yeast >= 4 and self.yeast <= 6:
            self.yeast = round(random.uniform(-6, 16), 2)

        self.olive_oil = round(random.uniform(-5, 35), 2)
        while self.olive_oil >= 5 and self.olive_oil <= 25:
            self.olive_oil = round(random.uniform(-5, 35), 2)

        self.salt = round(random.uniform(-8, 14), 2)
        while self.salt >= 2 and self.salt <= 4:
            self.salt = round(random.uniform(-8, 14), 2)

        self.standstill = round(random.uniform(10, 50), 2)
        while self.standstill >= 20 and self.standstill <= 40:
            self.standstill = round(random.uniform(10, 50), 2)

        self.temp = round(random.uniform(110, 330), 2)
        while self.temp >= 210 and self.temp <= 230:
            self.temp = round(random.uniform(110, 330), 2)

        self.bake_time = round(random.uniform(-1, 23), 2)
        while self.bake_time >= 9 and self.bake_time <= 13:
            self.bake_time = round(random.uniform(-1, 23), 2)
        # evil
        self.extra_effort = random.choices(is_add, weights=[10, 90])[0]
        self.pineapple = random.choices(is_add, weights=[90, 10])[0]
        self.pearl = random.choices(is_add, weights=[90, 10])[0]
        # non-relevent
        self.elec_power = random.randint(0, 1)
        self.cooker_age = random.randint(18, 100)
        self.cooker_gender = random.randint(0, 1)
        # label
        mutation = random.randint(0, 2)
        if mutation != 0:
            self.label = 0
        else:
            self.label = 1

    def __str__(self):
        return str(self.label)


pizzas = list()
pizzas_test = list()

for i in range(6666):
    my_pizza = pizza()
    pizzas.append(my_pizza)

for i in range(3333):
    my_pizza = pizza()
    pizzas_test.append(my_pizza)

with open('mydata.csv', 'w', encoding='utf-8') as f:
    json_data = [vars(p) for p in pizzas]
    wr = csv.DictWriter(f, fieldnames=json_data[0].keys(), delimiter=',', lineterminator='\n')
    wr.writeheader()
    wr.writerows(json_data)

with open('mydata_test.csv', 'w', encoding='utf-8') as f:
    json_data = [vars(p) for p in pizzas_test]
    wr = csv.DictWriter(f, fieldnames=json_data[0].keys(), delimiter=',', lineterminator='\n')
    wr.writeheader()
    wr.writerows(json_data)
