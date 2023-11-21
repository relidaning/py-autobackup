import re
from backup import *

if __name__ == '__main__':

    d={}

    try:
        file = open('autoBackup.ini', 'r')
        for line in file:
            if line.strip() == '':
                continue
            matchObj=re.match('\\[(\D*)\\]', line.strip(), re.M|re.I)
            if matchObj:
                # print('k:', matchObj.group(1))
                k = matchObj.group(1)
                d[k]=''
            else:
                # print('v:', line.strip())
                v = line.strip()
                d[k]=v if d[k]=='' else d[k]+', '+v
    except FileNotFoundError:
        d = {'target': '', 'achieve': ''}

    # print('conf:', d)
    aconf = Conf(target=d['target'])
    # print(aconf)

    achieve = Achieve3(aconf)
    achieve.watch()