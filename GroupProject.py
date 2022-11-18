from address_convert import convertBinaryToDecimal, convertHexToBinary
import numpy as np
import pandas as pd
import predictors
from tqdm import tqdm

file_names = ["gcc-short.br.txt",
              "art.br.txt",
              "sjeng.br.txt",
              "sphinx3.br.txt",
              "mcf.br.txt"]
# file_names = ["gcc-short.br.txt"]
column_names = ["instruction_address",
                "taken_or_not",
                "target_address",
                "instruction_name"]
output_columns = ["file name",
                  "total branches",
                  "taken", "not taken",
                  "taken percent",
                  "not taken percent",
                  "distinct branches"]
output_array = pd.DataFrame(columns=output_columns)

output_columns2 = ["file name",
                  "total branches",
                  "1-b # mispredictions", "1-b misprediction rate",
                  "2-b # mispredictions", "2-b misprediction rate",
                  "3-b # mispredictions", "3-b misprediction rate"]
output_array2 = pd.DataFrame(columns=output_columns2)



for file_name in file_names:

    print("Opening new file... " + file_name)
    df = pd.read_csv(file_name, header=None, names=column_names, sep=" ")
    print("Creating Bit Predictor Tables...", end=' ')
    one_bit = [predictors.OneBitPredictor('NT') for i in range(1024)]
    two_bit = [predictors.TwoBitPredictor('NT') for i in range(1024)]
    three_bit = [predictors.ThreeBitPredictor('NT') for i in range(1024)]
    print("Done!")

    print("Iterrating branches... ", end=' ', flush=True)
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        # print(row['instruction_address'], row['taken_or_not'])
        if row['taken_or_not'] == 'T':
            # print(row[0] + "  " + convertHexToBinary(row[0]))
            binAddr = convertHexToBinary(row[0])[-10:]
            tableAddr = convertBinaryToDecimal(binAddr)
            one_bit[tableAddr].taken()
            two_bit[tableAddr].taken()
            three_bit[tableAddr].taken()
        else:
            one_bit[tableAddr].not_taken()
            two_bit[tableAddr].not_taken()
            three_bit[tableAddr].not_taken()
    
    total1b = 0
    incorr1b = 0
    total2b = 0
    incorr2b = 0
    total3b = 0
    incorr3b = 0

    for i in range(len(one_bit)):
        total1b += one_bit[i].total
        incorr1b += one_bit[i].incorrect
        total2b += two_bit[i].total
        incorr2b += two_bit[i].incorrect
        total3b += three_bit[i].total
        incorr3b += three_bit[i].incorrect

    print("Done!")
    print("Results: ")
    print("1b:", end=' ')
    print(incorr1b / total1b)
    print("2b:", end=' ')
    print(incorr2b / total2b)
    print("3b:", end=' ')
    print(incorr3b / total3b)
    print("Saving results to csv...")
    new_row = [file_name, total1b, incorr1b, incorr1b / total1b, incorr2b, incorr2b / total2b, incorr2b, incorr3b / total3b]
    output_array2.loc[len(output_array2.index)] = new_row
    
    # TASK 1

    # print("dataframe shape")
    # print(df.shape)

    # total_branches = df.shape[0]
    # print("total branches ", total_branches)

    # print("dataframe unique entries")
    # uniques = df.nunique()
    # print(uniques)

    # distinct_branches = uniques[0]
    # print("distinct branches ", distinct_branches)

    # results = df["taken_or_not"].value_counts()
    # print(results)

    # taken = results[0]
    # print("taken ", taken)

    # not_taken = results[1]
    # print("not taken ", not_taken)

    # taken_percent = 100 * (taken / (taken + not_taken))
    # print("taken % ", taken_percent)

    # not_taken_percent = 100 * (not_taken / (taken + not_taken))
    # print("not taken % ", not_taken_percent)

    # new_row = [file_name, total_branches, taken, not_taken, taken_percent, not_taken_percent, distinct_branches]
    # print(new_row)

    # output_array.loc[len(output_array.index)] = new_row

output_array2 = output_array2.set_index("file name")
# print(output_array2)
pd.DataFrame(output_array2).to_csv("branch_prediction_summary_task3.csv")