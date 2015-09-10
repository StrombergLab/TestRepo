import re
import time
import os
import string
import urllib.request

def Main():
	currentDirectory = os.getcwd()
	#print(currentDirectory)
	
	schedulePageBase = 'http://espn.go.com/college-football/schedule/_/week/'
	
	scheduleList = [None] * 16
	
	for i in range(0, 15):
		scheduleList[i] = schedulePageBase + str(i+1)
	
	scheduleList[15] = 'http://espn.go.com/college-football/schedule/_/seasontype/3/week/1'
	
	dataToAddToFile = []
	
	for k in range(len(scheduleList)):
		schedulePage = urllib.request.urlopen(scheduleList[k]).read()	
		gameTable = re.findall('<div id="schedule-page"(.*?)</section>', str(schedulePage))
		
		listOfDates = re.findall('<caption>(.*?)<\/caption>', gameTable[0])
		#print(listOfDates)
		
		getScores = re.findall(':schedule:score".*?game\?gameId=\d+">(.*?)</a></td><td>', gameTable[0])
		#print(getScores)
		
		getTeams = re.findall('/_/id/\d+"><span>(.*?)</span>', gameTable[0])
		#print(getTeams)
		
		#for i in range(len(getScores)):
		#	print(getTeams[i*2], end=' ')
		#	print('and', end= ' ')
		#	print(getTeams[i*2 + 1], end= ' ')
		#	print(getScores[i])
			
		gameWinner = ''
		grabTeamsOnce = False
		for i in range(len(getScores)):
			skipCalculation = False
			
			lineForFile = ''
			
			tempTeamRE = re.findall('(\w+) \d+, (\w+) \d+', getScores[i])
			tempScoreRE = re.findall('\w+ (\d+), \w+ (\d+)', getScores[i])
			#print(tempTeamRE)
			#print(tempScoreRE)
			
			if not tempTeamRE:
				gameWinner = getScores[i]
				skipCalculation = True
			
			if skipCalculation == False:
				print(tempTeamRE[0][0], 'vs', tempTeamRE[0][1], end=' ')
				
				lineForFile = tempTeamRE[0][0] + '\t' + tempTeamRE[0][1]
				
				if tempScoreRE[0][0] > tempScoreRE[0][1]:
					print('Winner: ', tempTeamRE[0][0])	
					lineForFile = lineForFile + '\t' + tempTeamRE[0][0]
				
				if tempScoreRE[0][0] < tempScoreRE[0][1]:
					print('Winner: ', tempTeamRE[0][1])
					lineForFile = lineForFile + '\t' + tempTeamRE[0][1]
					
				if tempScoreRE[0][0] == tempScoreRE[0][1]:
					print('Winner:  Tie Game')
					lineForFile = lineForFile + '\tDraw'
					
			if skipCalculation == True:
				if grabTeamsOnce == False:
					rawTeams = re.findall('">(\w+)</abbr></a></td><td', str(schedulePage))
					grabTeamsOnce = True
					
				print(rawTeams[i*2], 'vs', rawTeams[i*2 + 1], 'Winner: ', gameWinner)
				lineForFile = rawTeams[i*2] + '\t' + rawTeams[i*2 + 1] + '\t' + gameWinner
			
			dataToAddToFile.append(lineForFile)
			
	with open('teamWinners', 'w') as f:
		for j in dataToAddToFile:
			f.write(j + '\n')
			
Main()	
