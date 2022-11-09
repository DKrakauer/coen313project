import numpy as np
import pandas as pd
import predictors


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

    df = pd.read_csv(file_name, header=None, names=column_names, sep=" ")
    one_bit = predictors.OneBitPredictor('NT')
    two_bit = predictors.TwoBitPredictor('NT')
    three_bit = predictors.ThreeBitPredictor('NT')

    for index, row in df.iterrows():
        # print(row['instruction_address'], row['taken_or_not'])
        if row['taken_or_not'] == 'T':
            one_bit.taken()
            two_bit.taken()
            three_bit.taken()
        else:
            one_bit.not_taken()
            two_bit.not_taken()
            three_bit.not_taken()

    print(one_bit.incorrect / one_bit.total)
    print(two_bit.incorrect / two_bit.total)
    print(three_bit.incorrect / three_bit.total)
    print(one_bit.total)
    print(two_bit.total)
    print(three_bit.total)

    new_row = [file_name, one_bit.total, one_bit.incorrect, one_bit.incorrect / one_bit.total, two_bit.incorrect, two_bit.incorrect / two_bit.total, three_bit.incorrect, three_bit.incorrect / three_bit.total]
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

print(output_array2)
pd.DataFrame(output_array2).to_csv("branch_prediction_summary_task3.csv")