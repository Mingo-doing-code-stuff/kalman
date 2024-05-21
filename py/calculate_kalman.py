import pandas as pd

# Read the CSV file
df = pd.read_csv('c_serial_port/data.csv', delimiter=';')

print(df.describe())
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

# Ensure the DataFrame has columns to process
if df.shape[1] == 0:
    print("The DataFrame has no columns to process.")
else:
    # Access columns by index and print the description safely
    for i in range(len(df.columns)):
        column_name = df.columns[i]
        column_data = df.iloc[:, i]
        # print(column_data.describe())

        print(f"> Axis {column_name}")
        print(f"[MEAN]:\t{column_data.mean()}")
        print(f"[VAR]:\t{column_data.var()}")
        print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
