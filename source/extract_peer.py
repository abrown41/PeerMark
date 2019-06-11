################################################################################
teams_file           = "teams.csv"            # csv file containing list of students and their teams
output_marks         = "marks_master.xlsx"
template_tex         = "../../templates/template.tex"

generate_feedback = True
pdfoutput = False
totmarks = 10

################################################################################

import os
from teams import *


def extract_data(fname,numteam):
    import xlrd
    wb = xlrd.open_workbook(fname)
    sh = wb.sheet_by_name('peer_review')
    scores=[]
    tscore=[]

    for colnum in range(1,numteam+1):
        indscore=[]
        for rownum in list(range(1,8)) + [9,12]:
            indscore.append(sh.row_values(rownum)[colnum])
        scores.append(indscore)
        tscore.append(indscore[-1])

    scores.sort(key=lambda x: x[0])
    return scores

def writescores(scores,opf):
    opf.write("**Peer evaluation scores for "+ str(scores[0]).strip() +"**\n\n")
    opf.write("* Attendance at group meetings: " + str(scores[1])+"\n")
    opf.write("* Contribution to meetings: " + str(scores[2])+"\n")
    opf.write("* Contribution outside meetings: " + str(scores[3])+"\n")
    opf.write("* Idea suggesting: " + str(scores[4])+"\n")
    opf.write("* Extracting useful knowledge: " + str(scores[5])+"\n")
    opf.write("* Encouraging participation: " + str(scores[6])+"\n")

    opf.write("\n")

    if str(scores[7]).strip() != '':
        opf.write("**Comments:** \n'")
        opf.write(str(scores[7]).strip()+"'\n\n")
    opf.write("**Overall score:** "+ str(scores[8]))
    opf.write("\n\n")
    opf.write("---\n\n")

def samename(name1,name2):
    if name1==name2:
        return True
    else:
        return False


def writedata(scores,stud_list):
    for item in scores:
        for name in stud_list:
            opname=name[1]
            opf=open(opname+'.md','a')
            if samename(item[0],name[0]):
                writescores(item,opf)
            opf.close()

teamlist = extract_teams(teams_file)
stud_names= get_teams(teams_file)

for team in teamlist:
    try:
        stud_list=stud_names[team]
        num_in_team=len(stud_list)
    except:
        stud_list = False
        pass

    if stud_list :
        for name in stud_list:
            fname=name[0].replace(" ","_")+"_"+name[1]+".xlsx"
            if os.path.isfile(fname):
                scores=extract_data(fname,num_in_team)
                writedata(scores,stud_list)


def extract_final_marks(fname):
    ipf=open(fname,'r')
    contents=ipf.readlines()

    score=0.
    count=0
    for line in contents:
        if line[2:16] == 'Overall score:':
            string_score = line.split('**')[-1]
            try:
                score=score+float(string_score)
            except:
                pass
            count=count+1
    if count !=0:
        return (totmarks*score)/(5.0*float(count))
    else:
        return 'Error'

def write_sheet(fname,data):
    # Construct student spreadsheet containing the necessary student names
    import xlsxwriter as xl
    
    wb = xl.Workbook(fname)
    sh = wb.add_worksheet('peer_review')

    for ii in range(len(data)):
        for jj in range(3):
            sh.write(ii,jj,data[ii][jj])
            
    wb.close()

# once the individual feedback has been collated for each student, create a
# pretty PDF to send to each student, and extract the final mark also

try:
    import pypandoc
    pdfoutput = (generate_feedback and pdfoutput)
except ImportError:
    pdfoutput = False
    pass

from subprocess import call
import os
import sys

if generate_feedback:
    call (['mkdir', 'feedback/'])
data_struct =[]
try:
    ipfile=open(teams_file,'r')
    lines=ipfile.readlines()
    for student in lines:
        stud_name = student.split(',')[0]
        stud_num  = student.split(',')[-1].strip('\n')

        inpfile = stud_num+".md"
        if pdfoutput:
            try:
                outfile = 'feedback/'+stud_num+".pdf"
                if os.path.isfile(inpfile):
                    pypandoc.convert_file(inpfile, 'pdf', outputfile = outfile, extra_args=['--template='+template_tex])
                else:
                    print ("could not locate file " + inpfile)
            except:
                print ("could not create file " + outfile)
                pass
        score = extract_final_marks(inpfile)
        data_struct.append((stud_name, stud_num, score))
        if (not generate_feedback) or (pdfoutput):
            call(["rm", inpfile])
        else:
            call(["mv", inpfile, "feedback/"])

except:
    sys.exit("could not extract student names from "+teams_file)

write_sheet(output_marks, data_struct)



