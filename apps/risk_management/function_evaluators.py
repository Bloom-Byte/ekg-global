"""Collection of TA-LIB function evaluators for use in criteria"""

import attrs

from .criteria import functions
from .criteria.kwargtypes import KwargsType, MergeKwargsTypes
from . import kwargstypes as kt
from . import arg_evaluators as arg_ev


#########################
# VOLATILITY INDICATORS #
#########################

ATR = functions.new_evaluator(
    "ATR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ATR",
)

NATR = functions.new_evaluator(
    "NATR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="NATR",
)

TRANGE = functions.new_evaluator(
    "TRANGE",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,  # Takes no keyword arguments
    alias="TRANGE",
)


##################################
# CANDLESTICK PATTERN EVALUATORS #
##################################

CDL2CROWS = functions.new_evaluator(
    "CDL2CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,  # Takes no keyword arguments
    alias="CDL2CROWS",
)

CDL3BLACKCROWS = functions.new_evaluator(
    "CDL3BLACKCROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDL3BLACKCROWS",
)

CDL3INSIDE = functions.new_evaluator(
    "CDL3INSIDE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDL3INSIDE",
)

CDL3LINESTRIKE = functions.new_evaluator(
    "CDL3LINESTRIKE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDL3LINESTRIKE",
)

CDL3OUTSIDE = functions.new_evaluator(
    "CDL3OUTSIDE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDL3OUTSIDE",
)

CDL3STARSINSOUTH = functions.new_evaluator(
    "CDL3STARSINSOUTH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDL3STARSINSOUTH",
)

CDL3WHITESOLDIERS = functions.new_evaluator(
    "CDL3WHITESOLDIERS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDL3WHITESOLDIERS",
)

CDLABANDONEDBABY = functions.new_evaluator(
    "CDLABANDONEDBABY",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLABANDONEDBABY",
)

CDLADVANCEBLOCK = functions.new_evaluator(
    "CDLADVANCEBLOCK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLADVANCEBLOCK",
)

CDLBELTHOLD = functions.new_evaluator(
    "CDLBELTHOLD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLBELTHOLD",
)

CDLBREAKAWAY = functions.new_evaluator(
    "CDLBREAKAWAY",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLBREAKAWAY",
)

CDLCLOSINGMARUBOZU = functions.new_evaluator(
    "CDLCLOSINGMARUBOZU",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLCLOSINGMARUBOZU",
)

CDLCONCEALBABYSWALL = functions.new_evaluator(
    "CDLCONCEALBABYSWALL",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLCONCEALBABYSWALL",
)

CDLCOUNTERATTACK = functions.new_evaluator(
    "CDLCOUNTERATTACK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLCOUNTERATTACK",
)

CDLDARKCLOUDCOVER = functions.new_evaluator(
    "CDLDARKCLOUDCOVER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLDARKCLOUDCOVER",
)

CDLDOJI = functions.new_evaluator(
    "CDLDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLDOJI",
)

CDLDOJISTAR = functions.new_evaluator(
    "CDLDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLDOJISTAR",
)

CDLDRAGONFLYDOJI = functions.new_evaluator(
    "CDLDRAGONFLYDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLDRAGONFLYDOJI",
)

CDLENGULFING = functions.new_evaluator(
    "CDLENGULFING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLENGULFING",
)

CDLEVENINGDOJISTAR = functions.new_evaluator(
    "CDLEVENINGDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLEVENINGDOJISTAR",
)

CDLEVENINGSTAR = functions.new_evaluator(
    "CDLEVENINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLEVENINGSTAR",
)

CDLGAPSIDESIDEWHITE = functions.new_evaluator(
    "CDLGAPSIDESIDEWHITE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLGAPSIDESIDEWHITE",
)

CDLGRAVESTONEDOJI = functions.new_evaluator(
    "CDLGRAVESTONEDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLGRAVESTONEDOJI",
)

CDLHAMMER = functions.new_evaluator(
    "CDLHAMMER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHAMMER",
)

CDLHANGINGMAN = functions.new_evaluator(
    "CDLHANGINGMAN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHANGINGMAN",
)

CDLHARAMI = functions.new_evaluator(
    "CDLHARAMI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHARAMI",
)

CDLHARAMICROSS = functions.new_evaluator(
    "CDLHARAMICROSS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHARAMICROSS",
)

CDLHIGHWAVE = functions.new_evaluator(
    "CDLHIGHWAVE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHIGHWAVE",
)

