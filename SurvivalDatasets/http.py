import Cache as cache

headers = {
	#"User-Agent": "scikit-learn datasets fetcher",
	"Connection": "keep-alive",
}

import requests

def setupSession():
	reqSess = requests.Session()

	try:
		import hyper.http20.response
		headers["Accept-Encoding"] = [k.decode("utf-8") for k in hyper.http20.response.decompressors]

		if b"br" not in hyper.http20.response.decompressors:
			try:
				import brotli
				hyper.http20.response.decompressors[b"br"] = brotli.Decompressor
			except:
				pass

		if b"br" in hyper.http20.response.decompressors:
			headers["Accept-Encoding"].append("br")

		from hyper.contrib import HTTP20Adapter
		ad = HTTP20Adapter()
		reqSess.mount("https://", ad)
		reqSess.mount("http://", ad)
		hyper.h2.settings.ENABLE_PUSH = False
	except:
		pass

	headers["Accept-Encoding"] = ", ".join(headers["Accept-Encoding"])
	reqSess.headers.update(headers)
	return reqSess

reqSess = setupSession()

def doGet(uri, binary=False):
	res = reqSess.get(uri)
	if binary:
		return res.raw
	return res.text

def get(uri, *args, force=False, binary=False, cacheFile="./survivalDatasets.sqlite", **kwargs):
	with cache.StringCache(cacheFile, True) as hcache:
		res = hcache[uri]
		if res and not force:
			return res
		else:
			res = doGet(uri, binary)
			if res:
				hcache[uri] = res
			return res
