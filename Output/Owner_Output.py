# Created by Dayu Wang (dwang@stchas.edu) on 2022-05-05

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-05-05


from Algorithms.Date import MONTHS
from csv import reader
from os import listdir
from os.path import isfile, join
from pandas import read_excel
from termcolor import colored
from xlsxwriter import Workbook


def main():
    # Open the original input file.
    raw_input_file = read_excel(
        io=r"../Raw_Input_File/final_ceo_list.xlsx",
        sheet_name="search"
    )
    raw_records = raw_input_file.values.tolist()

    # Open the output file.
    output_file = Workbook(r"./Output_Files/Output_File_-_Owners_-_XLSX.xlsx")
    worksheet = output_file.add_worksheet(name="Output_SVI_Index_of_CEOs")

    # Set output data formats.
    cell_format_header = output_file.add_format({
        "font_name": "Verdana",
        "font_size": 10,
        "font_color": "red",
        "bold": True,
        "italic": False,
        "underline": False,
        "align": "center",
        "valign": "vcenter",
        "border": 0
    })

    cell_format_data = output_file.add_format({
        "font_name": "Verdana",
        "font_size": 10,
        "font_color": "black",
        "bold": False,
        "italic": False,
        "underline": False,
        "align": "left",
        "valign": "vcenter",
        "border": 0
    })

    worksheet.write_row(
        row=0,
        col=0,
        data=["DATE", "OWNER", "SVI_INDEX", "TICKER", "CUSIP6",
              "CNAME", "GOOGLE_TRENDS_SEARCH_TERM", "GOOGLE_TRENDS_SUGGESTION"],
        cell_format=cell_format_header
    )

    worksheet.freeze_panes(1, 0)
    next_row = 1

    # Iterate through the files storing SVI index of CEOs.
    ceo_svi_dir = r"../Google_Trends_Data_Collection/Output_Files/Owner/Reliable"
    for filename in listdir(ceo_svi_dir):
        file = join(ceo_svi_dir, filename)
        if isfile(file):
            # Get the record number.
            record_num = int(filename[:5])

            # Get the owner, ticker, and cusip6 values from the original input file.
            raw_owner = raw_records[record_num - 2][1]
            raw_ticker = '' if str(raw_records[record_num - 2][2]).strip() == "nan" else raw_records[record_num - 2][2]
            raw_cusip6 = '' if str(raw_records[record_num - 2][3]).strip() == "nan" else raw_records[record_num - 2][3]
            raw_cname = raw_records[record_num - 2][4]

            # Open the csv file.
            csv_file = open(
                file=file,
                mode='r',
                newline='',
                errors="ignore"
            )
            csv = reader(csv_file)
            csv = list(csv)

            # Get Google Trends search term and Google Trends suggestions.
            google_trends_search_term = csv[2][1]
            google_trends_suggestion = csv[3][1]

            # Write the SVI data to the output file.
            for row in range(7, 226):
                year = str(csv[row][0])
                month = str(csv[row][1])
                svi = str(csv[row][2])
                date = fr"{MONTHS[month.lower()]}/1/{year}"

                worksheet.write_row(
                    row=next_row,
                    col=0,
                    data=[date, raw_owner, svi, raw_ticker, raw_cusip6, raw_cname,
                          google_trends_search_term, google_trends_suggestion],
                    cell_format=cell_format_data
                )
                next_row += 1

            csv_file.close()

            print(colored("Record %05d successfully exported!" % record_num, "green"))

    # Close the output file.
    output_file.close()


if __name__ == "__main__":
    main()
