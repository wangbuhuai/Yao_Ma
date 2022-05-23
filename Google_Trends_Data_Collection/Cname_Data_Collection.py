# Created by Dayu Wang (dwang@stchas.edu) on 2022-05-23

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-05-23


from Google_Trends.Search import SearchEngine
from pandas import read_excel
from termcolor import colored


def main():
    # Open the input Excel file.
    input_file = read_excel(
        io=r"../Raw_Input_File/Cname_Results_-_XLSX.xlsx"
    )

    # Output file directory
    output_dir = r"./Output_Files/Cname/Reliable/"

    for row_num, row in input_file.iterrows():
        # Get the Cname record.
        record_num = row_num + 2
        cname = str(row["ORIGINAL_CNAME"])
        search_term = str(row["GOOGLE_TRENDS_TERM"]).lower().strip()
        suggestion = str(row["GOOGLE_TRENDS_SUGGESTION"]).lower().strip()
        url = str(row["GOOGLE_TRENDS_URL"])

        engine = SearchEngine()
        color = "green"

        if url is None or len(url) == 0 or url[0] != '/':
            url = engine.get_cname_url(search_term, suggestion)
            color = "blue"

        if url is None:
            raise ValueError

        result = engine.search_cname(url)

        if result is None:
            print(colored("%03d - %s - No Data!" % (record_num, cname), "red"))
            continue

        # Store the result to an output file.
        output_file = open(
            file=output_dir + "%03d_-_Cname_-_SVI_Data_-_CSV.csv" % record_num,
            mode='w',
            errors="ignore"
        )

        # Write the header rows.
        output_file.write(f"CNAME:,{cname}\n")
        output_file.write(f"Google Trends Search Term:,{search_term}\n")
        output_file.write(f"Google Trends Suggestion:,{suggestion}\n")
        output_file.write(f"Google Trends URL:,{url}\n")

        # Write the SVI data.
        output_file.write(result)

        # Close the file.
        output_file.close()

        # Print a message in the console.
        print(colored("%03d - %s - Data Collected!" % (record_num, cname), color))


if __name__ == "__main__":
    main()
