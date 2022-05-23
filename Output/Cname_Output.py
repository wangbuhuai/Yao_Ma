# Created by Dayu Wang (dwang@stchas.edu) on 2022-05-23

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-05-23


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
        io=r"../Raw_Input_File/Cname_Results_-_XLSX.xlsx"
    )
    raw_records = raw_input_file.values.tolist()

    # Open the output file.
    output_file = Workbook(r"./Output_Files/Output_File_-_Cnames_-_XLSX.xlsx")
    worksheet = output_file.add_worksheet(name="Output_SVI_Index_of_Cnames")

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
        data=["RECORD_NUMBER", "DATE", "ORIGINAL_CNAME", "SVI_INDEX"],
        cell_format=cell_format_header
    )

    worksheet.freeze_panes(1, 0)
    next_row = 1

    # Iterate through the files storing SVI index of CEOs.
    cname_svi_dir = r"../Google_Trends_Data_Collection/Output_Files/Cname/Reliable"
    for filename in listdir(cname_svi_dir):
        file = join(cname_svi_dir, filename)
        if isfile(file):
            # Get the record number.
            record_num = int(filename[:3])

            # Get the cname from original input file.
            raw_cname = raw_records[record_num - 2][0]

            # Open the csv file.
            csv_file = open(
                file=file,
                mode='r',
                newline='',
                errors="ignore"
            )
            csv = reader(csv_file)
            csv = list(csv)

            # Write the SVI data to the output file.
            for row in range(5, 224):
                year = str(csv[row][0])
                month = str(csv[row][1])
                svi = str(csv[row][2])
                date = fr"{MONTHS[month.lower()]}/1/{year}"

                worksheet.write_row(
                    row=next_row,
                    col=0,
                    data=[record_num, date, raw_cname, svi],
                    cell_format=cell_format_data
                )
                next_row += 1

            csv_file.close()

            print(colored("Record %03d successfully exported!" % record_num, "green"))

    # Close the output file.
    output_file.close()


if __name__ == "__main__":
    main()
