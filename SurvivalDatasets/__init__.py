import arff
from warnings import warn
import requests
import pandas
import numpy as np
import sklearn.datasets.openml
from . import RDatasets
from io import StringIO
import typing
from lazy_object_proxy import Proxy
import functools

from .http import get as httpGet

def column2binary(pds, cn):
	nna=pds.loc[:, cn].notna()
	#print(cn, pds.loc[:, cn].unique(), nna.sum())
	s=pandas.Series(sorted(pds.loc[nna, cn].unique()))
	if not (len(s) == 2 or len(s) == 1):
		if s.dtype != np.float64 or not ((s<=1.) & (s >=0.)).all():
			raise ValueError(cn+": "+repr(s))
	else:
		pds.loc[nna, cn] = (pds.loc[nna, cn] == s[len(s)-1]).astype(float)

class Dataset():
	__slots__ = ("pds", "timesColumnName", "eventColumnName", "spec", "censorshipScore", "postProcessor", "isCensorship")
	
	
	def __init__(self, timesColumnName=None, eventColumnName=None, spec=None, postProcessor=None, isCensorship=None, pds=None):
		super().__init__()
		self.timesColumnName = timesColumnName
		self.eventColumnName = eventColumnName
		self.spec = spec
		self.postProcessor = postProcessor
		self.isCensorship = isCensorship
		self.censorshipScore = None
		if pds:
			self._init_data(pds)
		else:
			assert self.__class__._init_data.__code__.co_argcount == 1, "This class (`"+self._class__.__name__+"`) shouldn't be used directly (its `_init_data` requires params)"
			self.pds=Proxy(self._init_data)

	def _init_data(self, pds):
		#print(pds.head())
		if self.postProcessor:
			self.postProcessor(pds, self.timesColumnName, self.eventColumnName)
		isCensorship=self.isCensorship
		
		if self.eventColumnName:
			evtBool = None
			if self.isCensorship is None and self.timesColumnName:
				evtBool=pds.loc[:, self.eventColumnName].astype(bool)
				d=pds.loc[evtBool, self.timesColumnName]
				c=pds.loc[~evtBool, self.timesColumnName]
				md=d.mean()
				mc=c.mean()
				sd=d.std()
				sc=c.std()
				
				self.censorshipScore=(md-mc)/np.sqrt(sd*sc)
				
				isCensorship = self.censorshipScore > 0
				if isCensorship:
					warn("Censorship in `"+self.eventColumnName+"` detected heuristically (censorshipScore="+str(self.censorshipScore)+", d="+repr((md, sd))+", c="+repr((mc, sc))+"), would be transformed")
			
			if isCensorship:
				if evtBool is None:
					evtBool=self.pds.loc[:, self.eventColumnName].astype(bool)
				pds.loc[:, self.eventColumnName] = ~evtBool
		
		if self.spec:
			for cn, columnType in self.spec.items():
				if columnType == "binary":
					column2binary(pds, cn)
		return pds



class XYDataset(Dataset):
	def __init__(self, eventColumnName, spec=None, postProcessor=None, timesColumnName="duration", isCensorship=None):
		super().__init__(timesColumnName, eventColumnName, spec, postProcessor, isCensorship=isCensorship)
	
	def _init_data(self, covariates, duration):
		duration = pandas.Series(duration)
		duration.name = self.timesColumnName
		return super()._init_data(pandas.concat([covariates, duration], axis=1))
	


class XYZDataset(XYDataset):
	def __init__(self, spec=None, postProcessor=None, isCensorship=None):
		super().__init__(duration, None, spec, postProcessor, isCensorship=isCensorship)
		
	def _init_data(self, covariates, duration, event):
		event = pandas.Series(event).astype(bool)
		event.name = "event"
		return super()._init_data(pandas.concat([covariates, event], axis=1), duration)


class LifelinesDataset(Dataset):
	def __init__(self, func, timesColumnName, eventColumnName, spec=None, postProcessor=None, isCensorship=None):
		self.func=func
		super().__init__(timesColumnName, eventColumnName, spec, postProcessor, isCensorship=isCensorship)
	
	def _init_data(self):
		return super()._init_data(self.func())


class DecodingDataset(Dataset):
	def decode(self, src, timesColumnName, eventColumnName, spec, isCensorship=None):
		raise NotImplementedError()


class RemoteDataset(DecodingDataset):
	def _init_data(self):
		if isinstance(self.uri, (list, tuple)):
			for u in self.uri:
				try:
					src = httpGet(u)
					break
				except:
					warn("fetching "+uri+" has failed")
		else:
			src = httpGet(self.uri)
		pds, self.timesColumnName, self.eventColumnName, self.spec = self.decode(src, self.timesColumnName, self.eventColumnName, self.spec)
		return super()._init_data(pds)
	
	def __init__(self, uri, timesColumnName=None, eventColumnName=None, spec=None, postProcessor=None, isCensorship=None):
		self.uri=uri
		super().__init__(timesColumnName, eventColumnName, spec, postProcessor, isCensorship=isCensorship)


class ArffDatasetMixin:
	def decode(self, src, timesColumnName, eventColumnName, spec):
		import scipy.io.arff
		res = arff.loads(src)
		self.name = res["relation"]
		pds = pandas.DataFrame(res["data"])
		
		newColumns = [None]*len(res["attributes"])
		for i, (attrName, attrCat) in enumerate(res["attributes"]):
			newColumns[i] = attrName
			if isinstance(attrCat, list):
				if len(attrCat) == 2:
					pds.loc[:, i] = (pds.loc[:, i] == attrCat[1]).astype(bool)
					pass
				else:
					pass
			else:
				pds.loc[:, i] = pds.loc[:, i].astype(float)
		
		pds.columns = newColumns
		return pds, timesColumnName, eventColumnName, spec


