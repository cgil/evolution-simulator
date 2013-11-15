#!/usr/bin/env python
import random
import math

class AminoAcid(object):
	def __init__(self, type):
		self.type = type

class Protein(object):
	def __init__(self, aminoAcids):
		self.aminoAcids = aminoAcids

class Cell(object):
	def __init__(self, chromosomes):
		self.chromosomes = chromosomes
	def __str__(self):
		val = ""
		counter = 1
		for cGroup in chromosomes:
			val += "Chromosome group #" + str(counter) + ":\n"
			for c in cGroup:
				val += c.sequence + " "
			val += "\n"
			counter += 1
		return val

class Chromosome(object):
	def __init__(self, sequence):
		self.sequence = sequence


# {'chromosome1':[chromotid1, chromotid2],}

class Gamete(Cell): 
	def meiosis(self):
		for cGroup in self.chromosomes:
			cGroup.insert(1, cGroup[0])	# replication: duplicate each chromosome pair
			cGroup.insert(3, cGroup[2])
			cGroup = self.__prophase(cGroup)	# crossing over at chiasmatas 
	def __prophase(self, chromosomes):
		halfLength = len(chromosomes)/2
		for i in xrange(halfLength):	# cross over pairs are (i) and (i + halfLength)
			chromatid1 = chromosomes[i].sequence.split("|")
			chromatid2 = chromosomes[i+halfLength].sequence.split("|")
			chiasmatas = []
			minChromatidLength = min(len(chromatid1), len(chromatid2))
			chiasmata = random.randint(0, minChromatidLength - 1)
			chiasmatas.append(chiasmata)
			chromatid1[chiasmata], chromatid2[chiasmata] = self.__swap(chromatid1[chiasmata], chromatid2[chiasmata])
			for i in xrange(minChromatidLength):
				chiasmata = random.randint(0, minChromatidLength - 1)
				if chiasmata in chiasmatas:
					continue
				x = min(map(lambda x: abs(x-chiasmata), chiasmatas))
				probOfCrossover = 1/(1+math.exp(-(-5+x)))
				success = int(probOfCrossover*100) >= random.randint(1,100)
				if success:
					chromatid1[chiasmata], chromatid2[chiasmata] = self.__swap(chromatid1[chiasmata], chromatid2[chiasmata])
					chiasmatas.append(chiasmata)

	def __swap(self, a, b):
		tmp = a
		a = b
		b = tmp
		return a,b

c1m = Chromosome("10|01|01")
c1d = Chromosome("01|11|10")
c1 = [c1m, c1d]
c2 = [c1d, c1m]
chromosomes = []
chromosomes.append(c1)
chromosomes.append(c2)

cell = Gamete(chromosomes)
cell.meiosis()

print cell






