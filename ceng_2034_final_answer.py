#!/usr/bin/python3

import os
import requests
import sys
import hashlib
import uuid
import time
import multiprocessing
from multiprocessing import Pool


start_time=time.time()

print("There are %d CPUs on this machine" % multiprocessing.cpu_count())
print("Load avg:", os.getloadavg())


url = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

def child_process(url): 

	pid = os.fork() 

	if pid > 0: 
		print("Parent process and pid is : ", os.getpid()) 
		#avoid the orphan process
		os.waitpid(pid, 0)

		download_files=os.listdir()
		download_files.remove("final.py")
		print("Download files: ",download_files)

		a=[]
		

		with Pool(5) as p:
			a = p.map(control_md5,download_files)



		#find duplicate elements with multiprocessing
		with Pool(5) as p:
			duplicate = p.starmap(find_duplicates,( [a[0], a],[a[1], a], 
				[a[2], a], [a[3], a], [a[4], a]))


		dup_list=list(duplicate)
		list2=[]
		
		#remove the not unique elements and None in dup_list
		for i in dup_list:
			if i==None:
				dup_list.remove(None)
			elif i not in list2:
				list2.append(i)

		print("Duplicate files: ",list2)
		
		print ("Time taken =",time.time() - start_time,"seconds")

	else:
		print("Child process and pid is : ", os.getpid()) 
		
		#with the child process, download the files
		for i in range(5):
			download_file(url[i],"file{}".format(i))

		


def download_file(url, file_name=None):
	print("download_file processes pid:",os.getpid())
	r=requests.get(url, allow_redirects=True)
	file=file_name if file_name else str(uuid.uuid4())
	open(file, 'wb').write(r.content)

def find_duplicates(elem,a):
	
	print("find_duplicate processes pid:", os.getpid())
	
	j=0
	elements=[]

	for i in range(5):
		#it checks the duplicate elements
		if a[i] == elem:
			elements.insert(j,i)
			j +=1

			if j > 1:
				return elements

#I found this function on the internet
def control_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


child_process(url)	

