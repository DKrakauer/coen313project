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
# file_names = ["art.br.txt"]
column_names = ["instruction_address",
                "taken_or_not",
                "target_address",
                "instruction_name"]
output_columns2 = ["file name",
                  "Total Branches",
                  "Misprediction Rate", "# of Mispredictions"]
output_array2 = pd.DataFrame(columns=output_columns2)

for file_name in file_names:

    print("Opening new file... " + file_name)
    df = pd.read_csv(file_name, header=None, names=column_names, sep=" ")

    print("Creating Bit Predictor Tables...")
    tables = []
    for i in range(8):
        tables.append([predictors.nBitPredictor('NT',i) for j in range(1024)])
    print("Done!")

    print("Iterrating branches... ")
    total = 0
    correct = 0
    incorrect = 0
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        # print(row['instruction_address'], row['taken_or_not'])
        # print(row[0] + "  " + convertHexToBinary(row[0]))
        binAddr = convertHexToBinary(row[0])[-10:]
        tableAddr = convertBinaryToDecimal(binAddr)
        
        total += 1
        sum = 0
        if row['taken_or_not'] == 'T':
            for i in range(8):
                if tables[i][tableAddr].predict == 'T':
                    sum += 1
                tables[i][tableAddr].taken()
            if sum > 4:
                correct += 1
            else:
                incorrect += 1
        else:
            for i in range(8):
                if tables[i][tableAddr].predict == 'T':
                    sum += 1
                tables[i][tableAddr].not_taken()
            if sum < 5:
                correct += 1
            else:
                incorrect += 1
    print("Done!")
    new_row = [file_name, total, incorrect/total, incorrect]
    output_array2.loc[len(output_array2.index)] = new_row

output_array2 = output_array2.set_index("file name")
pd.DataFrame(output_array2).to_csv("task5_output.csv")