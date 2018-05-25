#!/usr/bin/env python
'''Example of generating KML from data in a CSV file 

References:

'''
from __future__ import print_function
import csv
import urllib2
from datetime import datetime
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

def makeExtendedDataElements(datadict):
	'''Converts a dictionary to ExtendedData/Data elements'''
	edata = KML.ExtendedData()
	for key, value in datadict.iteritems():
		edata.append(KML.Data(KML.value(value), name=key + "_"))
	return edata

doc = KML.Document()

iconstyles = [
	[1,'ff000000'],
	[1.2,'ff00ff00'],#10s
	[1.4,'ff00ff44'],#20s
	[1.6,'ff00cc88'],#30s ffb400
	[1.8,'ff00aaaa'],#40s
	[2.0,'ff0000ff'],#50s
]

# create a series of Icon Styles
for i, (scale, color) in enumerate(iconstyles):
	doc.append(
		KML.Style(
			KML.IconStyle(
				KML.color(color),
				KML.scale(scale),
				KML.Icon(
					KML.href("https://maps.google.com/mapfiles/kml/shapes/caution.png"),
				),
				KML.hotSpot(x="0.5",y="0",xunits="fraction",yunits="fraction"),
			),
			#balloonstyle,
			id="pollution-style-{threshold}".format(threshold=i),
		)
	)

adverseStyles = [
	['negligible',1,'ff888888'],
	['slight',1.33,'ff0000aa'],
	['moderate',1.66,'ff0000cc'],
	['substantial',2.0,'ff0000ff'],
]

for band, scale, color in adverseStyles:
	doc.append(
		KML.Style(
			KML.IconStyle(
				KML.color(color),
				KML.scale(scale),
				KML.Icon(
					KML.href("http://earth.google.com/images/kml-icons/track-directional/track-0.png"),
				),
				KML.hotSpot(x="0.5",y="0",xunits="fraction",yunits="fraction"),
			),
			#balloonstyle,
			id="adverse-style-{threshold}".format(threshold=band),
		)
	)

beneficialStyles = [
	['negligible',1,'ff888888'],
	['slight',1.33,'ff00aa00'],
	['moderate',1.66,'ff00cc00'],
	['substantial',2.0,'ff00ff00'],
]

for band, scale, color in beneficialStyles:
	doc.append(
		KML.Style(
			KML.IconStyle(
				KML.color(color),
				KML.scale(scale),
				KML.Icon(
					KML.href("http://earth.google.com/images/kml-icons/track-directional/track-8.png"),
				),
				KML.hotSpot(x="0.5",y="0",xunits="fraction",yunits="fraction"),
			),
			#balloonstyle,
			id="beneficial-style-{threshold}".format(threshold=band),
		)
	)


doc.append(KML.Folder())

receptorPosDict = {}
for row in csv.reader(open("receptors.csv")):
	receptorPosDict[int(row[0])] = float(row[1]), float(row[2])

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

	labelData = {}
	labelData['Receptor'] = receptorNum
	labelData['NO2 Baseline (2015)'] = baseline2015
	labelData['NO2 Without scheme (2026)'] = without2026
	labelData['NO2 With scheme (2026)'] = with2026
	labelData['Impact'] = "{} {}".format(significant, direction)

	if 0:
		pm = KML.Placemark(
			#KML.name("NO2={0}".format(baseline2015)),
			KML.styleUrl(
				"#pollution-style-{thresh}".format(
					thresh=int(baseline2015/10.0)
				)
			),
			makeExtendedDataElements(labelData),
			KML.Point(
				KML.coordinates("{0},{1}".format(pos[1], pos[0]))
			)
		)
		doc.Folder.append(pm)

	if 1:
		if direction=="Adverse":
			pm = KML.Placemark(
				KML.styleUrl(
					"#adverse-style-{thresh}".format(
						thresh=significant.lower()
					)
				),
				makeExtendedDataElements(labelData),
				KML.Point(
					KML.coordinates("{0},{1}".format(pos[1], pos[0]))
				)
			)
			doc.Folder.append(pm)

		if direction=="Beneficial":
			pm = KML.Placemark(
				KML.styleUrl(
					"#beneficial-style-{thresh}".format(
						thresh=significant.lower()
					)
				),
				makeExtendedDataElements(labelData),
				KML.Point(
					KML.coordinates("{0},{1}".format(pos[1], pos[0]))
				)
			)
			doc.Folder.append(pm)



# check if the schema is valid
from pykml.parser import Schema
schema_gx = Schema("kml22gx.xsd")
schema_gx.assertValid(doc)

fi = open("out.kml", "wt")
fi.write(etree.tostring(doc, pretty_print=True))
fi.close()

