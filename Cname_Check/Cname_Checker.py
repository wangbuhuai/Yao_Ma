# Created by Dayu Wang (dwang@stchas.edu) on 2022-05-06

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-05-06


from Google_Trends.Suggestions import match_company_suggestions
from pandas import read_excel
from pytrends.request import TrendReq
from termcolor import colored
from xlsxwriter import Workbook


def main():
    # Open the input file storing records.
    input_file = read_excel(
        io=r"../Output/Output_Files/Output_File_-_Owners_-_XLSX.xlsx",
        sheet_name="Output_SVI_Index_of_CEOs"
    )

    # Open the output file.
    output_file = Workbook(r"./Output_File/Cname_Checklist_-_XLSX.xlsx")
    worksheet = output_file.add_worksheet(name="Cname_Checklist")

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
        "border": 1,
        "border_color": "#D9D9D9"
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
        "border": 1,
        "border_color": "#D9D9D9"
    })

    cell_format_leftmost_column = output_file.add_format({
        "font_name": "Verdana",
        "font_size": 10,
        "font_color": "black",
        "bold": False,
        "italic": False,
        "underline": False,
        "align": "left",
        "valign": "vcenter",
        "border": 1,
        "bg_color": "#FFFF99",
        "border_color": "#D9D9D9"
    })

    cell_format_a1 = output_file.add_format({
        "font_name": "Verdana",
        "font_size": 10,
        "font_color": "red",
        "bold": True,
        "italic": False,
        "underline": False,
        "align": "center",
        "valign": "vcenter",
        "border": 1,
        "bg_color": "#FFFF99",
        "border_color": "#D9D9D9"
    })

    worksheet.write_string(
        row=0,
        col=0,
        string="ORIGINAL_CNAME",
        cell_format=cell_format_a1
    )

    worksheet.write_row(
        row=0,
        col=1,
        data=["SEARCH_TERM", "GOOGLE_TRENDS_TERM", "GOOGLE_TRENDS_SUGGESTION", "GOOGLE_TRENDS_URL"],
        cell_format=cell_format_header
    )

    worksheet.freeze_panes(1, 0)

    # Create a pytrends search engine.
    engine = TrendReq(
        hl="en-US",  # Language
        tz=360  # Timezone offset
    )

    # Create a set to store the processed cnames.
    cnames = set()

    found_count = 0
    not_found_count = 0

    for index, row in input_file.iterrows():
        cname = row["CNAME"]
        if cname in cnames:
            continue
        else:
            cnames.add(cname)

        sug_res = match_company_suggestions(engine, cname)

        worksheet.write_string(
            row=len(cnames),
            col=0,
            string=cname,
            cell_format=cell_format_leftmost_column
        )

        if sug_res is not None:
            worksheet.write_row(
                row=len(cnames),
                col=1,
                data=[sug_res["search"], sug_res["term"], sug_res["suggestion"], sug_res["url"]],
                cell_format=cell_format_data
            )
            print(colored(f"(%03d) \"{cname}\" found!" % len(cnames), "blue"))
            found_count += 1
        else:
            worksheet.write_row(
                row=len(cnames),
                col=1,
                data=['-', '-', '-', '-'],
                cell_format=cell_format_leftmost_column
            )
            print(colored(f"(%03d) \"{cname}\" not found!" % len(cnames), "red"))
            not_found_count += 1

    # Close the output file.
    output_file.close()

    print(f"Found: {found_count}")
    print(f"Not found: {not_found_count}")


if __name__ == "__main__":
    main()
