"""Risk management function evaluators."""

from .criteria import functions
from . import kwargs_types as kt
from . import arg_evaluators as arg_ev


#########################
# VOLATILITY INDICATORS #
#########################

ATR = functions.new_evaluator(
    "ATR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.TimePeriod,
    alias="ATR",
)

NATR = functions.new_evaluator(
    "NATR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.TimePeriod,
    alias="NATR",
)

TRANGE = functions.new_evaluator(
    "TRANGE",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,  # Takes no keyword arguments
    alias="TRANGE",
)


##################################
# CANDLESTICK PATTERN EVALUATORS #
##################################

CDL2CROWS = functions.new_evaluator(
    "CDL2CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,  # Takes no keyword arguments
    alias="CDL2CROWS",
)

CDL3BLACKCROWS = functions.new_evaluator(
    "CDL3BLACKCROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDL3BLACKCROWS",
)

CDL3INSIDE = functions.new_evaluator(
    "CDL3INSIDE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDL3INSIDE",
)

CDL3LINESTRIKE = functions.new_evaluator(
    "CDL3LINESTRIKE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDL3LINESTRIKE",
)

CDL3OUTSIDE = functions.new_evaluator(
    "CDL3OUTSIDE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDL3OUTSIDE",
)

CDL3STARSINSOUTH = functions.new_evaluator(
    "CDL3STARSINSOUTH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDL3STARSINSOUTH",
)

CDL3WHITESOLDIERS = functions.new_evaluator(
    "CDL3WHITESOLDIERS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDL3WHITESOLDIERS",
)

CDLABANDONEDBABY = functions.new_evaluator(
    "CDLABANDONEDBABY",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLABANDONEDBABY",
)

CDLADVANCEBLOCK = functions.new_evaluator(
    "CDLADVANCEBLOCK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLADVANCEBLOCK",
)

CDLBELTHOLD = functions.new_evaluator(
    "CDLBELTHOLD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLBELTHOLD",
)

CDLBREAKAWAY = functions.new_evaluator(
    "CDLBREAKAWAY",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLBREAKAWAY",
)

CDLCLOSINGMARUBOZU = functions.new_evaluator(
    "CDLCLOSINGMARUBOZU",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLCLOSINGMARUBOZU",
)

CDLCONCEALBABYSWALL = functions.new_evaluator(
    "CDLCONCEALBABYSWALL",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLCONCEALBABYSWALL",
)

CDLCOUNTERATTACK = functions.new_evaluator(
    "CDLCOUNTERATTACK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLCOUNTERATTACK",
)

CDLDARKCLOUDCOVER = functions.new_evaluator(
    "CDLDARKCLOUDCOVER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLDARKCLOUDCOVER",
)

CDLDOJI = functions.new_evaluator(
    "CDLDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLDOJI",
)

CDLDOJISTAR = functions.new_evaluator(
    "CDLDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLDOJISTAR",
)

CDLDRAGONFLYDOJI = functions.new_evaluator(
    "CDLDRAGONFLYDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLDRAGONFLYDOJI",
)

CDLENGULFING = functions.new_evaluator(
    "CDLENGULFING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLENGULFING",
)

CDLEVENINGDOJISTAR = functions.new_evaluator(
    "CDLEVENINGDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLEVENINGDOJISTAR",
)

CDLEVENINGSTAR = functions.new_evaluator(
    "CDLEVENINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLEVENINGSTAR",
)

CDLGAPSIDESIDEWHITE = functions.new_evaluator(
    "CDLGAPSIDESIDEWHITE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLGAPSIDESIDEWHITE",
)

CDLGRAVESTONEDOJI = functions.new_evaluator(
    "CDLGRAVESTONEDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLGRAVESTONEDOJI",
)

CDLHAMMER = functions.new_evaluator(
    "CDLHAMMER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHAMMER",
)

CDLHANGINGMAN = functions.new_evaluator(
    "CDLHANGINGMAN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHANGINGMAN",
)

CDLHARAMI = functions.new_evaluator(
    "CDLHARAMI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHARAMI",
)

CDLHARAMICROSS = functions.new_evaluator(
    "CDLHARAMICROSS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHARAMICROSS",
)

CDLHIGHWAVE = functions.new_evaluator(
    "CDLHIGHWAVE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHIGHWAVE",
)

