import csv
from ostn02python import OSGB, OSTN02

if __name__=="__main__":

	outMeasurements = open("outMeasurements.js", "wt")


	for row in csv.DictReader(open("measuredno2-2019.csv")):

		#print (row)

		(x,y,h) = OSTN02.OSGB36_to_ETRS89 (float(row["X"]), float(row["Y"]))
		(gla, glo) = OSGB.grid_to_ll(x, y)
		print (row["Site ID"], gla, glo)
		if len(row["2018"])==0: continue

		vals = [gla, glo, int(float(row["2018"])/10)*10, 
			row["Site ID"]]
		fmt = ("\tL.marker([{}, {}], {{icon: caution{}sIcon}}).addTo(mymap3).bindPopup(\""
			+"<b>Receptor {}</b><br/>")

		for y in range(2012,2019):
			if len(row[str(y)]) == 0: continue
			fmt += "NO2 {}: {}<br/>".format(y, "{}")
			vals.append(row[str(y)])

		fmt += "\");\n"

		outMeasurements.write(fmt.format(*vals))

	outMeasurements.close()

