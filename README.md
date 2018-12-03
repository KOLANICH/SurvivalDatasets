SurvivalDatasets.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[wheel](https://gitlab.com/KOLANICH/SurvivalDatasets/-/jobs/artifacts/master/raw/wheels/SurvivalDatasets-0.CI-py3-none-any.whl?job=build)
[![PyPi Status](https://img.shields.io/pypi/v/SurvivalDatasets.svg)](https://pypi.python.org/pypi/SurvivalDatasets)
![GitLab Build Status](https://gitlab.com/KOLANICH/SurvivalDatasets/badges/master/pipeline.svg)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/SurvivalDatasets.svg?branch=master)](https://travis-ci.org/KOLANICH/SurvivalDatasets)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/SurvivalDatasets.svg)](https://coveralls.io/r/KOLANICH/SurvivalDatasets)
![GitLab Coverage](https://gitlab.com/KOLANICH/SurvivalDatasets/badges/master/coverage.svg)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/SurvivalDatasets.svg)](https://libraries.io/github/KOLANICH/SurvivalDatasets)

This is a module importing some survival datasets for measuring performance of survival models. Can be repurposed to import other kinds of datasets, but currently I have populated the DB only with survival ones.


Requirements
------------
* [`Python >=3.4`](https://www.python.org/downloads/). [```Python 2``` is dead, stop raping its corpse.](https://python3statement.org/) Use ```2to3``` with manual postprocessing to migrate incompatible code to ```3```. It shouldn't take so much time. For unit-testing you need Python 3.6+ or PyPy3 because their ```dict``` is ordered and deterministic.
* [`numpy`](https://github.com/numpy/numpy) ![Licence](https://img.shields.io/github/license/numpy/numpy.svg) [![PyPi Status](https://img.shields.io/pypi/v/numpy.svg)](https://pypi.python.org/pypi/numpy) [![TravisCI Build Status](https://travis-ci.org/numpy/numpy.svg?branch=master)](https://travis-ci.org/numpy/numpy) [![Libraries.io Status](https://img.shields.io/librariesio/github/numpy/numpy.svg)](https://libraries.io/github/numpy/numpy)
* [`pandas`](https://github.com/pandas-dev/pandas) ![Licence](https://img.shields.io/github/license/pandas-dev/pandas.svg) [![PyPi Status](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.python.org/pypi/pandas) [![TravisCI Build Status](https://travis-ci.org/pandas-dev/pandas.svg?branch=master)](https://travis-ci.org/pandas-dev/pandas) [![CodeCov Coverage](https://codecov.io/github/pandas-dev/pandas/coverage.svg?branch=master)](https://codecov.io/github/pandas-dev/pandas/) [![Libraries.io Status](https://img.shields.io/librariesio/github/pandas-dev/pandas.svg)](https://libraries.io/github/pandas-dev/pandas) [![Gitter.im](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pydata/pandas)
* [`requests`](https://github.com/requests/requests) [![PyPi Status](https://img.shields.io/pypi/v/requests.svg)](https://pypi.python.org/pypi/requests) [![Libraries.io Status](https://img.shields.io/librariesio/github/requests/requests.svg)](https://libraries.io/github/requests/requests)
* [`scikit-learn`](https://github.com/scikit-learn/scikit-learn) [![PyPi Status](https://img.shields.io/pypi/v/scikit-learn.svg)](https://pypi.python.org/pypi/scikit-learn) [![Libraries.io Status](https://img.shields.io/librariesio/github/scikit-learn/scikit-learn.svg)](https://libraries.io/github/scikit-learn/scikit-learn)
