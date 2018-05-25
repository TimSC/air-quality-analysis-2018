import pyo5m.OsmData as OsmData

if __name__=="__main__":

	fi = open("receptors.osm", "rb")
	osmData = OsmData.OsmData()
	osmData.LoadFromOsmXml(fi)
	print ("nodes", len(osmData.nodes))
	print ("ways", len(osmData.ways))
	print ("relations", len(osmData.relations))

	fiOut = open("receptors.csv", "wt")

	for ndId, ndMeta, ndTags, ndPos in osmData.nodes:
		print (ndTags, ndPos)

		if 'ref' not in ndTags: continue
		receptorId = ndTags['ref']

		fiOut.write("{},{},{}\n".format(receptorId, ndPos[0], ndPos[1]))

	fiOut.close()