CDLHIKKAKE = functions.new_evaluator(
    "CDLHIKKAKE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHIKKAKE",
)

CDLHIKKAKEMOD = functions.new_evaluator(
    "CDLHIKKAKEMOD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHIKKAKEMOD",
)

CDLHOMINGPIGEON = functions.new_evaluator(
    "CDLHOMINGPIGEON",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLHOMINGPIGEON",
)

CDLIDENTICAL3CROWS = functions.new_evaluator(
    "CDLIDENTICAL3CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLIDENTICAL3CROWS",
)

CDLINNECK = functions.new_evaluator(
    "CDLINNECK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLINNECK",
)

CDLINVERTEDHAMMER = functions.new_evaluator(
    "CDLINVERTEDHAMMER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLINVERTEDHAMMER",
)

CDLKICKING = functions.new_evaluator(
    "CDLKICKING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLKICKING",
)

CDLKICKINGBYLENGTH = functions.new_evaluator(
    "CDLKICKINGBYLENGTH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLKICKINGBYLENGTH",
)

CDLLADDERBOTTOM = functions.new_evaluator(
    "CDLLADDERBOTTOM",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLLADDERBOTTOM",
)

CDLLONGLEGGEDDOJI = functions.new_evaluator(
    "CDLLONGLEGGEDDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLLONGLEGGEDDOJI",
)

CDLLONGLINE = functions.new_evaluator(
    "CDLLONGLINE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLLONGLINE",
)

CDLMARUBOZU = functions.new_evaluator(
    "CDLMARUBOZU",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLMARUBOZU",
)

CDLMATCHINGLOW = functions.new_evaluator(
    "CDLMATCHINGLOW",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLMATCHINGLOW",
)

CDLMATHOLD = functions.new_evaluator(
    "CDLMATHOLD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLMATHOLD",
)

CDLMORNINGDOJISTAR = functions.new_evaluator(
    "CDLMORNINGDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLMORNINGDOJISTAR",
)

CDLMORNINGSTAR = functions.new_evaluator(
    "CDLMORNINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.Penetration,
    alias="CDLMORNINGSTAR",
)

CDLONNECK = functions.new_evaluator(
    "CDLONNECK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLONNECK",
)

CDLPIERCING = functions.new_evaluator(
    "CDLPIERCING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLPIERCING",
)

CDLRICKSHAWMAN = functions.new_evaluator(
    "CDLRICKSHAWMAN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLRICKSHAWMAN",
)

CDLRISEFALL3METHODS = functions.new_evaluator(
    "CDLRISEFALL3METHODS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLRISEFALL3METHODS",
)

CDLSEPARATINGLINES = functions.new_evaluator(
    "CDLSEPARATINGLINES",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLSEPARATINGLINES",
)

CDLSHOOTINGSTAR = functions.new_evaluator(
    "CDLSHOOTINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLSHOOTINGSTAR",
)

CDLSHORTLINE = functions.new_evaluator(
    "CDLSHORTLINE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLSHORTLINE",
)

CDLSPINNINGTOP = functions.new_evaluator(
    "CDLSPINNINGTOP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLSPINNINGTOP",
)

CDLSTALLEDPATTERN = functions.new_evaluator(
    "CDLSTALLEDPATTERN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLSTALLEDPATTERN",
)

CDLSTICKSANDWICH = functions.new_evaluator(
    "CDLSTICKSANDWICH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLSTICKSANDWICH",
)

CDLTAKURI = functions.new_evaluator(
    "CDLTAKURI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLTAKURI",
)

CDLTASUKIGAP = functions.new_evaluator(
    "CDLTASUKIGAP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLTASUKIGAP",
)

CDLTHRUSTING = functions.new_evaluator(
    "CDLTHRUSTING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLTHRUSTING",
)

CDLTRISTAR = functions.new_evaluator(
    "CDLTRISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLTRISTAR",
)

CDLUNIQUE3RIVER = functions.new_evaluator(
    "CDLUNIQUE3RIVER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLUNIQUE3RIVER",
)

CDLUPSIDEGAP2CROWS = functions.new_evaluator(
    "CDLUPSIDEGAP2CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLUPSIDEGAP2CROWS",
)

CDLXSIDEGAP3METHODS = functions.new_evaluator(
    "CDLXSIDEGAP3METHODS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,
    alias="CDLXSIDEGAP3METHODS",
)


#######################
# MOMENTUM INDICATORS #
#######################

ADX = functions.new_evaluator(
    "ADX",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ADX",
)

