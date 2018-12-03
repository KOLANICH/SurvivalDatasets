#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
sys.path.append(str(Path(__file__).parent.absolute()))

from collections import OrderedDict
dict=OrderedDict

import pandas
from pandas.testing import assert_frame_equal, assert_series_equal
from Chassis import Chassis

class SimpleTests(unittest.TestCase):
	def setUp(self):
		from SurvivalDatasets.datasets import datasets
		self.datasets = datasets

	def testChassisSchemaCorrecttness(self):
		for dsName, ds in self.datasets.items():
			with self.subTest(dsName=dsName):
				if ds.spec:
					Chassis(ds.spec, ds.pds)
				else:
					print(repr(dsName), ":", Chassis.specFromPandas(ds.pds))

if __name__ == "__main__":
	unittest.main()
