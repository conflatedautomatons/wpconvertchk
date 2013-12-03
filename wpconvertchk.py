
from urllib2 import *
from HTMLParser import HTMLParser

site = "http://journeysofthefabulist.wordpress.com/"
pages = set()
visited = set()


class LinkAndImgParser(HTMLParser):
	def handle_starttag(self,tag,attrs):
		if tag == "a":
			for attr in attrs:
				if attr[0] == 'href':
					link = attr[1]
					if (link.find(site) < 0) \
					or (link.find("#comment") > 0) or (link.find("#main") > 0):
						return
					pages.add(link)
		if tag == "img":
			for attr in attrs:
				if attr[0] == 'src':
					srcLink = attr[1]
					if srcLink.find("fantasy") > 0:
						print "Possible old image %s " % (srcLink) 


parser = LinkAndImgParser()


def checkPage(pageUrl):
	print "Checking page %s " % (pageUrl)
	try:
		uh = urlopen(pageUrl)
		for line in uh:
			parser.feed(line)
		visited.add(pageUrl)
		# This is pretty dumb and slow
		for page in pages:
			if not page in visited:
				checkPage(page)
	except Exception as f:
		print "(Dodgy page choice) %s " % (f)
		visited.add(pageUrl)


checkPage(site)


