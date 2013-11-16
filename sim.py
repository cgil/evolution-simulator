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

# DNA sequence
class Chromosome(object):
	def __init__(self, sequence):
		self.sequence = sequence

# Large collection of information
class Cell(object):
	def __init__(self, chromosomes=None):
		if chromosomes == None:
			self.chromosomes = {}
		else:
			self.chromosomes = chromosomes
		self.totalChromosomes = len(self.chromosomes)
		self.delimeter = "|"	# Chromosome split delimeter
	def __str__(self):
		val = ""
		counter = 1
		for cGroup in self.chromosomes.values():
			val += "Chromosome group #" + str(counter) + ":\n"
			for c in cGroup:
				val += c.sequence + " "
			val += "\n"
			counter += 1
		return val
	# Cell replication
	def mitosis(self):
		return copy.deepcopy(self)

# Used for reproduction
class Gamete(Cell):
	def add(self, chromatid):
		self.chromosomes[self.totalChromosomes] = [chromatid]
		self.totalChromosomes += 1

# Can produce Gametes
class Germ(Cell): 
	# Cell creates Gametes- used for reproduction
	def meiosis(self):
		for cGroup in self.chromosomes.values():
			cGroup.insert(1, copy.deepcopy(cGroup[0]))			# replication: duplicate each chromosome pair
			cGroup.insert(3, copy.deepcopy(cGroup[2]))
			self.__prophase(cGroup)	# crossing over at chiasmatas 
		return self.__anaphase()

	# Cells replicate and then crossover to create diversity
	def __prophase(self, chromosomes):
		halfLength = len(chromosomes)/2
		for i in xrange(halfLength):			# cross over pairs are (i) and (i + halfLength)
			chromatid1 = chromosomes[i].sequence.split(self.delimeter)
			chromatid2 = chromosomes[i+halfLength].sequence.split(self.delimeter)
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
				probOfCrossover = 1/(1+math.exp(-(-5+x)))	# modified logorithmic growth (S) curve - asymptotic at f(x)=1
				success = probOfCrossover*100 >= random.randint(1,100)
				if success:
					chromatid1[chiasmata], chromatid2[chiasmata] = chromatid2[chiasmata], chromatid1[chiasmata]
					chiasmatas.append(chiasmata)

			chromosomes[i].sequence = self.delimeter.join(chromatid1)
			chromosomes[i+halfLength].sequence = self.delimeter.join(chromatid2)
	# Rearranges chromatids into new Gamete cells - increases diversity
	def __anaphase(self):
		gametes = [Gamete(),Gamete(),Gamete(),Gamete()]
		for i in xrange(4):
			for cGroup in self.chromosomes.values():
				rand = random.randint(0, len(cGroup)-1)
				chromatid = cGroup.pop(rand)
				gametes[i].add(chromatid)
		return gametes


c1m = Chromosome("00|00|00|00|00|00|00|00")
c1d = Chromosome("11|11|11|11|11|11|11|11")
c2m = Chromosome("22|22|22|22|22|22|22|22")
c2d = Chromosome("33|33|33|33|33|33|33|33")
cPair1 = [c1m, c1d]
cPair2 = [c2m, c2d]
chromes = {}
chromes[0] = cPair1
chromes[1] = cPair2

cell = Germ(chromes)
gametes = cell.meiosis()





