import pandas as pd
from teams import extract_teams, get_teams
import os
# csv file containing list of students and their teams
teams_file = "teams.csv"
output_marks = "marks_master.xlsx"
template_tex = "../templates/template.tex"

totmarks = 10


def extract_data(fname):
    df = pd.read_excel(fname)
    df.set_index("NAME:", inplace=True)
    df = df[df.index.notnull()]
    return df


def writedata(df, stud_list):
    for name in stud_list:
        opname = name[1]+".xlsx"
        df_ = df[name[0]].copy()
        df_.columns = ['' for _ in range(len(df_.columns))]

        df_.to_excel(opname)


teamlist = extract_teams(teams_file)
stud_names = get_teams(teams_file)

for team in teamlist:
    try:
        stud_list = stud_names[team]
    except KeyError:
        stud_list = False
        pass

    if stud_list:
        fulldf = pd.DataFrame()
        for name in stud_list:
            fname = name[0].replace(" ", "_")+"_"+name[1]+".xlsx"
            if os.path.isfile(fname):
                tmpdf = extract_data(fname)
                fulldf = pd.concat([fulldf, tmpdf], axis=1)

        writedata(fulldf, stud_list)
