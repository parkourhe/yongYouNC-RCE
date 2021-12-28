import os
import requests
import queue
from termcolor import cprint
from bs4 import BeautifulSoup
from multiprocessing import Pool

def delFile():
    if os.path.isfile('res.txt'):
        os.remove('res.txt')

def poc(targetArr,q):
    for l,j in enumerate(targetArr):
        with open("poc.txt") as file:
            # print(l)
            for line in file.readlines():
                # print(line)
                if "http" not in j:
                    ta = "http://{}{}".format(j,line)
                ta="{}{}".format(j,line)
                if "\n" in ta:
                    ta = ta.strip("\n")
                q.put(ta)
            file.close()
    return q

def target():
    targetArr = []
    with open("target.txt") as file:
        for line in file.readlines():
            if "\n" in line:
                line = line.strip("\n")
            if "http" not in line:
                line = "http://{}".format(line)
            targetArr.append(line)

        return targetArr

def isVul(target,value,code):
    soup = BeautifulSoup(value, "html.parser")
    s  = soup.find("h1")
    if s:
        if "BeanShell Test Servlet" in s:
            cprint("{}---POC可用".format(target),"green")
            return True
        else:
            cprint("{}---POC不可用".format(target),"red")
            return False
    else:
        cprint("{}---POC不可用".format(target),"red")
        return False

def errorHand(err):
    print("something is wrong")
    exit(-1)

def requestRes(target):
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    'Referer': 'https://www.baidu.com/robot',
    "Connection": "close"
    }
    print("[-] requesting target url with POC --{}.....".format(target))
    try:
       
        res = requests.get(target,headers=headers,timeout=3,verify=False)
        res.close()
        vulres = isVul(target,res.text,res.status_code)
           
    except Exception as e:
        print(e)
        content = "[+] target--{}-status:---------{}\n".format(target,'error')
        print(content)
        with open("res.txt","a+") as file:
            file.write(content)
    else:
        content = "[+] target--{}-status:{}---------{}\n".format(target,res.status_code,vulres)
        print(content)
        with open("res.txt","a+") as file:
            file.write(content)
            file.close()
    return


if __name__ == '__main__':
    delFile()
    q = queue.Queue()
    qe = poc(target(),q)
    p = Pool()
    while not qe.empty():
        data = qe.get(block=False)
        p.apply_async(requestRes,args=(data,),error_callback=errorHand)
    p.close()
    p.join()