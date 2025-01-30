import pandas as pd
from teams import extract_teams, get_teams
from glob import glob
import os
import numpy as np


# csv file containing list of students and their teams
ass = "Project 3 peer assessment (147404)"
teams_file = "teams.csv"
output_marks = "marks_master.xlsx"
template_tex = "../templates/template.tex"

totmarks = 100
namelist = []
marklist = []


def extract_data(fname):
    df = pd.read_excel(fname)
    df.drop_duplicates(subset="NAME:", inplace=True)
    df.set_index("NAME:", inplace=True)
    df = df[df.index.notnull()]
    return df


def writedata(df, stud_list):
    for name in stud_list:
        lname = name[0].split()[1]+name[0].split()[0]
        lname = lname.replace("'","")
        fnamelist = glob(f"{lname.lower()}*")
        if (fnamelist):
            fname = fnamelist[0]
            opname = f"feedback/{fname}"
            df_ = df[name[0]].copy()
            df_.columns = ['' for _ in range(len(df_.columns))]

            df_.to_excel(opname)
            lastname = name[0].split()[1]
            firstname = name[0].split()[0]
            namelist.append(f'{lastname}, {firstname}') 
            marklist.append(f'{np.round(10*np.average(df_.iloc[[len(df_)-1]]),0)}')


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
            lname = name[0].split()[1]+name[0].split()[0]
            lname = lname.replace("'","")
            print(lname)
            fnamelist = glob(f"{lname.lower()}*")
            if (fnamelist):
                fname = fnamelist[0]
#            print(fname)
#            fname = name[0].replace(" ", "_")+"_"+name[1]+".xlsx"
                if os.path.isfile(fname):
                    tmpdf = extract_data(fname)
                    fulldf = pd.concat([fulldf, tmpdf], axis=1)
            else: 
                print(name)

        writedata(fulldf, stud_list)

opdf = pd.DataFrame()
opdf["Name"] = namelist
opdf["Mark"] = marklist

gradebook = pd.read_csv("gradebook.csv")
gradebook.set_index("Student",inplace=True)
opdf.set_index("Name",inplace=True)

print(opdf)
gradebook[ass] = opdf["Mark"]
            
gradebook.to_csv("marking.csv",index=True)
