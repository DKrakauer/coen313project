import numpy as np
import pandas as pd


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
                  "taken", "not taken",
                  "taken percent",
                  "not taken percent",
                  "distinct branches"]
output_array = pd.DataFrame(columns=output_columns)

for file_name in file_names:
    df = pd.read_csv(file_name, header=None, names=column_names, sep=" ")

    print("dataframe shape")
    print(df.shape)

    total_branches = df.shape[0]
    print("total branches ", total_branches)

    print("dataframe unique entries")
    uniques = df.nunique()
    print(uniques)

    distinct_branches = uniques[0]
    print("distinct branches ", distinct_branches)

    results = df["taken_or_not"].value_counts()
    print(results)

    taken = results[0]
    print("taken ", taken)

    not_taken = results[1]
    print("not taken ", not_taken)

    taken_percent = 100 * (taken / (taken + not_taken))
    print("taken % ", taken_percent)

    not_taken_percent = 100 * (not_taken / (taken + not_taken))
    print("not taken % ", not_taken_percent)

    new_row = [file_name, total_branches, taken, not_taken, taken_percent, not_taken_percent, distinct_branches]
    print(new_row)

    output_array.loc[len(output_array.index)] = new_row

output_array = output_array.set_index("file name")

print(output_array)
pd.DataFrame(output_array).to_csv("branch_prediction_summary.csv")