def get_teams(fname):
    ipf = open(fname,'r')
    contents=ipf.readlines()
    data=[]
    for line in contents:
        data.append((line.split(',')[0],line.split(',')[1],line.split(',')[-1].strip('\n')))
    return find_teams(set(data))


def find_teams(names):
    from collections import defaultdict
    d = defaultdict(list)
    for fn, ln, sn in names:
        d[ln].append((fn,sn))
    return dict((k,v) for (k,v) in d.items() if len(v)>1)

def extract_teams(fname):
    ipf = open(fname,'r')
    contents=ipf.readlines()
    allteams=[]
    for line in contents:
        allteams.append(line.split(',')[1])
    return (list(sorted(set(allteams))))