CDLHIKKAKE = functions.new_evaluator(
    "CDLHIKKAKE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHIKKAKE",
)

CDLHIKKAKEMOD = functions.new_evaluator(
    "CDLHIKKAKEMOD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHIKKAKEMOD",
)

CDLHOMINGPIGEON = functions.new_evaluator(
    "CDLHOMINGPIGEON",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLHOMINGPIGEON",
)

CDLIDENTICAL3CROWS = functions.new_evaluator(
    "CDLIDENTICAL3CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLIDENTICAL3CROWS",
)

CDLINNECK = functions.new_evaluator(
    "CDLINNECK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLINNECK",
)

CDLINVERTEDHAMMER = functions.new_evaluator(
    "CDLINVERTEDHAMMER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLINVERTEDHAMMER",
)

CDLKICKING = functions.new_evaluator(
    "CDLKICKING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLKICKING",
)

CDLKICKINGBYLENGTH = functions.new_evaluator(
    "CDLKICKINGBYLENGTH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLKICKINGBYLENGTH",
)

CDLLADDERBOTTOM = functions.new_evaluator(
    "CDLLADDERBOTTOM",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLLADDERBOTTOM",
)

CDLLONGLEGGEDDOJI = functions.new_evaluator(
    "CDLLONGLEGGEDDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLLONGLEGGEDDOJI",
)

CDLLONGLINE = functions.new_evaluator(
    "CDLLONGLINE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLLONGLINE",
)

CDLMARUBOZU = functions.new_evaluator(
    "CDLMARUBOZU",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLMARUBOZU",
)

CDLMATCHINGLOW = functions.new_evaluator(
    "CDLMATCHINGLOW",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLMATCHINGLOW",
)

CDLMATHOLD = functions.new_evaluator(
    "CDLMATHOLD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLMATHOLD",
)

CDLMORNINGDOJISTAR = functions.new_evaluator(
    "CDLMORNINGDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLMORNINGDOJISTAR",
)

CDLMORNINGSTAR = functions.new_evaluator(
    "CDLMORNINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=kt.Penetration,
    alias="CDLMORNINGSTAR",
)

CDLONNECK = functions.new_evaluator(
    "CDLONNECK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLONNECK",
)

CDLPIERCING = functions.new_evaluator(
    "CDLPIERCING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLPIERCING",
)

CDLRICKSHAWMAN = functions.new_evaluator(
    "CDLRICKSHAWMAN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLRICKSHAWMAN",
)

CDLRISEFALL3METHODS = functions.new_evaluator(
    "CDLRISEFALL3METHODS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLRISEFALL3METHODS",
)

CDLSEPARATINGLINES = functions.new_evaluator(
    "CDLSEPARATINGLINES",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLSEPARATINGLINES",
)

CDLSHOOTINGSTAR = functions.new_evaluator(
    "CDLSHOOTINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLSHOOTINGSTAR",
)

CDLSHORTLINE = functions.new_evaluator(
    "CDLSHORTLINE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLSHORTLINE",
)

CDLSPINNINGTOP = functions.new_evaluator(
    "CDLSPINNINGTOP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLSPINNINGTOP",
)

CDLSTALLEDPATTERN = functions.new_evaluator(
    "CDLSTALLEDPATTERN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLSTALLEDPATTERN",
)

CDLSTICKSANDWICH = functions.new_evaluator(
    "CDLSTICKSANDWICH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLSTICKSANDWICH",
)

CDLTAKURI = functions.new_evaluator(
    "CDLTAKURI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLTAKURI",
)

CDLTASUKIGAP = functions.new_evaluator(
    "CDLTASUKIGAP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLTASUKIGAP",
)

CDLTHRUSTING = functions.new_evaluator(
    "CDLTHRUSTING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLTHRUSTING",
)

CDLTRISTAR = functions.new_evaluator(
    "CDLTRISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLTRISTAR",
)

CDLUNIQUE3RIVER = functions.new_evaluator(
    "CDLUNIQUE3RIVER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLUNIQUE3RIVER",
)

CDLUPSIDEGAP2CROWS = functions.new_evaluator(
    "CDLUPSIDEGAP2CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLUPSIDEGAP2CROWS",
)

CDLXSIDEGAP3METHODS = functions.new_evaluator(
    "CDLXSIDEGAP3METHODS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_type=None,
    alias="CDLXSIDEGAP3METHODS",
)
