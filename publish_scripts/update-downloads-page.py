import sys,re,datetime

date_map = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
release_date = datetime.datetime.now()

new_version = sys.argv[1]
print ("New vesion detected : v",new_version)


fin = open("downloads.html", "rt")
data = fin.read()

#detect the previous version
searchObj = re.search(rf'versionInfo">.*? ', data, re.M|re.I)
previous_version = searchObj.group().split('>')[1]
#removing the unwanted space of the previous version string
previous_version = previous_version[:len(previous_version)-1]
#change all the occurences of previous version to new version
data = data.replace(previous_version, new_version)
#add the previous vesion to 1.1.0 - <previous version> stack
data = re.sub(r'1.1.0 - .*?,', '1.1.0 - '+previous_version+',', data)
#release date update
data = re.sub(rf'{new_version} \(.*?\)', new_version+' ('+date_map[release_date.month-1]+' '+str(release_date.day)+', '+str(release_date.year)+')', data)
fin.close()

fin = open("downloads.html", "wt")
fin.write(data)
fin.close()