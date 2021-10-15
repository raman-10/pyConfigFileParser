import re
from pprint import pprint
class config_parse:
    def __init__(self):
        self.config_file_dict=None
        self.filepath=None
        
    def read(self,file):
        self.filepath=file
        with open(file,"r") as f:
            data=f.readlines()

        d={}
        for i in data:
            if(i.strip("\n ")!=''):
                if(re.search(r'\[.*\]',i)):
                    key=i.strip("\n][ ")
                    d[key]={}
                    continue
                subs=i.strip(" \n").split("=")
#                 print(subs)
                d[key][subs[0].strip()]=subs[1].strip()
        self.config_file_dict=d
        return self.config_file_dict
    def getSections(self):
        return list(self.config_file_dict.keys())
    
    def getSectionsData(self,*sectionhead):
        d={"data":{}}
        no=[]
        for i in sectionhead:
            try:
                d["data"][i]=self.config_file_dict[i]
            except KeyError:
                no+=[i]
        if(no!=[]):
            d["incorrect_section_head_names"]=no
        return d
    
    def getSubdata(self,sectionhead,*sub):
        print(sub)
        l={"data":{}}
        no=[]
        
        if(sectionhead in self.config_file_dict):
            for i in sub:
                try:
                    # print(i,self.config_file_dict[sectionhead][i])
                    l["data"][i]=self.config_file_dict[sectionhead][i]
                except:
                    no+=[i]
            if(no!=[]):
                l["incorrect_subheading_list"]=no
            return l

        return "incorrect sectionhead"

    def write(self,newFilePath):
        
        
        string=""
        for i in self.config_file_dict.keys():
            string+="["+i+"]"+"\n\n"
            k=self.config_file_dict[i].keys()
            v=self.config_file_dict[i].values()
            string+='\n'.join(list(map(lambda x:str(x[0])+"="+str(x[1]),zip(k,v))))
            string+="\n\n"
        with open(newFilePath,"w") as f:
            f.write(string)
            
    def addSectionAndPersist(self,sectionhead,mapping,newFilePath):
        if not(isinstance(mapping,dict)):
            return "Dictionary required in mapping"
        if sectionhead in self.getSections():
            return "Section already present"
        else:
            self.config_file_dict[sectionhead]=mapping
            self.write(newFilePath)

    def updateAndPersist(self,sectionhead,mapping,newFilePath):
        if not(isinstance(mapping,dict)):
            return "Dictionary required in mapping"
        if sectionhead not in self.getSections():
            return "Section not present"
        else:
            self.config_file_dict[sectionhead].update(mapping)
            self.write(newFilePath)


if __name__=='__main__':
    obj=config_parse()
    obj.read("conf.cfg")
    obj.updateAndPersist("Section 1",{"key3":"value3"},"copyconf.cfg")
    obj.addSectionAndPersist("new section",{"key1":"val1","key2":"val2"},"copyconf2.cfg")
    pprint(obj.getSectionsData("Section 1","Section 2","wrong section"))
    pprint(obj.getSections())
    pprint(obj.getSubdata("Section 1","key1","key2","wrong sub"))