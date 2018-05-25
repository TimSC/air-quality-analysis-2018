import csv

if __name__=="__main__":

	receptorPosDict = {}
	for row in csv.reader(open("receptors.csv")):
		receptorPosDict[int(row[0])] = float(row[1]), float(row[2])

	outImpact = open("outImpact.js", "wt")
	outPollution = open("outPollution.js", "wt")
		
	# read in a csv file, and create a placemark for each record
	for rowNum, row in enumerate(csv.reader(open("2026-Nitrogen Dioxide Results.csv"))):

		if rowNum < 5: continue

		receptor, baseline2015, without2026, with2026, pcAqal, change, pcRelChange, significant, direction = row
		baseline2015 = float(baseline2015)

		receptorNum = int(receptor[1:])
		if receptorNum not in receptorPosDict:
			print ("No position for receptor", receptorNum)
			continue
		pos = receptorPosDict[receptorNum]
		#print (receptor, pos, baseline2015, significant, direction)

		if direction in ["Adverse", "Beneficial"]:
			outImpact.write(("\tL.marker([{}, {}], {{icon: {}{}Icon}}).addTo(mymap).bindPopup(\""
				+"<b>Receptor {}</b><br/>Baseline NO2 2015: {}<br/>"
				+"With scheme NO2 2026: {}<br/>Without scheme NO2 2026: {}<br/>"
				+"Impact: {} {}"
				+"\");\n").format(
				pos[0], pos[1], direction.lower(), significant, 
				receptorNum, baseline2015, with2026, without2026, significant, direction))
		elif significant == "Negligible":
			outImpact.write(("\tL.marker([{}, {}], {{icon: negligibleIcon}}).addTo(mymap).bindPopup(\""
				+"<b>Receptor {}</b><br/>Baseline NO2 2015: {}<br/>"
				+"With scheme NO2 2026: {}<br/>Without scheme NO2 2026: {}<br/>"
				+"Impact: {} {}"
				+"\");\n").format(
				pos[0], pos[1], 
				receptorNum, baseline2015, with2026, without2026, significant, direction))

		outPollution.write(("\tL.marker([{}, {}], {{icon: caution{}sIcon}}).addTo(mymap2).bindPopup(\""
			+"<b>Receptor {}</b><br/>Baseline NO2 2015: {}<br/>"
			+"With scheme NO2 2026: {}<br/>Without scheme NO2 2026: {}<br/>"
			+"Impact: {} {}"
			+"\");\n").format(
			pos[0], pos[1], int(baseline2015/10)*10, 
			receptorNum, baseline2015, with2026, without2026, significant, direction))

	outImpact.close()
	outPollution.close()

