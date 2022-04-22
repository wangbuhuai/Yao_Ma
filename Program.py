# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-21


from Google_Trends.Search import SearchEngine
from Input.Settings import INPUT_FILE
from pandas import read_excel
from tkinter import Tk
from tkinter.filedialog import askopenfilename


LOW = 4628
HIGH = 20001


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

    # Create a Google Trends search engine.
    engine = SearchEngine()

    for index, value in enumerate(input_file[INPUT_FILE["Columns"][0]]):
        if index + 2 < LOW:
            continue
        if index + 2 > HIGH:
            break

        engine.set_term(value.strip())
        result = engine.search()
        if result is not None:
            result[0].insert(
                loc=0,
                column="Row Number",
                value=f"{index + 2}"
            )

            # Write the result to a CSV file.
            path = r"./Output_Files/Google_Trends/" + ("Reliable" if result[1] else "Unreliable") + '/'
            filename = ("%05d" % (index + 2)) + ('' if result[1] else '!') + " - " + engine.get_term() + " (CEO)"
            extension = "csv"
            result[0].to_csv(
                (path + filename + " - " + extension.upper() + '.' + extension).replace(' ', '_'),
                errors="ignore",
                index=True
            )

            print("File \"" + filename + " - " + extension.upper() + '.' + extension + "\" Created!")


if __name__ == "__main__":
    main()
