from . import *

from lifelines.datasets import *

import lazily.roman


def postProcessDemocracy(ds, timesColumnName, eventColumnName):
	ds.loc[:, "democracy"] = ds.loc[:, "democracy"] == "Non-democracy"


def postProcessStartStop(pds, timesColumnName, eventColumnName):
	pds.loc[:, "T"] = pds.loc[:, "stop"] - pds.loc[:, "start"]


def postProcessRecur(pds, timesColumnName, eventColumnName):
	remapColumnsNames(pds, {'CENSOR': "E"})
	pds.loc[:, "T"] = pds.loc[:, "TIME1"] - pds.loc[:, "TIME0"]


def postProcessHeartTransplant(pds, timesColumnName, eventColumnName):
	pds.loc[:, "T"] = pds.loc[:, "stop"] - pds.loc[:, "start"]


def postProcessEucalyptus(pds, timesColumnName, eventColumnName):
	maxSurv = pds.loc[:, timesColumnName].max()
	pds.loc[:, eventColumnName] = pds.loc[:, timesColumnName].notna()
	pds.loc[~pds.loc[:, eventColumnName], timesColumnName] = maxSurv


def postProcessThoracicSurgery(pds, timesColumnName, eventColumnName):
	remapColumnsNames(pds, {
		'V1': "Diagnosis",# - specific combination of ICD-10 codes for primary and secondary as well multiple tumours if any (DGN3,DGN2,DGN4,DGN6,DGN5,DGN8,DGN1)
		'V2': "Forced vital capacity",  # - FVC (numeric)
		
		'V3': "Volume exhaled",# Volume that has been exhaled at the end of the first second of forced expiration - FEV1 (numeric)
		
		'V4': "Performance status",# Performance status - Zubrod scale (PRZ2,PRZ1,PRZ0)
		'V5': "Pain before surgery",  # bool
		'V6': "Haemoptysis before surgery",  # bool
		'V7': "Dyspnoea before surgery",  # bool
		'V8': "Cough before surgery",  # bool
		'V9': "Weakness before surgery",  # bool
		
		'V10': "size of the original tumour",# from OC11 (smallest) to OC14 (largest) (OC11,OC14,OC12,OC13)
		'V11': "diabetes mellitus",  # bool
		'V12': "MI up to 6 months",
		'V13': "PAD - peripheral arterial diseases",
		'V14': "Smoking",  # bool
		'V15': "Asthma",  # bool
		'V16': "Age",  # at surgery (numeric)
		'Class': "died" # within 1 year
	})
	pds.loc[:, "T"]=1 # year


def postProcessAIDS(pds, timesColumnName, eventColumnName):
	remapColumnsNames(
		pds,
		{
			"time": "time_to_diagnosis_or_death",
			"censor": "diagnosis_or_death_occured",
			"time_d": "time_to_death",
			"censor_d": "death_occured",
		}
	)
	remapColumnsValues(pds,
		{
			"txgrp":{"1":"ZDV + 3TC", "2":"ZDV + 3TC + IDV", "3":"d4T + 3TC", "4":"d4T + 3TC + IDV"},
			"raceth":{"1":"White Non-Hispanic", "2":"Black Non-Hispanic", "3":"Hispanic (regardless of race)", "4":"Asian, Pacific Islander", "5":"American Indian, Alaskan Native", "6": "Other/unknown"},
			"ivdrug":{"1":"Never", "2":"Currently", "3":"Previously"},
		}
	)
	
	splitStrCathegoricalsToBinary(pds, {"txgrp": "+"})

def showColumns(pds, timesColumnName, eventColumnName):
	print(pds.columns, timesColumnName in pds.columns, eventColumnName in ds.columns)

def postProcessCGD(pds, timesColumnName, eventColumnName):
	pds.loc[:, "T"] = pds.loc[:, "tstop"] - pds.loc[:, "tstart"]


sksurvDSBase = "https://raw.githubusercontent.com/sebp/scikit-survival/master/sksurv/datasets/data/"
shapDSBase = "https://raw.githubusercontent.com/slundberg/shap/master/data/"


def postProcessNHANES1(pds, timesColumnName, eventColumnName):
	pds.loc[:, eventColumnName] = pds.loc[:, timesColumnName] > 0
	pds.loc[:, timesColumnName] = abs(pds.loc[:, timesColumnName])

def postProcessBladder(pds, timesColumnName, eventColumnName):
	postProcessStartStop(pds)
	pds.loc[:, "E"] = pds.loc[:, "status"] >= 1

def postProcessPBC(pds, timesColumnName, eventColumnName):
	pds.loc[:, "E"] = pds.loc[:, "status"] == 2
	remapColumnsValues(pds, {"trt":{1:1, 2:0}})

def postProcessPBCSEQ(pds, timesColumnName, eventColumnName):
	pds.loc[:, "E"] = pds.loc[:, "status"] == 2

def postProcessGBSG2(pds, timesColumnName, eventColumnName):
	remapColumnsNames(pds, {'cens': "E"})
	pds.loc[:, "tgrade"] = pds.loc[:, "tgrade"].map(lazily.roman.fromRoman)

def postProcessLymphoma(pds, timesColumnName, eventColumnName):
	remapColumnsNames(pds, {'Censor': "E"})

