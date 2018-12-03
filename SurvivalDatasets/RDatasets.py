__all__ = ("getDatasets",)
from io import StringIO
from .GitHubDatasets import *
from sklearn.utils import Bunch
from warnings import warn

defaultRepoName = "vincentarelbundock/Rdatasets"

from .http import get as httpGet

def getRDatasetsIndex(repoName=None, refspec="master"):
	if not repoName:
		repoName = defaultRepoName
	import csv
	res = {}
	repoRawPath = GH_RAW_BASE + repoName

	index = httpGet(repoRawPath + "/" + refspec + "/datasets.csv")
	reader = csv.reader(index.splitlines())
	headers = next(reader)

	hasDicMapping = {}
	hasPrefix = "has_"

	for i in range(len(headers)):
		headers[i] = headers[i].lower()
		if headers[i].startswith(hasPrefix):
			hasDicMapping[headers[i][len(hasPrefix):]] = headers[i]

	for r in reader:
		row = dict(zip(headers, r))
		pkg = row['package']
		del(row['package'])
		id = row['item']

		hasDic = {}
		for hasTypeName, hasTypeColumnName in hasDicMapping.items():
			hasDic[hasTypeName] = bool(row[hasTypeColumnName])
			del(row[hasTypeColumnName])

		row["has"] = hasDic

		row["shape"] = (row["rows"], row["cols"])
		del(row["rows"])
		del(row["cols"])

		if pkg not in res:
			res[pkg] = {}

		helpPath = row["doc"].split("/")
		helpPath.insert(-1, "rst")
		helpPath[-1] = ".".join(helpPath[-1].split(".")[:-1]+["rst"])
		row["doc"] = "/".join(helpPath)
		res[pkg][id] = row

	return res


index = None


def getDatasets(category=None, names=None, usePandas=False):
	global index
	if not index:
		index = getRDatasetsIndex()

	res = {}

	if category is None and names is None:
		for cn in index:
			res[cn] = getDatasets(category=cn, names=None, usePandas=usePandas)
	else:
		if isinstance(names, str):
			names = (names,)

		if names is None:
			names = index[category]

		for name in names:
			res[name] = getDataset(category, name, usePandas=usePandas)
	return res

from io import StringIO

def getDataset(category, name, usePandas=False):
	"""Returns a dataset from """ + defaultRepoName
	
	metadata = index[category][name]
	csv = httpGet(metadata["csv"])
	desc = httpGet(metadata["doc"])
	
	if not usePandas:
		from numpy import genfromtxt
		data = genfromtxt(csv.splitlines(), delimiter=',', names=True, dtype=None, encoding=None, missing_values="NA", autostrip=True, deletechars="")
	else:
		from pandas import read_csv
		with StringIO(csv) as f:
			data = read_csv(f, skipinitialspace=True, iterator=False, chunksize=None, compression=None, memory_map=True)
		
	
	additionalInfo = parseInfoFromDocs(desc)
	
	if "details" not in additionalInfo:
		additionalInfo["details"] = desc
	
	return Bunch(
		X=data, y=None, target=None, feature_names=(data.dtype.names if not usePandas else list(data.columns)),
		DESCR=metadata["title"],
		url=metadata["csv"],
		**additionalInfo
	)


def parseSections(desc):
	try:
		import docutils.parsers.rst
		import docutils.utils
		import docutils.frontend
	except ImportError as ex:
		warn("`docutils` is not present, unable to parse metadata from docs.")
		return {}

	s = docutils.frontend.OptionParser(components=(
		docutils.parsers.rst.Parser,)).get_default_values()
	p = docutils.parsers.rst.Parser()
	doc = docutils.utils.new_document(None, s)
	p.parse(desc, doc)
	parsedDocs = doc.asdom()
	sections = {}

	for s in parsedDocs.getElementsByTagName("section"):
		tit = s.getElementsByTagName("title")
		nm = tit[0].childNodes[0].data
		sections[nm] = s
	return sections


def parseInfoFromDocs(desc):
	sections = parseSections(desc)
	res = {}

	try:
		res["columnsDescriptions"] = parseColumnsInfo(sections["Format"])
		if "Description" in sections:
			res["details"] = node2text(sections["Description"])
	except Exception as ex:
		res["columnsDescriptions"] = ex

	if "Source" in sections:
		res["references"] = node2text(sections["Source"])

	return res


def getTextFromNodes(node):
	if node.nodeType == node.TEXT_NODE:
		yield node.data
	else:
		for cn in node.childNodes:
			yield from getTextFromNodes(cn)


def node2text(node):
	return "".join(getTextFromNodes(node))


def findAllTables(section):
	return list(findDefinitionListTables(section)) + list(findTables(section))


def findDefinitionListTables(section):
	return findTables(section, "definition_list", "definition_list_item")


def findTables(section, tagName="table", rowTagName="row"):
	ft = section.getElementsByTagName(tagName)
	for t in ft:
		yield t.getElementsByTagName(rowTagName)


def parseColumnsInfo(formatSect):
	parsedParams = {}
	ft = list(findAllTables(formatSect))

	if len(ft) != 1:
		raise ValueError("More than 1 table in `Format` section, don't know which one to parse. "+repr(ft))

	rows = ft[0]

	for row in rows:
		if len(row.childNodes) == 2:
			resNodes = []
			for s in row.childNodes:
				sText = node2text(s)
				if sText is not None:
					sText = sText.strip()
					resNodes.append(sText)

			if len(resNodes) == 2:
				k, v = resNodes
				if k and v:
					if k[-1] == ":":
						k = k[:-1].strip()
					parsedParams[k] = v
			
	return parsedParams
