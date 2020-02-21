r = open('/Users/hrithik/PycharmProjects/testpy/Webpages.txt','r')
w = open('/Users/hrithik/PycharmProjects/testpy/Final_Webpage_List.txt','w')
count = 1
line_list = r.readlines()
other_list = []
for line in line_list:
    other_list = []
    if 'Term counter' in line:
        newStr = "Page counter: "+str(count)+" "+line
        count += 1

    else:
        newStr = line
    other_list.append(newStr)
    w.writelines(other_list)

r.close()
w.close()