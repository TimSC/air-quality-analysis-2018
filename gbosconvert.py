import csv
from ostn02python import OSGB, OSTN02

if __name__=="__main__":

	outMeasurements = open("outMeasurements.js", "wt")


	for row in csv.DictReader(open("actualno2.csv")):

		#print (row)

		(x,y,h) = OSTN02.OSGB36_to_ETRS89 (float(row["X"]), float(row["Y"]))
		(gla, glo) = OSGB.grid_to_ll(x, y)
		print (row["Site ID"], gla, glo)
		if len(row["2016"])==0: continue

		outMeasurements.write(("\tL.marker([{}, {}], {{icon: caution{}sIcon}}).addTo(mymap3).bindPopup(\""
			+"<b>Receptor {}</b><br/>"
			+"NO2 2012: {}<br/>"
			+"NO2 2013: {}<br/>"
			+"NO2 2014: {}<br/>"
			+"NO2 2015: {}<br/>"
			+"NO2 2016: {}<br/>"
			+"\");\n").format(
			gla, glo, int(float(row["2016"])/10)*10, 
			row["Site ID"], row["2012"], row["2013"], row["2014"], row["2015"], row["2016"]))

	outMeasurements.close()

