import os

def Main():
	currentDirectory = os.getcwd()
	os.chdir('..')
	currentDirectory = os.getcwd()
	
	fileList = os.listdir(currentDirectory)
	fileList.remove('pythonScripts')
	
	fileTime = []
	
	for i in fileList:
		rawStats = os.stat(i)
		fileTime.append(rawStats.st_mtime)
	
	largestIndex = fileTime.index(max(fileTime))
	
	latestFile = fileList[largestIndex]
	print(latestFile)
	
Main() 
