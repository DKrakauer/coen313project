import pandas as pd
import math

# Correlating predictor (global) (5,1) predictor with 5 bits of address
# Correlating predictor (local)  (5,1) (5 bits of address every address pattern has its own shift register


class SaturatedCounter:
    def __init__(self, low, high):
        self.high = high
        self.low = low
        self.count = math.floor((high - low) / 2)

    def inc(self):
        if self.count < self.high:
            self.count += 1

    def dec(self):
        if self.count > self.low:
            self.count -= 1


class nBitPredictor:
    def __init__(self, n=1):
        self.n = n
        self.counter_max = pow(2, n) - 1
        self.decision_boundary = (self.counter_max + 1) / 2
        self.address_dict = {}
        self.predict = 'NT'
        self.correct = 0
        self.incorrect = 0
        self.total = 0

    def generate_prediction(self, address):
        if address not in self.address_dict.keys():
            self.address_dict[address] = SaturatedCounter(0, self.counter_max)
        if self.address_dict[address].count < self.decision_boundary:
            return 'NT'
        else:
            return 'T'

    def taken(self, address=''):
        self.total += 1
        if self.generate_prediction(address) == 'T':
            self.correct += 1
        else:
            self.incorrect += 1

        self.address_dict[address].inc()

    def not_taken(self, address=''):
        self.total += 1
        if self.generate_prediction(address) == 'NT':
            self.correct += 1
        else:
            self.incorrect += 1

        self.address_dict[address].dec()


def hex_to_last_5(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(5)[-5:]


def run(debug=1):
    if debug == 2:
        file_names = ["gcc-short.br.txt",
                      "art.br.txt"]
    elif debug == 1:
        file_names = ["gcc-short.br.txt"]
    elif debug == 0:
        file_names = ["gcc-short.br.txt",
                      "art.br.txt",
                      "sjeng.br.txt",
                      "sphinx3.br.txt",
                      "mcf.br.txt"]
    column_names = ["instruction_address",
                    "taken_or_not",
                    "target_address",
                    "instruction_name"]

    output_columns = ["file name",
                      "total branches",
                      "global mispredictions", "global misprediction rate",
                      "local mispredictions", "local misprediction rate"]
    output_array = pd.DataFrame(columns=output_columns)

    for file_name in file_names:
        print("\nstarting " + str(file_name))
        df = pd.read_csv(file_name, header=None, names=column_names, sep=" ")
        global_5_1 = nBitPredictor(n=5)
        global_history = 'NNNNN'
        local_5_1 = nBitPredictor(n=5)

        for index, row in df.iterrows():
            if row['taken_or_not'] == 'T':
                global_5_1.taken(address=global_history)
                global_history = global_history[1:] + 'T'
                local_5_1.taken(hex_to_last_5(row['instruction_address']))
            else:
                global_5_1.not_taken(address=global_history)
                global_history = global_history[1:] + 'N'
                local_5_1.not_taken(hex_to_last_5(row['instruction_address']))

        print("\nglobal stats")
        print(global_5_1.incorrect / global_5_1.total)
        print(global_5_1.total)

        print("\nlocal stats")
        print(local_5_1.incorrect / local_5_1.total)
        print(local_5_1.total)

        new_row = [file_name, global_5_1.total,
                   global_5_1.incorrect, global_5_1.incorrect / global_5_1.total,
                   local_5_1.incorrect, local_5_1.incorrect / local_5_1.total]
        output_array.loc[len(output_array.index)] = new_row

    output_array = output_array.set_index("file name")

    print(output_array)
    pd.DataFrame(output_array).to_csv("branch_prediction_summary_task_4.csv")


run(debug=0)
