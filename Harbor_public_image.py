import requests,json,sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
print("usage: python3 ./Harbor_public_image.py https://xx.xx.xx.xx/")
baseurl = sys.argv[1]


def getversion(baseurl):
    url=baseurl+"/api/systeminfo"
    r=requests.get(url,verify=False)
    if r.status_code==200:
        return "v1"
    else:
        return "v2"






def getprojects(baseurl):
    url=baseurl+"/api/v2.0/projects/"
    r=requests.get(url,verify=False)
    data=json.loads(r.text)
    #print(data)
    projects=[]
    for i in data:
        if i["metadata"]["public"]=="true":
            projects.append(i["name"])
        else:
            print("no public projects !!!")
    #print(projects)
    return projects
            
        
        
        
def getrepos(baseurl,projects):
    repos=[]
    for project in projects:
        
        url=baseurl+"/api/v2.0/search?q="+project
        r=requests.get(url,verify=False)
    #print(r)
        data=json.loads(r.text)
    #print(data)
        
        if data["project"][0]["metadata"]["public"]=="true":
            repos_json_list=data["repository"]
            for i in repos_json_list:
                repos.append(i["repository_name"])
        else:
            print("not public repos !!!")
        #print(repos)
    return repos

def getimageurl(baseurl,repos):
    
    for i in repos:
        try:    
            project=i.split("/")[0]
            imagename=i.split("/")[1]
            url=baseurl+"/api/v2.0/projects/"+project+"/repositories/"+imagename+"/artifacts?with_tag=true&with_scan_overview=true&with_label=true&page_size=15&page=1"
            r=requests.get(url,verify=False)
            data=json.loads(r.text)
            #print(data[0])
            digest=data[0]["digest"]
            image=(baseurl.split("/")[2]+"/"+i+"@"+digest)
            print(image)
            #imageurls.append(baseurl+"/"+i+"@"+digest)
            #print(imageurls)
        except Exception:
            continue
    
    


def getprojects_v1(baseurl):
    projects={}
    
    url=baseurl+"/api/projects"
    r=requests.get(url,verify=False)
    data=json.loads(r.text)
    for i in data:
        if i["metadata"]["public"]=="true":
            projects[i["name"]]=i["project_id"]
    print(projects)
    return projects           


def getrepos_v1(baseurl,projects):
    repos=[]
    for project in projects.keys():
        url=baseurl+"/api/repositories?project_id="+str(projects[project])+"&q="
        r=requests.get(url,verify=False)
        data=json.loads(r.text)
        for repo in data:
            repos.append(repo["name"])
    return repos
        
def getimageurl_v1(baseurl,repos):
    
    for repo in repos:
        url=baseurl+"/api/repositories/"+repo+"/tags?detail=true"
        r=requests.get(url,verify=False)
        data=json.loads(r.text)
        data=data[-1]
        digest=data["digest"]
        image=baseurl.split("/")[2]+"/"+repo+"@"+digest
        print(image)
    
            
version=getversion(baseurl)
if version=="v1":    
    projects=getprojects_v1(baseurl)
    repos=getrepos_v1(baseurl,projects)
    getimageurl_v1(baseurl,repos)

elif version=="v2":
    projects=getprojects(baseurl)
    repos=getrepos(baseurl,projects)
    getimageurl(baseurl,repos)

































