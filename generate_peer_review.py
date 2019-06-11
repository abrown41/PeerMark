################################################################################

teams_file           = "teams.csv"            # csv file containing list of students and their teams
template_spreadsheet = "template_spreadsheet.xlsx"        # xlsx file containing template spreadsheet
instruction_file     = "instructions.txt"  # text file containing instructions for completing the spreadsheet

team_letters = ['A', 'B', 'C'] # Allows for subgroups of teams (e.g. by tutorial)
no_of_teams = 11 # the maximum number of teams in a subgroup

################################################################################

# Check input files all exist
import os 
import sys
for fname in [teams_file, template_spreadsheet, instruction_file]:
    if (not os.path.isfile(fname)):
        sys.exit("File " + fname +" not found")

from teams import *

def read_template():
    """ 
    read the template spreadsheet and instructions from file. The filenames are
    given by the user after prompting
    """
    import xlrd

    tempbook = xlrd.open_workbook(template_spreadsheet)
    sheet = tempbook.sheet_by_index(0)

    ipf=open(instruction_file,'r')
    inst=ipf.read()
    ipf.close
    data=[]
    for ii in range(sheet.nrows):
        data.append([sheet.cell_value(ii, col) for col in range(sheet.ncols)])

    numrows=sheet.nrows
    numcols=sheet.ncols

    return data,inst,numrows,numcols

def set_formatting(wb,sh):
    """
    Set spreadsheet formatting. This enforces certain rules, including locking
    the header cells for editing, and restricting the values which may be
    entered in the cells
    """
    locked = wb.add_format()
    locked.set_locked(True)

    unlocked = wb.add_format()
    unlocked.set_locked(False)

    fmt = wb.add_format()
    fmt.set_text_wrap()
    fmt.set_align('vcenter')

    # set column widths (first column wide to contain text)
    sh.set_column('A:A', 30) 
    sh.set_column('B:E', 18)
    sh.protect()

    # set row heights: deeper cells to wrap text.
    for ii in list(range(2,10)) + [11,12]:
        sh.set_row(ii,50)

    rfmt = wb.add_format()
    rfmt.set_align('right')

    format1 = wb.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    format2 = wb.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})

    # colour the cells containing the total marks green if the marks are valid
    # and red if not. If a student enters an 'out of bounds' score, the cells
    # turn red.
    sh.conditional_format('G13', {'type': 'cell',
                                     'criteria': '<',
                                     'value': 0,
                                     'format': format1})
    sh.conditional_format('G13', {'type': 'cell',
                                     'criteria': '>=',
                                     'value': 0,
                                     'format': format2})
    sh.conditional_format('B13:E13', {'type': 'cell',
                                     'criteria': '<',
                                     'value': 0,
                                     'format': format1})
    sh.conditional_format('B13:E13', {'type': 'cell',
                                     'criteria': '>=',
                                     'value': 0,
                                     'format': format2})

    return fmt,rfmt,unlocked

def set_tot_points(data,team):
    """
    team gets a maximum number of points to allocate based on the number of
    team members. Average per team member should be 3.25/5. Thus totpoints gives
    the integer number of points available to allocate, and then conditional
    formatting is set for the cells containing the total, so that they return a
    value of -1 if the maximum value is exceeded.
    """
    import math
    
    totpoints = (str(math.ceil(3.25*(len(team)-1))))
    data[-1][-1]=  '='+totpoints+'-SUM(B12:E12)'
    data[-1][1] = '=if(sum(B12:E12)<='+totpoints+',B12,-1)'
    data[-1][2] = '=if(sum(B12:E12)<='+totpoints+',C12,-1)'
    data[-1][3] = '=if(sum(B12:E12)<='+totpoints+',D12,-1)'
    if len(team) == 5:
        data[-1][4] = '=if(sum(B12:E12)<='+totpoints+',E12,-1)'

    return data, totpoints

def write_sheet(fname,team,inst,indata,numrows,numcols):
    # Construct student spreadsheet containing the necessary student names
    import xlsxwriter as xl

    data=indata.copy()
    
    data, totpoints = set_tot_points(data,team)
    xname=fname+".xlsx"

    wb = xl.Workbook(xname)
    sh = wb.add_worksheet('peer_review')

    fmt,rfmt,unlocked = set_formatting(wb,sh)

    for ii in range(numrows):
        for jj in range(numcols):
            sh.write(ii,jj,data[ii][jj],fmt)
            
    sh.write(0,0,data[0][0],rfmt)
    sh.write(0,1,team[0])

    sh.write(1,0,data[1][0],rfmt)
    for ii in range(1,len(team)):
        sh.write(1,ii,team[ii])
        for jj in list(range(2,8))+ [9, 11]:
            sh.write(jj,ii,"",unlocked)

    set_data_validation(sh)
    input_textbox(inst,sh)

    wb.close()

def set_data_validation(sh):
    # Enforce integer marks between 0 and 5 in the relevant cells in spreadsheet

    for col in ['B','C','D','E']:
        for row in list(range(3,8)) + [12]:
            cell = col+str(row)
            sh.data_validation(cell, {'validate': 'integer',
                                            'criteria': 'between',
                                            'minimum': 0,
                                            'maximum': 5,
                                            'error_message': 'Must be integer between 0 and 5'})          

def input_textbox(text,worksheet):
    # inputs textbox of instructions into final worksheet
    
	options = {
		'width': 350,
		'height': 600,
		'x_offset': 0,
		'y_offset': 0,

		'font': {'color': 'black',
				 'size': 14},
		'align': {'vertical': 'middle',
				  'horizontal': 'center'
				  },
	}

	worksheet.insert_textbox('G1', text, options)

teamlist = extract_teams(teams_file)
stud_names= (get_teams(teams_file))


for team in teamlist:
    tempdata,inst,numrows,numcols= read_template()
    try:
        stud_list=stud_names[team]
    except:
        stud_list = False
        pass
    
    if stud_list :
        teamnames=[team]+[name[0] for name in stud_list]
        for name in stud_list:
            und_name=name[0].replace(" ","_")+"_"+name[1]
            write_sheet(und_name,teamnames,inst,tempdata,numrows,numcols)