class ArffRemoteDataset(ArffDatasetMixin, RemoteDataset):
	pass


class CSVDatasetMixin:
	def __init__(self, *args, sep=",", **kwargs):
		self.sep=sep
		super().__init__(*args, **kwargs)
	
	def decode(self, src, timesColumnName, eventColumnName, spec, **kwargs):
		from numpy import genfromtxt

		if "sep" not in kwargs:
			kwargs["sep"] = self.sep

		with StringIO(src) as f:
			pds = pandas.read_csv(f, **kwargs)

		return pds, timesColumnName, eventColumnName, spec


class CSVRemoteDataset(CSVDatasetMixin, RemoteDataset):
	pass


class RemoteXYDataset(XYDataset, DecodingDataset):
	def __init__(self, uriCovariates, uriDuration, timesColumnName=None, eventColumnName=None, spec=None, postProcessor=None, isCensorship=None):
		self.uriCovariates=uriCovariates
		self.uriDuration=uriDuration
		super().__init__(eventColumnName, spec, postProcessor, timesColumnName=timesColumnName, isCensorship=isCensorship)
	
	def _init_data(self):
		srcCovariates = httpGet(self.uriCovariates)
		srcDuration = httpGet(self.uriDuration)
		pdsCovariates, self.timesColumnName, self.eventColumnName, self.spec = self.decode(srcCovariates, self.timesColumnName, self.eventColumnName, self.spec)
		pdsDuration, self.timesColumnName, self.eventColumnName, self.spec = self.decode(srcDuration, self.timesColumnName, self.eventColumnName, self.spec)
		
		pdsDuration = pdsDuration.loc[:, self.timesColumnName]
		return super()._init_data(pdsCovariates, pdsDuration)

class CSVRemoteXYDataset(CSVDatasetMixin, RemoteXYDataset):
	pass



def openml2pandas(name):
	res = sklearn.datasets.openml.fetch_openml(name, target_column=None, data_home=".\datasets")
	# print(res.feature_names)
	dt = res.data
	if hasattr(dt, "toarray"):
		dt = dt.toarray()
	pds = pandas.DataFrame(dt, columns=res.feature_names)
	spec = Chassis.Chassis.specFromPandas(pds)
	for catName, cat in res.categories.items():
		if len(cat) == 2 and spec[catName] != "binary":
			spec[catName] = "binary"
			pds.loc[catName] = (pds.loc[catName] == cat[1]).astype(bool)
	res.data = None
	res.categories = None
	res.feature_names = None
	return pds, spec, res


class OpenMLDataset(Dataset):
	def _init_data(self):
		res = sklearn.datasets.openml.fetch_openml(self.name, version=version, target_column=None, data_home=dataHome)
		# print(res.feature_names)
		dt = res.data
		if hasattr(dt, "toarray"):
			dt = dt.toarray()
		pds = pandas.DataFrame(dt, columns=res.feature_names)
		return super()._init_data(pds)
	
	def __init__(self, name, timesColumnName=None, eventColumnName=None, spec=None, postProcessor=None, isCensorship=None, version='active', dataHome=None):
		self.name=name
		super().__init__(timesColumnName, eventColumnName, spec, postProcessor, isCensorship=isCensorship)


class RDatasetsDataset(Dataset):
	def _init_data(self):
		res = RDatasets.getDatasets(self.category, self.name, usePandas=True)
		self.columnsDescriptions = res.columnsDescriptions
		pds = res.X
		return super()._init_data(pds)
	
	def __init__(self, category, name, timesColumnName=None, eventColumnName=None, spec=None, postProcessor=None, isCensorship=None):
		#print("fetching "+name)
		self.category=category
		self.name=name
		self.columnsDescriptions = None
		super().__init__(timesColumnName, eventColumnName, spec, postProcessor, isCensorship=isCensorship)


def remapColumnsNames(ds, remapping):
	newColumns = list(ds.columns)
	for i, colName in enumerate(ds.columns):
		if colName in remapping:
			newColumns[i] = remapping[colName]
	ds.columns = newColumns

def remapColumn(pds, cn, mapping):
	nna=pds.loc[:, cn].notna()
	pds.loc[nna, cn] = pds.loc[nna, cn].map(lambda x: mapping[x])

def remapColumnsValues(pds, remapping):
	for cn, mapping in remapping.items():
		remapColumn(pds, cn, mapping)
	
def splitStrCathegoricalToBinary(pds, cn, separator="+"):
	childrenColz=set()
	def processor(x):
		nonlocal childrenColz
		el=set((s.strip() for s in x.split(separator)))
		childrenColz|=el
		return el
	
	splitted=pds[cn].map(processor)
	sorted(childrenColz)

	ress=[None]*len(splitted)
	for i, el in enumerate(splitted.iloc[:]):
		ress[i] = [col in el for col in childrenColz]
	
	childrenColz = ["ssctb("+cn+") -> "+enumV for enumV in childrenColz]
	
	res = pandas.DataFrame(ress, columns=childrenColz)
	for col in childrenColz:
		pds.loc[:, col] = res.loc[:, col]
	del(pds[cn])

def splitStrCathegoricalsToBinary(pds, specs):
	for cn, sep in specs.items():
		splitStrCathegoricalToBinary(pds, cn, sep)
