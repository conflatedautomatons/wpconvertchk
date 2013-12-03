#
# Check for unconverted URLs for images in after wordpress domain conversion
#

from urllib2 import *
from HTMLParser import HTMLParser
import time
import traceback
import sys



class LinkAndImgParser(HTMLParser):

	def __init__(self,site,oldsite):
		HTMLParser.__init__(self)
		self.site = site
		self.oldsite = oldsite
		self.newPages = set()
		self.visited = set()
		self.possibleOld = set()

	def handle_starttag(self,tag,attrs):
		if tag == "a":
			for attr in attrs:
				if attr[0] == 'href':
					link = attr[1]
					if link.find(self.oldsite) > 0:
						self.addPossibleOld(link)
					if (link.find(self.site) < 0) \
					or (link.find("#comment") > 0) \
					or (link.find("#main") > 0) \
					or (link in self.visited):
						return
					self.newPages.add(link)
		if tag == "img":
			for attr in attrs:
				if attr[0] == 'src':
					srcLink = attr[1]
					if srcLink.find(self.oldsite) > 0:
						self.addPossibleOld(link)

	def addPossibleOld(self,link):
		print "Possible old reference %s " % (link) 
		self.possibleOld.add(link)

	def checkSite(self):
		self.checkPage(self.site)

	def checkPage(self,pageUrl):
		print "Checking page %s " % (pageUrl)
		#if len(self.visited) % 10 == 0:
		#	print len(self.visited)
		try:
			uh = urlopen(pageUrl)
			for line in uh:
				self.feed(line)
			self.visited.add(pageUrl)
			if pageUrl in self.newPages:
				self.newPages.remove(pageUrl)
			# This is a bit dumb and slow
			for page in frozenset(self.newPages):
				self.checkPage(page)
		except Exception as f:
			print "(Dodgy page choice) %s ... %s " % (pageUrl,f)
			print traceback.format_exc()
			self.visited.add(pageUrl)
			if pageUrl in self.newPages:
				self.newPages.remove(pageUrl)

	def printState(self):
		print "Visited %d pages"  % len(self.visited)
		print "Possible old images"
		for link in self.possibleOld:
			print link


if __name__ == "__main__":
	site, oldsite = sys.argv[1:3]
	print time.ctime()
	parser = LinkAndImgParser(site, oldsite )
	parser.checkSite()
	parser.printState()
	print time.ctime()

