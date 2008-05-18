# coding=UTF-8
# Copyright (c) 2008 Geoffrey Sneddon
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from lxml import etree
from copy import deepcopy

from specGen import utils

class xref(object):
	"""Add cross-references."""
	
	dfns = {}
	refs = ("span", "abbr", "code", "var", "samp", "i")
	not_within = ("a", "dfn", "datagrid")
	
	def __init__(self, ElementTree, **kwargs):
		self.buildReferences(ElementTree, **kwargs)
		self.addReferences(ElementTree, **kwargs)
	
	def buildReferences(self, ElementTree):
		for dfn in ElementTree.iter("dfn"):
			if dfn.get(u"title"):
				name = dfn.get(u"title")
			else:
				name = utils.textContent(dfn)
			
			name = name.strip(utils.spaceCharacters).lower()
			id = utils.generateID(dfn)
			
			dfn.set(u"id", id)
			
			self.dfns[name] = id
	
	def addReferences(self, ElementTree):
		for tag in self.refs:
			for element in ElementTree.iter(tag):
				goodParenting = True
				current = element
				while (current.getparent()):
					current = current.getparent()
					if current.tag in self.not_within:
						goodParenting = False
						break
				
				if goodParenting:
					if element.get(u"title"):
						name = element.get(u"title")
					else:
						name = utils.textContent(element)
					
					name = name.strip(utils.spaceCharacters).lower()
					
					if name in self.dfns:
						if element.tag == "span":
							element.tag = "a"
							element.set("href", "#" + self.dfns[name])
						else:
							link = etree.Element("a", {"href": "#" + self.dfns[name]})
							link.append(deepcopy(element))
							link[0].tail = None
							element.addnext(link)
							element.getparent().remove(element)