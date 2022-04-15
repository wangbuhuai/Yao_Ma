# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-15


from Google_Trends.Search import SearchEngine
from Input.Settings import INPUT_FILE
from pandas import DataFrame, concat, read_excel
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def main():
    # Ask the user to select the input Excel spreadsheet.
    Tk().withdraw()
    input_file = askopenfilename(
        title="Select the Excel spreadsheet:",
        filetypes=INPUT_FILE["Type"]
    )

    # Open the input Excel spreadsheet.
    input_file = read_excel(
        io=input_file,
        sheet_name=INPUT_FILE["Sheet"]
    )

    # Create a DataFrame to store the output values.
    output_data = DataFrame()

    # Create a Google Trends search engine.
    engine = SearchEngine()

    for value in input_file[INPUT_FILE["Column"]]:
        engine.set_term(value.strip())
        result = engine.search()
        if result is None:
            continue
        output_data = concat([output_data, result])

    output_data.to_excel("C:/Dayu_Wang/Temp/output.xlsx")


if __name__ == "__main__":
    main()
