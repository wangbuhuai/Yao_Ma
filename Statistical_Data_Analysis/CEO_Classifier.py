# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-19

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-19


from Google_Trends.Search import SearchEngine
from Google_Trends.Search_Term import Record
from Google_Trends.Suggestion import match_suggestions
from Input.Settings import INPUT_FILE
from pandas import DataFrame, read_excel
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

    # Create a Google Trends search engine.
    engine = SearchEngine()

    # Create dictionaries to store the results.
    results = [{}, {}, {}, {}]
    for i in range(len(results)):
        for col in INPUT_FILE["Columns"]:
            results[i]["NUMBER"] = []
            results[i][col] = []

    for index, row in input_file.iterrows():
        search_term = Record(index + 2, row["OWNER"], row["TICKER"], row["CUSIP6"], row["CNAME"])
        engine.set_term(search_term.get_owner())

        if match_suggestions(engine.get_req(), search_term.get_owner()) is not None:
            engine.turn_on_suggestions()
            search_result = engine.search()
            if search_result is not None:
                results[0]["NUMBER"].append(search_term.get_row())
                results[0]["OWNER"].append(search_term.get_owner())
                results[0]["TICKER"].append(search_term.get_ticker())
                results[0]["CUSIP6"].append(search_term.get_cusip6())
                results[0]["CNAME"].append(search_term.get_cname())
            else:
                results[1]["NUMBER"].append(search_term.get_row())
                results[1]["OWNER"].append(search_term.get_owner())
                results[1]["TICKER"].append(search_term.get_ticker())
                results[1]["CUSIP6"].append(search_term.get_cusip6())
                results[1]["CNAME"].append(search_term.get_cname())
        else:
            engine.turn_off_suggestions()
            search_result = engine.search()
            if search_result is not None:
                results[2]["NUMBER"].append(search_term.get_row())
                results[2]["OWNER"].append(search_term.get_owner())
                results[2]["TICKER"].append(search_term.get_ticker())
                results[2]["CUSIP6"].append(search_term.get_cusip6())
                results[2]["CNAME"].append(search_term.get_cname())
            else:
                results[3]["NUMBER"].append(search_term.get_row())
                results[3]["OWNER"].append(search_term.get_owner())
                results[3]["TICKER"].append(search_term.get_ticker())
                results[3]["CUSIP6"].append(search_term.get_cusip6())
                results[3]["CNAME"].append(search_term.get_cname())

        print(search_term)

    for i in range(len(results)):
        DataFrame(data=results[i]).to_csv(f"./Output_Files/Class_{i}.csv", errors="ignore", index=False)


if __name__ == "__main__":
    main()
