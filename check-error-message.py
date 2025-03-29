import shutil
import sys,os
import pandas as pd

### Create by: Leticia A. Gomes
### Goal: Automatize copy failed jobs to workflow
### Command to run: python3 resub-backonworkflow.py NAME-WORKFLOW
# Change NAME-WORKFLOW to your workflow flow names

completed=[]
failed=[]

title='%s' % sys.argv[1].split('.')[0]
logpath=os.getcwd()
filenames=[]
path_file=[]
error_msg=[]

#Define types of calculations that failed will be checked
#jobs=['s0-sp-tddft-solv','s0-opt-freq-solv','s1-opt-freq-solv','t1-opt-freq-solv','cat-opt-freq-solv','1an-opt-freq-solv','cat-opt-freq-vac', 's0-opt-freq-vac']
jobs=['s1-opt-freq-solv']

#GET PATH
def get_path():
  name_workflow='%s' % (title)
  path_workflow='%s/%s' % (logpath,name_workflow)
  os.chdir(path_workflow)
  for file in os.listdir():
    if file.endswith('.log'):
      pathfile='%s/%s' % (path_workflow,file)
      path_file.append(pathfile)
  #remove duplicates
  file_path=[]
  for item in path_file:
    if item not in file_path:
      file_path.append(item)
      for item in file_path:
        if item not in filenames:
          filenames.append(item)
  return file_path

#Check if it is completed or failed

def check_complete(path):
  for item in path:
    with open(item, "r") as f:
      last_line = f.readlines()[-1]
    f.close()
    check=last_line.find("Normal termination of Gaussian")
    if check != -1:
      completed.append(item)
    else:
      failed.append(item)
      with open(item, "r") as f:
        message=f.readlines()[-7]
      f.close()
      error_msg.append(message)

def export_failed():
 bench_number=[]
 inchkey=[]
 job=[]
 for item in failed:
  path=item
  bench_number.append(path.split("/")[7])
  inchkey.append(item.split("/")[8].split(".")[0].split("_")[0])
  job.append(item.split("/")[8].split(".")[0].split("_")[1])
 failed_results=pd.DataFrame(list(zip(failed,bench_number,inchkey,job,error_msg)),columns =['Path','Number bench','Inchkey','Job','Message'])
 os.chdir(logpath)
 failed_results.to_csv(str(title)+"-failed.csv",index=False)
                           
              
                            
      
    


def main():
    path=get_path()
    check_complete(path)
    export_failed()

if __name__ == "__main__":
    main()
