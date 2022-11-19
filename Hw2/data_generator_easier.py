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
        tsai = [0, 1]
        self.high_flour = round(random.uniform(100, 180), 2)
        self.low_flour = round(random.uniform(60, 140), 2)
        self.warm_water = round(random.uniform(100, 180), 2)
        self.sugar = round(random.uniform(4, 10), 2)
        self.yeast = round(random.uniform(2, 7), 2)  # 酵母粉
        self.salt = round(random.uniform(2, 5), 2)
        self.olive_oil = round(random.uniform(10, 20), 2)
        self.standstill = round(random.uniform(30, 60), 2)
        self.temp = round(random.uniform(210, 230), 2)
        self.bake_time = round(random.uniform(10, 12), 2)
        # evil
        self.extra_effort = random.choices(is_add, weights=[90, 10])[0]
        self.pineapple = random.choices(is_add, weights=[10, 90])[0]
        self.pearl = random.choices(is_add, weights=[10, 90])[0]
        # non-relevent
        self.elec_power = random.choices(tsai, weights=[5, 95])[0]
        self.cooker_age = random.randint(12, 100)
        self.cooker_gender = random.randint(0, 1)
        # label
        mutation = random.randint(0, 2999)
        if mutation != 0:
            self.label = 1
        else:
            self.label = 0

    def bad_pizza(self):
        is_add = [True, False]
        tsai = [0, 1]
        self.high_flour = round(random.uniform(-400, 680), 2)
        # while self.high_flour >= 100 and self.high_flour <= 180:
        #     self.high_flour = round(random.uniform(-400, 680), 2)

        self.low_flour = round(random.uniform(-440, 640), 2)
        # while self.low_flour >= 60 and self.low_flour <= 140:
        #     self.low_flour = round(random.uniform(-440, 640), 2)

        self.warm_water = round(random.uniform(-400, 680), 2)
        # while self.warm_water >= 100 and self.warm_water <= 180:
        #     self.warm_water = round(random.uniform(-400, 680), 2)

        self.sugar = round(random.uniform(-96, 110), 2)
        # while self.sugar >= 4 and self.sugar <= 10:
        #     self.sugar = round(random.uniform(-96, 110), 2)

        self.yeast = round(random.uniform(-98, 107), 2)  # 酵母粉
        # while self.yeast >= 2 and self.yeast <= 7:
        #     self.yeast = round(random.uniform(-98, 107), 2)

        self.salt = round(random.uniform(-98, 105), 2)
        # while self.salt >= 2 and self.salt <= 5:
        #     self.salt = round(random.uniform(-98, 105), 2)

        self.olive_oil = round(random.uniform(-90, 120), 2)
        # while self.olive_oil >= 10 and self.olive_oil <= 20:
        #     self.olive_oil = round(random.uniform(-90, 120), 2)

        self.standstill = round(random.uniform(-70, 160), 2)
        # while self.standstill >= 30 and self.standstill <= 60:
        #     self.standstill = round(random.uniform(-70, 160), 2)

        self.temp = round(random.uniform(-290, 730), 2)
        # while self.temp >= 210 and self.temp <= 230:
        #     self.temp = round(random.uniform(-290, 730), 2)

        
        self.bake_time = round(random.uniform(-90, 112), 2)
        # while self.bake_time >= 10 and self.bake_time <= 12:
        #     self.bake_time = round(random.uniform(-90, 112), 2)
        # evil
        self.extra_effort = random.choices(is_add, weights=[10, 90])[0]
        self.pineapple = random.choices(is_add, weights=[90, 10])[0]
        self.pearl = random.choices(is_add, weights=[90, 10])[0]
        # non-relevent
        self.elec_power = random.choices(tsai, weights=[95, 5])[0]
        self.cooker_age = random.randint(12, 100)
        self.cooker_gender = random.randint(0, 1)
        # label
        mutation = random.randint(0, 2999)
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