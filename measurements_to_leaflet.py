import csv
from ostn02python import OSGB, OSTN02

if __name__=="__main__":

	outPollution = open("outPollution.js", "wt")

	receptorPosDict = {}
	for row in csv.DictReader(open("measuredno2.csv")):
		
		receptorNum = row["Site ID"]
		(x,y,h) = OSTN02.OSGB36_to_ETRS89 (float(row["X"]), float(row["Y"]))
		(gla, glo) = OSGB.grid_to_ll(x, y)

		if len(row["2017"]) > 0:

			m2017 = float(row["2017"])

			popupHtml = "<b>Receptor {}</b>".format(receptorNum)

			for year in range(2012, 2018):
				if len(row[str(year)]) == 0: continue
				popupHtml += "<br/>NO2 {}: {}".format(year, float(row[str(year)]))
		
			outPollution.write(("\tL.marker([{}, {}], {{icon: caution{}sIcon}}).addTo(mymap).bindPopup(\""
				+"{}\");\n").format(
				gla, glo, int(m2017/10)*10, popupHtml))

		else:
			popupHtml = "<b>Receptor {}</b>".format(receptorNum)
		
			outPollution.write(("\tL.marker([{}, {}], {{icon: negligibleIcon}}).addTo(mymap).bindPopup(\""
				+"{}\");\n").format(
				gla, glo, popupHtml))
			
	outPollution.close()

