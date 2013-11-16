#!/usr/bin/env python
import random
import math
import copy

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

class Gamete(Cell): 
	def meiosis(self):
		i = 0
		for cGroup in self.chromosomes:
			cGroup.insert(1, copy.deepcopy(cGroup[0]))			# replication: duplicate each chromosome pair
			cGroup.insert(3, copy.deepcopy(cGroup[2]))
			print "cGroup: ", i
			i += 1
			self.__prophase(cGroup)	# crossing over at chiasmatas 
	def __prophase(self, chromosomes):
		halfLength = len(chromosomes)/2
		for i in xrange(halfLength):			# cross over pairs are (i) and (i + halfLength)
			chromatid1 = chromosomes[i].sequence.split("|")
			chromatid2 = chromosomes[i+halfLength].sequence.split("|")
			chiasmatas = []
			minChromatidLength = min(len(chromatid1), len(chromatid2))
			chiasmata = random.randint(0, minChromatidLength - 1)
			chiasmatas.append(chiasmata)
			chromatid1[chiasmata], chromatid2[chiasmata] = chromatid2[chiasmata], chromatid1[chiasmata]
			for j in xrange(minChromatidLength):
				chiasmata = random.randint(0, minChromatidLength - 1)
				if chiasmata in chiasmatas:
					continue
				x = min(map(lambda x: abs(x-chiasmata), chiasmatas))
				probOfCrossover = 1/(1+math.exp(-(-5+x)))
				success = probOfCrossover*100 >= random.randint(1,100)
				if success:
					chromatid1[chiasmata], chromatid2[chiasmata] = chromatid2[chiasmata], chromatid1[chiasmata]
					chiasmatas.append(chiasmata)

			chromosomes[i].sequence = "|".join(chromatid1)
			chromosomes[i+halfLength].sequence = "|".join(chromatid2)

c1m = Chromosome("00|00|00|00|00|00|00|00")
c1d = Chromosome("11|11|11|11|11|11|11|11")
c2m = Chromosome("22|22|22|22|22|22|22|22")
c2d = Chromosome("33|33|33|33|33|33|33|33")
c1 = [c1m, c1d]
c2 = [c2m, c2d]
chromosomes = []
chromosomes.append(c1)
chromosomes.append(c2)

cell = Gamete(chromosomes)
cell.meiosis()

print cell