def postProcessEchoMonths(pds, timesColumnName, eventColumnName):
	pds.loc[:, "E"] = ~pds.loc[:, "still_alive"]

def preprocessHolyMollyPolly(pds, timesColumnName, eventColumnName):
	pds.loc[:, "E"] = True

def preprocessRTransplant(pds, timesColumnName, eventColumnName):
	pds.loc[:, "event"] = pds.loc[:, "event"] == "death"

def preprocessColon(pds, timesColumnName, eventColumnName):
	remapColumnsValues(pds, {"extent":{1:"submucosa", 2:"muscle", 3:"serosa", 4:"contiguous structures"}})
	splitStrCathegoricalsToBinary(pds, {"rx": "+"})

def postProcessNcog(pds, timesColumnName, eventColumnName):
	remapColumnsNames(pds, {'arm': "treatment"})

def postProcessHNCancer(pds, timesColumnName, eventColumnName):
	pds.loc[:, "tumor_stage"] = pds.loc[:, "tumor_stage"].map(lazily.roman.fromRoman)

def postProcessGolubEUP(pds, timesColumnName, eventColumnName):
	pds.loc[:, "T"] = pds.loc[:, "end"] - pds.loc[:, "begin"]


n='numerical'
b='binary'
c="categorical"
s="stop"
lungCancerSpec={
	'OS_event': b,
	'OS_years': n,
	'age': n,
	'g_201938_at': n,
	'g_202387_at': n,
	'g_202454_s_at': n,
	'g_203967_at': n,
	'g_203968_s_at': n,
	'g_204531_s_at': n,
	'g_204890_s_at': n,
	'g_204891_s_at': n,
	'g_204979_s_at': n,
	'g_206924_at': n,
	'g_206926_s_at': n,
	'g_211475_s_at': n,
	'g_211851_x_at': n,
	'g_212724_at': n,
	'g_214088_s_at': n,
	'g_215638_at': n,
	'g_216010_x_at': n,
	'g_AFFX.HUMGAPDH.M33197_5_at': n,
	'g_AFFX.HUMGAPDH.M33197_M_at': n,
	'histology': n,
	'sex': b
}

lungAndCancerSpec={
	'inst': n,
	'time': n,
	'status': n,
	'age': n,
	'sex': b,
	'ph.ecog': n,
	'ph.karno': n,
	'pat.karno': n,
	'meal.cal': n,
	'wt.loss': n
}

# todo: https://www.nature.com/articles/s41467-017-02465-5
# todo: https://github.com/wkzs111/phm-ieee-2012-data-challenge-dataset https://github.com/Lucky-Loek/ieee-phm-2012-data-challenge-dataset
# todo: http://data-acoustics.com/measurements/bearing-faults/
# todo: https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/
# todo: https://csegroups.case.edu/bearingdatacenter/pages/download-data-file
# todo: http://data-acoustics.com/measurements/bearing-faults/bearing-3/
# todo: http://data-acoustics.com/measurements/bearing-faults/bearing-1/
# todo: https://mfpt.org/fault-data-sets/
# todo: RDatasetsDataset("KMsurv", ..., None, None, isCensorship=None),