ADXR = functions.new_evaluator(
    "ADXR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ADXR",
)

APO = functions.new_evaluator(
    "APO",
    arg_evaluators=[arg_ev.Close],
    kwargstype=MergeKwargsTypes(kt.FastandSlowPeriod, kt.MAType),
    alias="APO",
)

AROON = functions.new_evaluator(
    "AROON",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargstype=kt.TimePeriod,
    alias="AROON",
)

AROONOSC = functions.new_evaluator(
    "AROONOSC",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargstype=kt.TimePeriod,
    alias="AROONOSC",
)

BOP = functions.new_evaluator(
    "BOP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=None,  # No keyword arguments
    alias="BOP",
)

CCI = functions.new_evaluator(
    "CCI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="CCI",
)

CMO = functions.new_evaluator(
    "CMO",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="CMO",
)

DX = functions.new_evaluator(
    "DX",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="DX",
)

MACD = functions.new_evaluator(
    "MACD",
    arg_evaluators=[arg_ev.Close],
    kwargstype=MergeKwargsTypes(kt.FastandSlowPeriod, kt.SignalPeriod),
    alias="MACD",
)

MACDEXT = functions.new_evaluator(
    "MACDEXT",
    arg_evaluators=[arg_ev.Close],
    kwargstype=MergeKwargsTypes(
        kt.FastandSlowPeriod, kt.FastandSlowMAType, kt.SignalPeriod, kt.SignalMAType
    ),
    alias="MACDEXT",
)

MACDFIX = functions.new_evaluator(
    "MACDFIX",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.SignalPeriod,
    alias="MACDFIX",
)

MFI = functions.new_evaluator(
    "MFI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close, arg_ev.Volume],
    kwargstype=kt.TimePeriod,
    alias="MFI",
)

MINUS_DI = functions.new_evaluator(
    "MINUS_DI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="MINUS_DI",
)

MINUS_DM = functions.new_evaluator(
    "MINUS_DM",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargstype=kt.TimePeriod,
    alias="MINUS_DM",
)

MOM = functions.new_evaluator(
    "MOM",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="MOM",
)

PLUS_DI = functions.new_evaluator(
    "PLUS_DI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="PLUS_DI",
)

PLUS_DM = functions.new_evaluator(
    "PLUS_DM",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargstype=kt.TimePeriod,
    alias="PLUS_DM",
)

PPO = functions.new_evaluator(
    "PPO",
    arg_evaluators=[arg_ev.Close],
    kwargstype=MergeKwargsTypes(kt.FastandSlowPeriod, kt.MAType),
    alias="PPO",
)

ROC = functions.new_evaluator(
    "ROC",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ROC",
)

ROCP = functions.new_evaluator(
    "ROCP",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ROCP",
)

ROCR = functions.new_evaluator(
    "ROCR",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ROCR",
)

ROCR100 = functions.new_evaluator(
    "ROCR100",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="ROCR100",
)

RSI = functions.new_evaluator(
    "RSI",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="RSI",
)

STOCH = functions.new_evaluator(
    "STOCH",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=MergeKwargsTypes(
        kt.FastK_Period,
        kt.SlowK_Period,
        kt.SlowK_MAType,
        kt.SlowD_Period,
        kt.SlowD_MAType,
    ),
    alias="STOCH",
)

STOCHF = functions.new_evaluator(
    "STOCHF",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=MergeKwargsTypes(kt.FastK_Period, kt.FastD_Period, kt.FastD_MAType),
    alias="STOCHF",
)

STOCHRSI = functions.new_evaluator(
    "STOCHRSI",
    arg_evaluators=[arg_ev.Close],
    kwargstype=MergeKwargsTypes(
        kt.TimePeriod, kt.FastK_Period, kt.FastD_Period, kt.FastD_MAType
    ),
    alias="STOCHRSI",
)

TRIX = functions.new_evaluator(
    "TRIX",
    arg_evaluators=[arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="TRIX",
)

ULTOSC = functions.new_evaluator(
    "ULTOSC",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=KwargsType(
        "ULTOSC_TimePeriods",
        {
            "timeperiod1": attrs.field(type=int, default=7),
            "timeperiod2": attrs.field(type=int, default=14),
            "timeperiod3": attrs.field(type=int, default=28),
        },
    ),
    alias="ULTOSC",
)

WILLR = functions.new_evaluator(
    "WILLR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargstype=kt.TimePeriod,
    alias="WILLR",
)