datasets = {
	#TODO:
	#"nh4": LifelinesDataset(load_nh4, 'time', 'E', None, None, isCensorship=False),
	#"lupus": LifelinesDataset(load_lupus, 'time', 'E', None, None, isCensorship=False),
	
	
	# "gbsg2": ArffRemoteDataset(sksurvDSBase+"GBSG2.arff", 'time', 'E', None, postProcessGBSG2)
	"gbsg2": LifelinesDataset(load_gbsg2, 'time', 'E', {
		"horTh": b,
		"age": n,
		"menostat": b,
		"tsize": n,
		"tgrade": n,
		"pnodes": n,
		"progrec": n,
		"estrec": n,
		"time": n,
		"E": b
	}, postProcessGBSG2, isCensorship=False),
	
	"aids": ArffRemoteDataset(sksurvDSBase+"actg320.arff", "time_to_death", "death_occured", {
		"time_to_diagnosis_or_death": n,
		"diagnosis_or_death_occured": s,
		"time_to_death": n,
		"death_occured": s,
		"tx": s,
		#"txgrp": c,
		"ssctb(txgrp) -> ZDV" :b,
		"ssctb(txgrp) -> 3TC" :b,
		"ssctb(txgrp) -> IDV" :b,
		"ssctb(txgrp) -> d4T" :b,
		"strat2": s,
		'sex': b,
		"raceth": c,
		"ivdrug": c,
		"hemophil": s,
		"karnof": n,
		"cd4": n,
		"priorzdv": n,
		"age": n
	}, postProcessAIDS, isCensorship=False),
	
	#"aids2": RDatasetsDataset("MASS", 'Aids2', None, None, None, isCensorship=False) #MASS Aids2 Australian AIDS Survival Data (AIDS2) - TODO: check that it is not from sksurv
	
	# "breast_cancer": ArffRemoteDataset(sksurvDSBase+"breast_cancer_GSE7390-metastasis.arff", "t.tdm", "e.tdm"),
	
	#"veteran": ArffRemoteDataset(sksurvDSBase+"veteran.arff", "Survival_in_days", "Status", isCensorship=False),
	"veteran": OpenMLDataset("veteran", "Survival", "Status", {
		"Treatment": b,
		"Celltype": n,
		"Survival": n,
		"Status": b,
		"Karnofsky_score": n,
		"Months_from_Diagnosis": n,
		"Age": n,
		"Prior_therapy": b
	}, version=1, isCensorship=False),
	#'veteran': RDatasetsDataset("survival", 'veteran', "time", "status", isCensorship=False),
	
	"whas500": ArffRemoteDataset(sksurvDSBase+"whas500.arff", "lenfol", "fstat", {
		"age": n,
		"gender": s,
		"hr": n,
		"sysbp": n,
		"diasbp": n,
		"bmi": n,
		"cvd": s,
		"afb": s,
		"sho": s,
		"chf": s,
		"av3": s,
		"miord": s,
		"mitype": s,
		"los": n,
		"lenfol": n,
		"fstat": s
	}, isCensorship=False),
	
	"canadian_senators": LifelinesDataset(load_canadian_senators, 'diff_days', 'observed', {
		"Name": s,
		"Political Affiliation at Appointment": c,
		"Province / Territory": c,
		"Appointed on the advice of": s,
		"Term (yyyy.mm.dd)": s,
		"start_date": s,
		"end_date": s,
		"reason": s,
		"diff_days": n,
		"observed": s
	}, isCensorship=False), #
	"democracy": LifelinesDataset(load_dd, 'duration', 'observed',
		{
			'ctryname': c,
			'cowcode2': s,
			'politycode': s,
			'un_region_name': c,
			'un_continent_name': c,
			'ehead': s,
			'leaderspellreg': s,
			'democracy': b,
			'regime': c,
			'start_year': n,
			'duration': n,
			'observed': b
		},
		postProcessDemocracy,
		isCensorship=False
	),
	"dfcv": LifelinesDataset(load_dfcv, "T", "event", {
		"start": n,
		"group": b,
		"z": b,
		s: n,
		"event": s,
		"T": n
	}, postProcessStartStop, isCensorship=False),
	"g3": LifelinesDataset(load_g3, 'time', 'event', {
		"no.": n,
		"age": n,
		'sex': b,
		"histology": c,
		"group": c,
		"event": s,
		"time": n
	}, isCensorship=False),
	
	"holly_molly_polly": LifelinesDataset(load_holly_molly_polly, "T", "E", {
		"ID": c,
		"Status": n,
		"Stratum": n,
		"Start(days)": n,
		"Stop(days)": n,
		"tx": b,
		"T": n,
		"E": s
	}, preprocessHolyMollyPolly, isCensorship=False),
	"kidney_transplant": LifelinesDataset(load_kidney_transplant, 'time', 'death', {
		"time": n,
		"death": b,
		"age": n,
		"black_male": b,
		"white_male": b,
		"black_female": b
	}, isCensorship=False),
	'kidney': RDatasetsDataset("survival", 'kidney', "time", "status", {
		"time": n,
		"status": b,
		"age": n,
		'sex': b,
		"disease": c,
		"frail": n
	}, isCensorship=False),
	
	"larynx": LifelinesDataset(load_larynx, 'time', 'death', {
		"time": n,
		"age": n,
		"death": b,
		"Stage II": b,
		"Stage III": b,
		"Stage IV": b
	}, isCensorship=False),
	
	"lcd": LifelinesDataset(load_lcd, 'T', 'C', {
		"C": b,
		"T": n,
		"group": c
	}, isCensorship=False),
	
	'leukemia': RDatasetsDataset("survival", 'leukemia', 'time', 'status', {
		"time": n,
		"status": b,
		"x": c
	}, isCensorship=False),
	"leukemia_lifelines": LifelinesDataset(load_leukemia, 't', 'status', {
		"t": n,
		"status": b,
		"sex": b,
		"logWBC": n,
		"Rx": b
	}, isCensorship=False),
	
	"lung": LifelinesDataset(load_lung, 'time', 'status', lungAndCancerSpec, isCensorship=False), # NorthCentral Cancer Treatment Group (NCCTG) Lung Cancer Data (LC)
	# 'lung': RDatasetsDataset("survival", 'lung', 'time', 'status', lungAndCancerSpec, isCensorship=False),
	'cancer': RDatasetsDataset("survival", 'cancer', 'time', 'status', lungAndCancerSpec, isCensorship=False), # NorthCentral Cancer Treatment Group (NCCTG) Lung Cancer Data (LC) too
	
	"lymphoma": LifelinesDataset(load_lymphoma, 'Time', 'E', {
		"Stage_group": n,
		"Time": n,
		"E": b
	}, postProcessLymphoma, isCensorship=False),
	
	"psychiatric_patients": LifelinesDataset(load_psychiatric_patients, 'T', 'C', {
		"Age": n,
		"T": n,
		"C": b,
		'sex': b
	}, isCensorship=False), # https://books.google.ru/books?id=3q_NBQAAQBAJ&pg=PA206
	"recur": LifelinesDataset(load_recur, "T", "E", {
		"AGE": n,
		"TREAT": b,
		"TIME0": n,
		"TIME1": n,
		"E": b,
		"EVENT": n,
		"T": n
	}, postProcessRecur, isCensorship=False),
	"artifical_regression": LifelinesDataset(load_regression_dataset, 'T', 'E', {
		"var1": n,
		"var2": n,
		"var3": n,
		"T": n,
		"E": b
	}, isCensorship=False),
	
	"rossi": LifelinesDataset(load_rossi, 'week', 'arrest', {
		'fin': b,
		'age': n,
		'race': b,
		'wexp': b,
		'mar': b,
		'paro': b,
		'prio': n,
		
		'week': n,
		'arrest': b,
	}, isCensorship=False),
	"heart": LifelinesDataset(
		load_stanford_heart_transplants, "T", "event",
		{
			'start': s,
			s: s,
			'event': b,
			'age': n,
			'year': n,
			'surgery': b,
			'transplant': b,
			'id': s,
			'T': n
		},
		postProcessHeartTransplant,
		isCensorship=False
	), # Stanford HeartTransplant Data (HT)
	#'heart': RDatasetsDataset("survival", 'heart', None, None, isCensorship=False),
	
	"waltons": LifelinesDataset(load_waltons, "T", "E", {
		"T": n,
		"E": b,
		"group": c
	}, isCensorship=False),
	
	"eucalyptus": OpenMLDataset("eucalyptus", "Surv", "E", {
		"Abbrev": n,
		"Rep": n,
		"Locality": n,
		"Map_Ref": n,
		"Latitude": n,
		"Altitude": n,
		"Rainfall": n,
		"Frosts": n,
		"Year": n,
		"Sp": n,
		"PMCno": n,
		"DBH": n,
		"Ht": n,
		"Surv": n,
		"Vig": n,
		"Ins_res": n,
		"Stem_Fm": n,
		"Crown_Fm": n,
		"Brnch_Fm": n,
		"Utility": n,
		"E": s
	}, postProcessEucalyptus, version=1, isCensorship=False),
	'pbc': RDatasetsDataset("survival", 'pbc', "time", "status", {
		"time": n,
		"status": n,
		"trt": b,
		"age": n,
		"sex": b,
		"ascites": b,
		"hepato": b,
		"spiders": b,
		"edema": b,
		"bili": n,
		"chol": n,
		"albumin": n,
		"copper": n,
		"alk.phos": n,
		"ast": n,
		"trig": n,
		"platelet": n,
		"protime": n,
		"stage": n,
		"E": s
	}, postProcessPBC, isCensorship=False),
	"pbcseq": OpenMLDataset("pbcseq", "number_of_days", "E", {
		'number_of_days': n,
		'status': s,
		'drug': b,
		'age': n,
		'sex': b,
		'day': n,
		'presence_of_asictes': b,
		'presence_of_hepatomegaly': b,
		'presence_of_spiders': b,
		'presence_of_edema': b,
		'serum_bilirubin': n,
		'serum_cholesterol': n,
		'albumin': n,
		'alkaline_phosphatase': n,
		'SGOT': n,
		'platelets': n,
		'prothrombin_time': n,
		'histologic_stage_of_disease': n,
		"E": b
	}, postProcessPBCSEQ, version=1, isCensorship=False),
	
	"thoracic-surgery": OpenMLDataset("thoracic-surgery", "T", "died", {
		"Diagnosis": c,
		"Forced vital capacity": n,
		"Volume exhaled": n,
		"Performance status": c,
		"Pain before surgery": b,
		"Haemoptysis before surgery": b,
		"Dyspnoea before surgery": b,
		"Cough before surgery": b,
		"Weakness before surgery": b,
		"size of the original tumour": n,
		"diabetes mellitus": b,
		"MI up to 6 months": b,
		"PAD - peripheral arterial diseases": b,
		"Smoking": b,
		"Asthma": b,
		"Age": n,
		"died": b,
		"T": n
	}, postProcessThoracicSurgery, isCensorship=False),
	"echoMonths": OpenMLDataset("echoMonths", "class", "still_alive", {
		"still_alive": s,
		"age": n,
		"pericardial": b,
		"fractional": n,
		"epss": n,
		"lvdd": n,
		"wall_score": n,
		"wall_index": n,
		"alive_at_1": b,
		"class": n
	}, version=1, isCensorship=True),
	
	"lungcancer_GSE31210": OpenMLDataset("lungcancer_GSE31210", "OS_years", "OS_event", lungCancerSpec, isCensorship=False),
	"lungcancer_shedden": OpenMLDataset("lungcancer_shedden", "OS_years", "OS_event", lungCancerSpec, isCensorship=False),
	
	#"hcc": OpenMLDataset("hcc-dataset", None, "Class", {}, None, isCensorship=True), #time is 1 year
	
	'bladder': RDatasetsDataset("survival", 'bladder', s, "event", {
		"rx": n,
		"number": n,
		"size": n,
		s: n,
		"event": b,
		"enum": n
	}, isCensorship=False),
	'cgd': RDatasetsDataset("survival", 'cgd', "T", "status", {
		"center": s,
		"hos.cat": s,
		"random": s,
		"treat": b,
		"sex": b,
		"age": n,
		"height": n,
		"weight": n,
		"inherit": b,
		"steroids": b,
		"propylac": b,
		"tstart": s,
		"enum": n,
		"tstop": s,
		"status": b,
		"T": n
	}, postProcessCGD, isCensorship=False),
	'colon': RDatasetsDataset("survival", 'colon', "time", "status", {
		"id": s,
		#"study": n,
		#"rx": c,
		'ssctb(rx) -> 5FU': b,
		'ssctb(rx) -> Lev': b,
		'ssctb(rx) -> Obs': b,
		"sex": b,
		"age": n,
		"obstruct": b,
		"perfor": b,
		"adhere": b,
		"nodes": n,
		"status": b,
		"differ": n,
		"extent": c,#numerical
		"surg": b,
		"node4": b,
		"time": n,
		"etype": s # 1=recurrence,2=death
	}, preprocessColon, isCensorship=False),
	'flchain': RDatasetsDataset("survival", 'flchain', "futime", "death", {
		"age": n,
		'sex': b,
		"sample.yr": n,
		"kappa": n,
		"lambda": n,
		"flc.grp": n,
		"creatinine": n,
		"mgus": b,
		"futime": n,
		"death": b,
		#"chapter": s #primary cause of death
	}, isCensorship=False),
	'genfan': RDatasetsDataset("survival", 'genfan', "hours", "status", {
		"hours": n,
		"status": b
	}, isCensorship=False),
	'mgus': RDatasetsDataset("survival", 'mgus', "futime", "death", {
		"age": n,
		'sex': b,
		"dxyr": n,
		"pcdx": c,
		"pctime": n,
		"futime": n,
		"death": b,
		"alb": n,
		"creat": n,
		"hgb": n,
		"mspike": n
	}, isCensorship=False),
	'mgus2': RDatasetsDataset("survival", 'mgus2', "futime", "death", {
		"age": n,
		'sex': b,
		"hgb": n,
		"creat": n,
		"mspike": n,
		"ptime": n,
		"pstat": b,
		"futime": n,
		"death": b
	}, isCensorship=False),
	'myeloid': RDatasetsDataset("survival", 'myeloid', "futime", "death", {
		"trt": c,
		"futime": n,
		"death": b,
		"txtime": n,
		"crtime": s, #numerical
		"rltime": s #numerical
	}, isCensorship=False),
	'nwtco': RDatasetsDataset("survival", 'nwtco', "rel", "edrel", {
		"seqno": n,
		"instit": n,
		"histol": n,
		"stage": n,
		"study": n,
		"rel": b,
		"edrel": n,
		"age": n,
		"insubcohort": s
	}, isCensorship=False),
	'ovarian': RDatasetsDataset("survival", 'ovarian', "futime", "fustat", {
		"futime": n,
		"fustat": b,
		"age": n,
		"resid.ds": n,
		"rx": n,
		"ecog.ps": n
	}, isCensorship=False),
	'rats': RDatasetsDataset("survival", 'rats', "time", "status", {
		"litter": n,
		"rx": b,
		"time": n,
		"status": b,
		'sex': b
	}, isCensorship=False),
	'retinopathy': RDatasetsDataset("survival", 'retinopathy', "futime", "status", {
		"laser": b,
		"eye": b,
		"age": n,
		"type": b,
		"trt": b,
		"futime": n,
		"status": b,
		"risk": n
	}, isCensorship=False),
	'stanford2': RDatasetsDataset("survival", 'stanford2', "time", "status", {
		"id": s,
		"time": n,
		"status": b,
		"age": n,
		"t5": n
	}, isCensorship=False),
	'transplant': RDatasetsDataset("survival", 'transplant', "futime", "event", {
		"age": n,
		'sex': b,
		"abo": c,
		"year": n,
		"futime": n,
		"event": s
	}, preprocessRTransplant, isCensorship=False),
	
	#'logan': RDatasetsDataset("survival", 'logan', None, None), #WTF, it seems to be non-survival dataset
	#'rhDNase': RDatasetsDataset("survival", 'rhDNase', None, None), # where is censorship?
	#'solder': RDatasetsDataset("survival", 'solder', None, None), #WTF
	#'tobin': RDatasetsDataset("survival", 'tobin', None, None), #WTF
	#'uspop2': RDatasetsDataset("survival", 'uspop2', None, None), # seems to be counts of persons of different sexes in US populations per years
	
	#TODO:
	#"aircondit": RDatasetsDataset("boot", "aircondit", None, None, isCensorship=None),
	#"aircondit7": RDatasetsDataset("boot", "aircondit7", None, None, isCensorship=None),
	#"hirose", RDatasetsDataset("boot", "hirose", None, None, isCensorship=None),
	#"pistonrings": RDatasetsDataset("HSAUR", "pistonrings", None, None, isCensorship=None),
	#"Space_Shuttle_O-rings": RDatasetsDataset("vcd" ,"SpaceShuttle", None, None, isCensorship=None),
	#"LeveeFailures_Mississippi": RDatasetsDataset("Stat2Data", "LeveeFailures", None, None, isCensorship=None),
	
	"NHANES_1": CSVRemoteXYDataset(
		shapDSBase+"NHANESI_subset_X.csv", shapDSBase+"NHANESI_subset_y.csv", "y", 'E',
		{
			'Age': n,
			'Diastolic BP': n,
			'Poverty index': n,
			'Race': c,
			'Red blood cells': n,
			'Sedimentation rate': n,
			'Serum Albumin': n,
			'Serum Cholesterol': n,
			'Serum Iron': n,
			'Serum Magnesium': n,
			'Serum Protein': n,
			'Sex': b,
			'Systolic BP': n,
			'TIBC': n,
			'TS': n,
			'White blood cells': n,
			'BMI': n,
			'Pulse pressure': n,
			"death": s,
			'y': n,
		},
		postProcessNHANES1,
		isCensorship=False
	),

	"gbsc":CSVRemoteDataset("https://raw.githubusercontent.com/bsbarkur/gbcs-analysis/master/gbcs.csv", "survtime", "censrec",
		{
			"diagdateb": s,
			"recdate": s,
			"deathdate": s,
			"age": n,
			"menopause": b,
			"hormone": b,
			"size": n,
			"grade": c,
			"nodes": n,
			"prog_recp": n,
			"estrg_recp": n,
			"rectime": n,
			"censrec": b,
			"survtime": n,
			"censdead": s #b
		}
	),
	#"prothro":CSVRemoteDataset("https://xobemid.stata.com/books/prothro.dat", None, None, None), # non-survival
	"prothros":CSVRemoteDataset("https://xobemid.stata.com/books/prothros.dat", "time", "death",
		{
			"id": s,
			"N": s,
			"treat": b,
			"time": n,
			"death": b,
		},
		sep="\t",
		isCensorship=False,
	),

	 # TODO: there are more datasets in this dir
	"ncog": CSVRemoteDataset(
		("https://web.stanford.edu/%7Ehastie/CASI_files/DATA/ncog.txt", "https://raw.githubusercontent.com/ermeel86/paramaetricsurvivalmodelsinstan/master/data/ncog.txt"), "t", "d",
		{
			'day': n,
			'month': n,
			'year': n,
			't': n,
			'd': b,
			'treatment': b
		},
		postProcessNcog, sep = " ", isCensorship = False
	),
	"pediatric_cancer": CSVRemoteDataset(
		("https://web.stanford.edu/%7Ehastie/CASI_files/DATA/pediatric.txt", "https://raw.githubusercontent.com/ermeel86/paramaetricsurvivalmodelsinstan/master/data/pediatric.txt"), "t", "d",
		{
			'sex': b,
			'race': b,
			'age': n,
			'entry': s,
			'far': n,
			't': n,
			'd': b
		},
	sep = " ", isCensorship = False, ),
	 # "nflrb": CSVRemoteDataset("https://raw.githubusercontent.com/johnrandazzo/surv_nflrb/master/nflrb_data.csv", None, None, None),
	 # "MESS": CSVRemoteDataset("https://raw.githubusercontent.com/suziebrown/survival/master/MESSdat.csv", None, None, None),
	 # "plants": CSVRemoteDataset("https://raw.githubusercontent.com/fcdidone/survival/master/c.csv", None, None, None),
	"HN_cancer": CSVRemoteDataset(
		"https://raw.githubusercontent.com/TomBelbin/SurvivalApp/master/HNpatientdata.csv", "survival_month", "survival_status",
		{
			'hn_id': c,
			'age': n,
			'AgeGroup': c,
			'gender': b,
			'race': c,
			'ethnicity': c,
			'tumor_site': c,
			'current_smoker': b,
			'current_drinker': b,
			'survival_status': b,
			'survival_month': n,
			'DOD_status': b,
			'Overall_status': b,
			'tumor_stage': n,
			'node_status': b,
			'treatment': c
		},
		postProcessHNCancer, isCensorship = False
	),
	"rafiee": CSVRemoteDataset(
		"https://raw.githubusercontent.com/RRafiee/SurvivalAnalysis/master/survivaldata.csv", "OS_Time", "OS_YN",
		{
			'OS_Time': n,
			'OS_YN': b,
			'Variable1': n,
			'Variable2': n
		},
		isCensorship = False
	),
	"unemployment": CSVRemoteDataset(
		"https://raw.githubusercontent.com/tsheezy917/survivalmodel/master/survival_unemployment.csv", None, None,
		{
			'spell': n,
			'event': b,
			'censor2': b,
			'censor3': b,
			'censor4': b,
			'ui': b,
			'reprate': n,
			'logwage': n,
			'tenure': n,
			'disrate': n,
			'slack': b,
			'abolpos': b,
			'explose': b,
			'stateur': n,
			'houshead': b,
			'married': b,
			'female': b,
			'child': b,
			'ychild': b,
			'nonwhite': b,
			'age': n,
			'schlt12': b,
			'schgt12': b,
			'smsa': b,
			'bluecoll': b,
			'mining': b,
			'constr': b,
			'transp': b,
			'trade': b,
			'fire': b,
			'services': b,
			'pubadmin': b,
			'year85': b,
			'year87': b,
			'year89': b,
			'midatl': b,
			'encen': b,
			'wncen': b,
			'southatl': b,
			'escen': b,
			'wscen': b,
			'mountain': b,
			'pacific': b
		},
		isCensorship = False
	),
	"Ina": CSVRemoteDataset(
		"https://raw.githubusercontent.com/Hagkaup/Rprojects/master/Ina.csv", "DeathTime", "censor",
		{
			'Sex': b,
			'Genotype': c,
			'Vial': n,
			'DeathTime': n,
			'censor': b
		}
	),
	"shapesplosion": CSVRemoteDataset(
		"https://raw.githubusercontent.com/eshjain/SurvivalAnalysis403/master/PerfectionFlash_data%20(8).csv", "timeUsed", None,
		{
			'v1label': n,
			'v1value': n,
			'v2label': n,
			'v2value': n,
			'v3label': n,
			'v3value': n,
			'numShapes': n,
			'matchingScheme': c,
			'requestedTime': n,
			'timeUsed': n,
			'timerDisplay': n,
			'numErrors': n,
			'shapesMatched': n,
			'proximityValue': n,
			'timestamp': c
		},
	isCensorship = False
	),
	# "Telco_Customer_Churn_2015": CSVRemoteDataset(
		# "https://raw.githubusercontent.com/CAJan93/survivalAnalysisDemo/master/telco_customer_churn.csv", "tenure", "Churn",
		# {
			# 'gender': c,
			# 'SeniorCitizen': b,
			# 'Partner': c,
			# 'Dependents': c,
			# 'tenure': n,
			# 'PhoneService': c,
			# 'MultipleLines': c,
			# 'InternetService': c,
			# 'OnlineSecurity': c,
			# 'OnlineBackup': c,
			# 'DeviceProtection': c,
			# 'TechSupport': c,
			# 'StreamingTV': c,
			# 'StreamingMovies': c,
			# 'Contract': c,
			# 'PaperlessBilling': c,
			# 'PaymentMethod': c,
			# 'MonthlyCharges': n,
			# 'TotalCharges': c,
			# 'Churn': b
		# },
		# isCensorship = False
	# ),
	"alumni_association_membership": CSVRemoteDataset(
		"https://raw.githubusercontent.com/kartucson/AlumniMembership_SurvivalAnalysis/master/ProcessedData.csv", "dtm", "cens",
		{
			'CnBio_ID': s,
			'CnBio_Age': n,
			'CnBio_Ethnicity': c,
			'CnBio_Gender': b,
			'CnPrAl_Date_graduated': c,
			'CnMem_1_01_Date_Joined': s,
			'Days_to_membership': n,
			'CnPrAl_Degree': c,
			'Degree_level': c,
			'CnPrAlAttrCat_1_01_Description': c,
			'CnPrAlAttrCat_1_02_Description': n,
			'CnPrBs_Industry': c,
			'CnAdrPrf_City': c,
			'CnAdrPrf_County': c,
			'CnAdrPrf_State': c,
			'CnAdrPrf_ContryLongDscription': c,
			'CnSmryEdu_Total_Educations': n,
			'CnMem_1_01_Consecutive_Years': n,
			'CnMem_1_01_Standing': c,
			'CnMem_1_01_Total_Years': n,
			'CnMem_1_01_Last_Dropped_Date': s,
			'CnMem_1_01_Cur_Expires_on': c,
			'Type_membership': c,
			'CnMem_1_01_AtrCat_1_01_Description': c,
			'CnGf_1_01_Fnds_1_01_Description': c,
			'CnGf_1_01_Apls_1_01_Ap_Description': c,
			'CnGf_1_01_Pks_1_01_Package_ID': s,
			'CnGf_1_01_Pks_1_01_Description': c,
			'CnGf_1_01_Pks_1_01_Description.1': c,
			'Membership_desc': c,
			'Gdate': c,
			'Gmonth': c,
			'Gyear': n,
			'Mdate': s,
			'Mmonth': n,
			'Myear': n,
			'degree_full': c,
			'stateF': c,
			'state': c,
			'Ethnicity': c,
			'Age': n,
			'one': n,
			'Same_day': n,
			'Same_classroom_same_day': n,
			'surv': c,
			'dtm': n,
			'cens': b,
			'group': b,
			'GraduationPeriod': c,
			'time': n,
			'Gender': c,
			'Same_city_members': s,
			'Same_degree_year_members': s
		},
		isCensorship = False,
	),
	 # "possums9": CSVRemoteDataset("https://raw.githubusercontent.com/geobro1992/AMBBIS-SURV/master/hetage/poss9.txt", None, None, None),
	"GolubEUP": CSVRemoteDataset(
		"https://raw.githubusercontent.com/christophergandrud/simPH/master/data/GolubEUPData.tab", "T", "event",
		{
			'obs': n,
			'caseno': s,
			'begin': s,
			'end': s,
			'event': b,
			'backlog': n,
			'agenda': b,
			'qmv': b,
			'qmvpostsea': b,
			'qmvpostteu': b,
			'coop': b,
			'codec': b,
			'eu9': b,
			'eu10': b,
			'eu12': b,
			'eu15': b,
			'thatcher': b,
			"T": n
		},
		postProcessGolubEUP, sep = "\t", isCensorship = False
	),
	# "CarpenterFda": CSVRemoteDataset("https://raw.githubusercontent.com/christophergandrud/simPH/master/data/CarpenterFdaData.tab", "acttime", "censor", None, sep = "\t"),
	 

	#"cervical": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/cervical.csv", None, None, None),
	#"desercion": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/desercion.csv", None, None, None),
	#"hptn": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/hptn.csv", None, None, None),
	#"pns": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/pns.csv", None, None, None),
	#"uis": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/uis.csv", None, None, None),
	#"whas": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/whas.csv", None, None, None),
	# "AccraBoth": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraBoth.csv", None, None, None),
	# "AccraConst": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraConst.csv", None, None, None),
	# "AccraDIC": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraConstr.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraDIC.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraMat.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraMatSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/AccraSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Accraboth_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Accraconst_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Accramat_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Accramat_sen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Accrasen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/BiokoConst.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamBoth.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamConst.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamConstr.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamDIC.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamMat.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamMatSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamboth_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaamconst_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaammat_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/DarEsSalaammat_sen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/GhanaBoth.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/GhanaConstr.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/GhanaDIC.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/GhanaMat.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/GhanaMatSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/GhanaSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Ghanaboth_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Ghanaconst_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Ghanamat_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Ghanamat_sen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Ghanasen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroBoth.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroConst.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroConstr.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroDIC.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroMat.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroMatSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/MorogoroSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Morogoroboth_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Morogoroconst_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Morogoromat_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Morogoromat_sen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Morogorosen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeBoth.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeConst.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeConstr.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeDIC.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeMat.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeMatSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/PrincipeSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Principeboth_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Principeconst_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Principemat_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Principemat_sen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/Principesen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeBoth.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeConst.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeConstr.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeDIC.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeMat.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeMatSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeSen.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeboth_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomeconst_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomemat_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomemat_sen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/SaoTomesen_life_table.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/constSreg_data.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/constantSregression.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/eidolon_teeth_data.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/ghanaconst.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/my_data_res.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/my_dic_res.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/survivalvgender.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/test_supp_info.csv", None, None, None),
	# "": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/weightedAge.csv", None, None, None),
	#"migstatus": CSVRemoteDataset("https://github.com/kjbark3r/Survival/blob/master/migstatus.csv", None, None, None),
	#"AnimalInfo": CSVRemoteDataset("https://github.com/kjbark3r/Survival/blob/master/AnimalInfo.csv", None, None, None),
	#"phr": CSVRemoteDataset("https://github.com/kjbark3r/Survival/blob/master/phr.csv", None, None, None),
	#"heatmap": CSVRemoteDataset("https://github.com/manalirupji/CASAS/blob/master/heatmap.csv", None, None, None),
	#"": CSVRemoteDataset("https://github.com/manalirupji/CASAS/blob/master/BRCA_for_quantile_survival_analysis.csv", None, None, None),
	#"bmtcrr": CSVRemoteDataset("https://github.com/manalirupji/CASAS/blob/master/bmtcrr.csv", None, None, None),
	#"example_landmark_Stan": CSVRemoteDataset("https://github.com/manalirupji/CASAS/blob/master/example_landmark_Stan.csv", None, None, None),
	#"Active": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/Active.csv", None, None, None),
	#"InActive": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/InActive.csv", None, None, None),
	#"Inactive": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/Inactive.csv", None, None, None),
	#"NetLixx": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/NetLixx.csv", None, None, None),
	#"NetLixxCox": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/NetLixxCox.csv", None, None, None),
	#"NetLixxCoxPredict": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/NetLixxCoxPredict.csv", None, None, None),
	#"NetLixxRMST": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/NetLixxRMST.csv", None, None, None),
	#"competing_risks": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/competing_risks.csv", None, None, None),
	#"time_varying_covariate": CSVRemoteDataset("https://github.com/Makarand87/SurvivalAnalysis/blob/master/time_varying_covariate.csv", None, None, None),
	#"qol": CSVRemoteDataset("https://github.com/graemeleehickey/joineRML/blob/master/data-raw/qol/qol.csv", None, None, None),
	#"prot": CSVRemoteDataset("https://github.com/graemeleehickey/joineRML/blob/master/data-raw/renal/prot_raw.csv", None, None, None),
	#"haem": CSVRemoteDataset("https://github.com/graemeleehickey/joineRML/blob/master/data-raw/renal/haem_raw.csv", None, None, None),
	#"gfr": CSVRemoteDataset("https://github.com/graemeleehickey/joineRML/blob/master/data-raw/renal/gfr_raw.csv", None, None, None),
	#"island_eradication_1": CSVRemoteDataset("https://github.com/carterz2/Zachs-Data/blob/master/Survival%20Analysis%20of%20island%20Eradication/SurvBaseline.csv", None, None, None),
	#"island_eradication_2": CSVRemoteDataset("https://github.com/carterz2/Zachs-Data/blob/master/Survival%20Analysis%20of%20island%20Eradication/SurvBaselineV2.csv", None, None, None),
	#"bridges_dataclean": CSVRemoteDataset("https://github.com/chandansaha2014/CAIT-Bridges-Survival-Analysis/blob/master/Data/DataClean.csv", None, None, None),
	#"bridges_survival": CSVRemoteDataset("https://github.com/chandansaha2014/CAIT-Bridges-Survival-Analysis/blob/master/Data/Survival.csv", None, None, None),

	#"CODAchain2": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/CODAchain2.txt", None, None, None),
	#"CODAchain3": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/CODAchain3.txt", None, None, None),
	#"CODAindex": CSVRemoteDataset("https://github.com/dtsh2/Survival/blob/master/CODAindex.txt", None, None, None),
	#"uis": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/uis.txt", None, None, None),
	#"whas": CSVRemoteDataset("https://github.com/eduardoleon/survival/blob/master/data/whas.txt", None, None, None),
}