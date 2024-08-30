"""Collection of TA-LIB function evaluators for use in criteria"""

import attrs

from .criteria import functions
from .criteria.kwargs_schemas import KwargsSchema, MergeKwargsSchemas
from . import kwargs_schemas as kt
from . import arg_evaluators as arg_ev


EVALUATOR_GROUPS = (
    "Volatility Indicators",
    "Pattern Recognition",
    "Momentum Indicators",
    "Math Operators",
)

#########################
# VOLATILITY INDICATORS #
#########################

ATR = functions.new_evaluator(
    "ATR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="ATR",
    description="Average True Range. Measures market volatility by decomposing the entire range of an asset price for that period.",
    group="Volatility Indicators",
)

NATR = functions.new_evaluator(
    "NATR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="NATR",
    description="Normalized Average True Range. The ATR value normalized to represent a percentage of the closing price.",
    group="Volatility Indicators",
)

TRANGE = functions.new_evaluator(
    "TRANGE",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,  # Takes no keyword arguments
    alias="TRANGE",
    description="True Range. The greatest of the following: current high minus the current low, the absolute value of the current high minus the previous close, and the absolute value of the current low minus the previous close.",
    group="Volatility Indicators",
)


###################################
# CANDLESTICK PATTERN RECOGNITION #
###################################

CDL2CROWS = functions.new_evaluator(
    "CDL2CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,  # Takes no keyword arguments
    alias="CDL2CROWS",
    group="Pattern Recognition",
    description="Two Crows: A bearish reversal pattern consisting of two black candlesticks after a long white one.",
)

CDL3BLACKCROWS = functions.new_evaluator(
    "CDL3BLACKCROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDL3BLACKCROWS",
    group="Pattern Recognition",
    description="Three Black Crows: A bearish reversal pattern consisting of three consecutive black candlesticks.",
)

CDL3INSIDE = functions.new_evaluator(
    "CDL3INSIDE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDL3INSIDE",
    group="Pattern Recognition",
    description="Three Inside Up/Down: A three-candlestick pattern signaling a potential reversal.",
)

CDL3LINESTRIKE = functions.new_evaluator(
    "CDL3LINESTRIKE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDL3LINESTRIKE",
    group="Pattern Recognition",
    description="Three-Line Strike: A four-candlestick reversal pattern consisting of three candles in the direction of the trend followed by a counter candle.",
)

CDL3OUTSIDE = functions.new_evaluator(
    "CDL3OUTSIDE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDL3OUTSIDE",
    group="Pattern Recognition",
    description="Three Outside Up/Down: A bullish or bearish reversal pattern with three candlesticks.",
)

CDL3STARSINSOUTH = functions.new_evaluator(
    "CDL3STARSINSOUTH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDL3STARSINSOUTH",
    group="Pattern Recognition",
    description="Three Stars in the South: A rare bullish reversal pattern consisting of three candlesticks.",
)

CDL3WHITESOLDIERS = functions.new_evaluator(
    "CDL3WHITESOLDIERS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDL3WHITESOLDIERS",
    group="Pattern Recognition",
    description="Three White Soldiers: A bullish reversal pattern with three consecutive long white candles.",
)

CDLABANDONEDBABY = functions.new_evaluator(
    "CDLABANDONEDBABY",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLABANDONEDBABY",
    group="Pattern Recognition",
    description="Abandoned Baby: A reversal pattern characterized by a gap between the three candles.",
)

CDLADVANCEBLOCK = functions.new_evaluator(
    "CDLADVANCEBLOCK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLADVANCEBLOCK",
    group="Pattern Recognition",
    description="Advance Block: A bearish reversal pattern consisting of three candlesticks.",
)

CDLBELTHOLD = functions.new_evaluator(
    "CDLBELTHOLD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLBELTHOLD",
    group="Pattern Recognition",
    description="Belt-hold: A pattern with one long candlestick with no shadow in the direction of the trend.",
)

CDLBREAKAWAY = functions.new_evaluator(
    "CDLBREAKAWAY",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLBREAKAWAY",
    group="Pattern Recognition",
    description="Breakaway: A pattern consisting of five candlesticks that indicates a potential trend reversal.",
)

CDLCLOSINGMARUBOZU = functions.new_evaluator(
    "CDLCLOSINGMARUBOZU",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLCLOSINGMARUBOZU",
    group="Pattern Recognition",
    description="Closing Marubozu: A candlestick with no shadows and the close is at the high or low.",
)

CDLCONCEALBABYSWALL = functions.new_evaluator(
    "CDLCONCEALBABYSWALL",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLCONCEALBABYSWALL",
    group="Pattern Recognition",
    description="Concealing Baby Swallow: A bullish reversal pattern formed by four black candlesticks.",
)

CDLCOUNTERATTACK = functions.new_evaluator(
    "CDLCOUNTERATTACK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLCOUNTERATTACK",
    group="Pattern Recognition",
    description="Counterattack: A two-candlestick pattern indicating a possible trend reversal.",
)

CDLDARKCLOUDCOVER = functions.new_evaluator(
    "CDLDARKCLOUDCOVER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLDARKCLOUDCOVER",
    group="Pattern Recognition",
    description="Dark Cloud Cover: A bearish reversal pattern with a black candlestick closing below the midpoint of the previous white candlestick.",
)

CDLDOJI = functions.new_evaluator(
    "CDLDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLDOJI",
    group="Pattern Recognition",
    description="Doji: A candlestick where the open and close are almost the same, signaling indecision.",
)

CDLDOJISTAR = functions.new_evaluator(
    "CDLDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLDOJISTAR",
    group="Pattern Recognition",
    description="Doji Star: A pattern where a Doji follows a long candlestick, indicating a potential reversal.",
)

CDLDRAGONFLYDOJI = functions.new_evaluator(
    "CDLDRAGONFLYDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLDRAGONFLYDOJI",
    group="Pattern Recognition",
    description="Dragonfly Doji: A Doji with a long lower shadow and no upper shadow, often indicating a bullish reversal.",
)

CDLENGULFING = functions.new_evaluator(
    "CDLENGULFING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLENGULFING",
    group="Pattern Recognition",
    description="Engulfing Pattern: A reversal pattern where a larger candlestick engulfs the previous one.",
)

CDLEVENINGDOJISTAR = functions.new_evaluator(
    "CDLEVENINGDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLEVENINGDOJISTAR",
    group="Pattern Recognition",
    description="Evening Doji Star: A bearish reversal pattern with a Doji in the middle of a three-candlestick formation.",
)

CDLEVENINGSTAR = functions.new_evaluator(
    "CDLEVENINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLEVENINGSTAR",
    group="Pattern Recognition",
    description="Evening Star: A bearish reversal pattern with three candlesticks, indicating the end of an uptrend.",
)

CDLGAPSIDESIDEWHITE = functions.new_evaluator(
    "CDLGAPSIDESIDEWHITE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLGAPSIDESIDEWHITE",
    group="Pattern Recognition",
    description="Up/Down-gap side-by-side white lines: A continuation pattern with two white candlesticks forming after a gap.",
)

CDLGRAVESTONEDOJI = functions.new_evaluator(
    "CDLGRAVESTONEDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLGRAVESTONEDOJI",
    group="Pattern Recognition",
    description="Gravestone Doji: A Doji with a long upper shadow and no lower shadow, often indicating a bearish reversal.",
)

CDLHAMMER = functions.new_evaluator(
    "CDLHAMMER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHAMMER",
    group="Pattern Recognition",
    description="Hammer: A bullish reversal pattern with a small body and a long lower shadow, indicating potential buying pressure.",
)

CDLHANGINGMAN = functions.new_evaluator(
    "CDLHANGINGMAN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHANGINGMAN",
    group="Pattern Recognition",
    description="Hanging Man: A bearish reversal pattern with a small body and a long lower shadow, indicating potential selling pressure.",
)

CDLHARAMI = functions.new_evaluator(
    "CDLHARAMI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHARAMI",
    group="Pattern Recognition",
    description="Harami: A two-candlestick pattern indicating a potential reversal, where the second candle is contained within the body of the first.",
)

CDLHARAMICROSS = functions.new_evaluator(
    "CDLHARAMICROSS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHARAMICROSS",
    group="Pattern Recognition",
    description="Harami Cross: A variation of the Harami pattern where the second candlestick is a Doji.",
)

CDLHIGHWAVE = functions.new_evaluator(
    "CDLHIGHWAVE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHIGHWAVE",
    group="Pattern Recognition",
    description="High-Wave: A candlestick with long upper and lower shadows, indicating market indecision.",
)

CDLHIKKAKE = functions.new_evaluator(
    "CDLHIKKAKE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHIKKAKE",
    group="Pattern Recognition",
    description="Hikkake Pattern: A continuation or reversal pattern that follows a failed pattern breakout.",
)

CDLHIKKAKEMOD = functions.new_evaluator(
    "CDLHIKKAKEMOD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHIKKAKEMOD",
    group="Pattern Recognition",
    description="Modified Hikkake Pattern: A variation of the Hikkake pattern with a different configuration of candlesticks.",
)

CDLHOMINGPIGEON = functions.new_evaluator(
    "CDLHOMINGPIGEON",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLHOMINGPIGEON",
    group="Pattern Recognition",
    description="Homing Pigeon: A bullish reversal pattern where the second candlestick is contained within the body of the first.",
)

CDLIDENTICAL3CROWS = functions.new_evaluator(
    "CDLIDENTICAL3CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLIDENTICAL3CROWS",
    group="Pattern Recognition",
    description="Identical Three Crows: A bearish reversal pattern consisting of three black candlesticks with identical open and close prices.",
)

CDLINNECK = functions.new_evaluator(
    "CDLINNECK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLINNECK",
    group="Pattern Recognition",
    description="In-Neck: A bearish continuation pattern with a black candlestick followed by a small white candlestick.",
)

CDLINVERTEDHAMMER = functions.new_evaluator(
    "CDLINVERTEDHAMMER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLINVERTEDHAMMER",
    group="Pattern Recognition",
    description="Inverted Hammer: A bullish reversal pattern with a long upper shadow and a small body, indicating potential buying pressure.",
)

CDLKICKING = functions.new_evaluator(
    "CDLKICKING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLKICKING",
    group="Pattern Recognition",
    description="Kicking: A two-candlestick pattern with a gap between a white and black candlestick, signaling a strong reversal.",
)

CDLKICKINGBYLENGTH = functions.new_evaluator(
    "CDLKICKINGBYLENGTH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLKICKINGBYLENGTH",
    group="Pattern Recognition",
    description="Kicking by Length: A variation of the Kicking pattern that considers the length of the candlesticks.",
)

CDLLADDERBOTTOM = functions.new_evaluator(
    "CDLLADDERBOTTOM",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLLADDERBOTTOM",
    group="Pattern Recognition",
    description="Ladder Bottom: A five-candlestick bullish reversal pattern with consecutive lower closes followed by a gap up.",
)

CDLLONGLEGGEDDOJI = functions.new_evaluator(
    "CDLLONGLEGGEDDOJI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLLONGLEGGEDDOJI",
    group="Pattern Recognition",
    description="Long-Legged Doji: A Doji with long upper and lower shadows, indicating high market volatility and indecision.",
)

CDLLONGLINE = functions.new_evaluator(
    "CDLLONGLINE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLLONGLINE",
    group="Pattern Recognition",
    description="Long Line Candle: A long candlestick with a significant body, indicating strong market momentum.",
)

CDLMARUBOZU = functions.new_evaluator(
    "CDLMARUBOZU",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLMARUBOZU",
    group="Pattern Recognition",
    description="Marubozu: A candlestick with no shadows, indicating a strong trend in the direction of the body.",
)

CDLMATCHINGLOW = functions.new_evaluator(
    "CDLMATCHINGLOW",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLMATCHINGLOW",
    group="Pattern Recognition",
    description="Matching Low: A bullish reversal pattern with two consecutive candlesticks having the same low.",
)

CDLMATHOLD = functions.new_evaluator(
    "CDLMATHOLD",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLMATHOLD",
    group="Pattern Recognition",
    description="Mat Hold: A continuation pattern with a gap up, three small candlesticks, and a gap down, indicating strong trend momentum.",
)

CDLMORNINGDOJISTAR = functions.new_evaluator(
    "CDLMORNINGDOJISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLMORNINGDOJISTAR",
    group="Pattern Recognition",
    description="Morning Doji Star: A bullish reversal pattern with a Doji in the middle of a three-candlestick formation.",
)

CDLMORNINGSTAR = functions.new_evaluator(
    "CDLMORNINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.Penetration,
    alias="CDLMORNINGSTAR",
    group="Pattern Recognition",
    description="Morning Star: A bullish reversal pattern with three candlesticks, indicating the end of a downtrend.",
)

CDLONNECK = functions.new_evaluator(
    "CDLONNECK",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLONNECK",
    group="Pattern Recognition",
    description="On-Neck: A bearish continuation pattern with a black candlestick followed by a small white candlestick.",
)

CDLPIERCING = functions.new_evaluator(
    "CDLPIERCING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLPIERCING",
    group="Pattern Recognition",
    description="Piercing Pattern: A bullish reversal pattern with a white candlestick that opens below the previous black candlestick and closes above its midpoint.",
)

CDLRICKSHAWMAN = functions.new_evaluator(
    "CDLRICKSHAWMAN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLRICKSHAWMAN",
    group="Pattern Recognition",
    description="Rickshaw Man: A Doji with long upper and lower shadows, indicating market indecision and high volatility.",
)

CDLRISEFALL3METHODS = functions.new_evaluator(
    "CDLRISEFALL3METHODS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLRISEFALL3METHODS",
    group="Pattern Recognition",
    description="Rising/Falling Three Methods: A continuation pattern with a series of small candlesticks within a trend, indicating a pause before the trend resumes.",
)

CDLSEPARATINGLINES = functions.new_evaluator(
    "CDLSEPARATINGLINES",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLSEPARATINGLINES",
    group="Pattern Recognition",
    description="Separating Lines: A continuation pattern with two opposite-colored candlesticks that share the same opening price.",
)

CDLSHOOTINGSTAR = functions.new_evaluator(
    "CDLSHOOTINGSTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLSHOOTINGSTAR",
    group="Pattern Recognition",
    description="Shooting Star: A bearish reversal pattern with a long upper shadow and a small body, indicating potential selling pressure.",
)

CDLSHORTLINE = functions.new_evaluator(
    "CDLSHORTLINE",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLSHORTLINE",
    group="Pattern Recognition",
    description="Short Line Candle: A short candlestick with a small body, indicating a lack of strong market momentum.",
)

CDLSPINNINGTOP = functions.new_evaluator(
    "CDLSPINNINGTOP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLSPINNINGTOP",
    group="Pattern Recognition",
    description="Spinning Top: A candlestick with a small body and long upper and lower shadows, indicating market indecision.",
)

CDLSTALLEDPATTERN = functions.new_evaluator(
    "CDLSTALLEDPATTERN",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLSTALLEDPATTERN",
    group="Pattern Recognition",
    description="Stalled Pattern: A bearish reversal pattern with three candlesticks, indicating the potential end of an uptrend.",
)

CDLSTICKSANDWICH = functions.new_evaluator(
    "CDLSTICKSANDWICH",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLSTICKSANDWICH",
    group="Pattern Recognition",
    description="Stick Sandwich: A bullish reversal pattern with three candlesticks, where the middle candlestick is opposite in color to the surrounding candlesticks.",
)

CDLTAKURI = functions.new_evaluator(
    "CDLTAKURI",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLTAKURI",
    group="Pattern Recognition",
    description="Takuri (Dragonfly Doji): A bullish reversal pattern with a long lower shadow and a small body, indicating potential buying pressure.",
)

CDLTASUKIGAP = functions.new_evaluator(
    "CDLTASUKIGAP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLTASUKIGAP",
    group="Pattern Recognition",
    description="Tasuki Gap: A continuation pattern with a gap followed by candlesticks that move in the same direction, indicating strong trend momentum.",
)

CDLTHRUSTING = functions.new_evaluator(
    "CDLTHRUSTING",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLTHRUSTING",
    group="Pattern Recognition",
    description="Thrusting Pattern: A bearish continuation pattern with a black candlestick followed by a small white candlestick that closes below the midpoint of the previous black candlestick.",
)

CDLTRISTAR = functions.new_evaluator(
    "CDLTRISTAR",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLTRISTAR",
    group="Pattern Recognition",
    description="Tristar: A reversal pattern with three consecutive Dojis, indicating a potential trend change.",
)

CDLUNIQUE3RIVER = functions.new_evaluator(
    "CDLUNIQUE3RIVER",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLUNIQUE3RIVER",
    group="Pattern Recognition",
    description="Unique Three River Bottom: A bullish reversal pattern with three candlesticks, where the third candlestick is a small white candlestick within the body of the second.",
)

CDLUPSIDEGAP2CROWS = functions.new_evaluator(
    "CDLUPSIDEGAP2CROWS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLUPSIDEGAP2CROWS",
    group="Pattern Recognition",
    description="Upside Gap Two Crows: A bearish reversal pattern with a gap up followed by two black candlesticks that close the gap.",
)

CDLXSIDEGAP3METHODS = functions.new_evaluator(
    "CDLXSIDEGAP3METHODS",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="CDLXSIDEGAP3METHODS",
    group="Pattern Recognition",
    description="Upside/Downside Gap Three Methods: A continuation pattern with a gap followed by three small candlesticks within the gap, indicating trend continuation.",
)


#######################
# MOMENTUM INDICATORS #
#######################

ADX = functions.new_evaluator(
    "ADX",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="ADX",
    group="Momentum Indicators",
    description="Average Directional Index: Measures the strength of a trend without indicating its direction.",
)

ADXR = functions.new_evaluator(
    "ADXR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="ADXR",
    group="Momentum Indicators",
    description="Average Directional Movement Rating: A smoothed version of ADX, indicating the trend strength.",
)

APO = functions.new_evaluator(
    "APO",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.FastandSlowPeriod, kt.MAType),
    alias="APO",
    group="Momentum Indicators",
    description="Absolute Price Oscillator: Shows the difference between two moving averages of a security's price.",
)

AROON = functions.new_evaluator(
    "AROON",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=kt.TimePeriod,
    alias="AROON",
    group="Momentum Indicators",
    description="Aroon: Identifies the strength of a trend and the likelihood of its continuation.",
)

AROONOSC = functions.new_evaluator(
    "AROONOSC",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=kt.TimePeriod,
    alias="AROONOSC",
    group="Momentum Indicators",
    description="Aroon Oscillator: Calculates the difference between Aroon Up and Aroon Down.",
)

BOP = functions.new_evaluator(
    "BOP",
    arg_evaluators=[arg_ev.Open, arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=None,
    alias="BOP",
    group="Momentum Indicators",
    description="Balance of Power: Measures the strength of buyers versus sellers.",
)

CCI = functions.new_evaluator(
    "CCI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="CCI",
    group="Momentum Indicators",
    description="Commodity Channel Index: Identifies cyclical trends in a security's price.",
)

CMO = functions.new_evaluator(
    "CMO",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="CMO",
    group="Momentum Indicators",
    description="Chande Momentum Oscillator: Measures the momentum of a security's price, developed by Tushar Chande.",
)

DX = functions.new_evaluator(
    "DX",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="DX",
    group="Momentum Indicators",
    description="Directional Movement Index: Indicates the strength of a trend by comparing positive and negative movement.",
)

MACD = functions.new_evaluator(
    "MACD",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.FastandSlowPeriod, kt.SignalPeriod),
    alias="MACD",
    group="Momentum Indicators",
    description="Moving Average Convergence Divergence: A trend-following momentum indicator that shows the relationship between two moving averages.",
)

MACDEXT = functions.new_evaluator(
    "MACDEXT",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(
        kt.FastandSlowPeriod, kt.FastandSlowMAType, kt.SignalPeriod, kt.SignalMAType
    ),
    alias="MACDEXT",
    group="Momentum Indicators",
    description="MACD with controllable moving average types: A more flexible version of MACD that allows for different types of moving averages.",
)

MACDFIX = functions.new_evaluator(
    "MACDFIX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.SignalPeriod,
    alias="MACDFIX",
    group="Momentum Indicators",
    description="MACD Fix: A variant of the MACD with a fixed 9-day signal line.",
)

MFI = functions.new_evaluator(
    "MFI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close, arg_ev.Volume],
    kwargs_schema=kt.TimePeriod,
    alias="MFI",
    group="Momentum Indicators",
    description="Money Flow Index: Measures the buying and selling pressure using both price and volume.",
)

MINUS_DI = functions.new_evaluator(
    "MINUS_DI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="MINUS_DI",
    group="Momentum Indicators",
    description="Minus Directional Indicator: Measures the negative directional movement, used in ADX calculations.",
)

MINUS_DM = functions.new_evaluator(
    "MINUS_DM",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=kt.TimePeriod,
    alias="MINUS_DM",
    group="Momentum Indicators",
    description="Minus Directional Movement: Represents the difference between the low of the current period and the low of the previous period.",
)

MOM = functions.new_evaluator(
    "MOM",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MOM",
    group="Momentum Indicators",
    description="Momentum: Measures the speed and change of price movements.",
)

PLUS_DI = functions.new_evaluator(
    "PLUS_DI",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="PLUS_DI",
    group="Momentum Indicators",
    description="Plus Directional Indicator: Measures the positive directional movement, used in ADX calculations.",
)

PLUS_DM = functions.new_evaluator(
    "PLUS_DM",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=kt.TimePeriod,
    alias="PLUS_DM",
    group="Momentum Indicators",
    description="Plus Directional Movement: Represents the difference between the high of the current period and the high of the previous period.",
)

PPO = functions.new_evaluator(
    "PPO",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.FastandSlowPeriod, kt.MAType),
    alias="PPO",
    group="Momentum Indicators",
    description="Percentage Price Oscillator: Similar to MACD but expressed as a percentage.",
)

ROC = functions.new_evaluator(
    "ROC",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="ROC",
    group="Momentum Indicators",
    description="Rate of Change: Measures the percentage change in price between the current price and the price a certain number of periods ago.",
)

ROCP = functions.new_evaluator(
    "ROCP",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="ROCP",
    group="Momentum Indicators",
    description="Rate of Change Percentage: Expresses the rate of change as a percentage.",
)

ROCR = functions.new_evaluator(
    "ROCR",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="ROCR",
    group="Momentum Indicators",
    description="Rate of Change Ratio: Similar to ROC but expressed as a ratio.",
)

ROCR100 = functions.new_evaluator(
    "ROCR100",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="ROCR100",
    group="Momentum Indicators",
    description="Rate of Change Ratio 100: Similar to ROCR but scaled by 100.",
)

RSI = functions.new_evaluator(
    "RSI",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="RSI",
    group="Momentum Indicators",
    description="Relative Strength Index: A momentum oscillator that measures the speed and change of price movements.",
)

STOCH = functions.new_evaluator(
    "STOCH",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=MergeKwargsSchemas(
        kt.FastK_Period,
        kt.SlowK_Period,
        kt.SlowK_MAType,
        kt.SlowD_Period,
        kt.SlowD_MAType,
    ),
    alias="STOCH",
    group="Momentum Indicators",
    description="Stochastic Oscillator: Compares a particular closing price to a range of prices over a certain period.",
)

STOCHF = functions.new_evaluator(
    "STOCHF",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=MergeKwargsSchemas(kt.FastK_Period, kt.FastD_Period, kt.FastD_MAType),
    alias="STOCHF",
    group="Momentum Indicators",
    description="Stochastic Fast: A faster version of the Stochastic Oscillator.",
)

STOCHRSI = functions.new_evaluator(
    "STOCHRSI",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(
        kt.TimePeriod, kt.FastK_Period, kt.FastD_Period, kt.FastD_MAType
    ),
    alias="STOCHRSI",
    group="Momentum Indicators",
    description="Stochastic RSI: An oscillator that measures the level of RSI relative to its range.",
)

TRIX = functions.new_evaluator(
    "TRIX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="TRIX",
    group="Momentum Indicators",
    description="Triple Exponential Moving Average Oscillator: Measures the rate of change of a triple exponentially smoothed moving average.",
)

ULTOSC = functions.new_evaluator(
    "ULTOSC",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=KwargsSchema(
        "ULTOSC_TimePeriods",
        {
            "timeperiod1": attrs.field(type=int, default=7),
            "timeperiod2": attrs.field(type=int, default=14),
            "timeperiod3": attrs.field(type=int, default=28),
        },
    ),
    alias="ULTOSC",
    group="Momentum Indicators",
    description="Ultimate Oscillator: Combines short-term, intermediate-term, and long-term price action into one oscillator.",
)

WILLR = functions.new_evaluator(
    "WILLR",
    arg_evaluators=[arg_ev.High, arg_ev.Low, arg_ev.Close],
    kwargs_schema=kt.TimePeriod,
    alias="WILLR",
    group="Momentum Indicators",
    description="Williams %R: A momentum indicator that measures overbought and oversold levels.",
)


#############################
# MATH OPERATOR FUNCTIONS #
#############################

ADD = functions.new_evaluator(
    "ADD",
    arg_evaluators=[arg_ev.Real0, arg_ev.Real1],
    kwargs_schema=None,
    alias="ADD",
    description="Vector Arithmetic Addition",
    group="Math Operators",
)

DIV = functions.new_evaluator(
    "DIV",
    arg_evaluators=[arg_ev.Real0, arg_ev.Real1],
    kwargs_schema=None,
    alias="DIV",
    description="Vector Arithmetic Division",
    group="Math Operators",
)

MAX = functions.new_evaluator(
    "MAX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MAX",
    description="Highest value over a specified period",
    group="Math Operators",
)

MAXINDEX = functions.new_evaluator(
    "MAXINDEX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MAXINDEX",
    description="Index of highest value over a specified period",
    group="Math Operators",
)

MIN = functions.new_evaluator(
    "MIN",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MIN",
    description="Lowest value over a specified period",
    group="Math Operators",
)

MININDEX = functions.new_evaluator(
    "MININDEX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MININDEX",
    description="Index of lowest value over a specified period",
    group="Math Operators",
)

MINMAX = functions.new_evaluator(
    "MINMAX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MINMAX",
    description="Lowest and highest values over a specified period",
    group="Math Operators",
)

MINMAXINDEX = functions.new_evaluator(
    "MINMAXINDEX",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MINMAXINDEX",
    description="Indexes of lowest and highest values over a specified period",
    group="Math Operators",
)

MULT = functions.new_evaluator(
    "MULT",
    arg_evaluators=[arg_ev.Real0, arg_ev.Real1],
    kwargs_schema=None,
    alias="MULT",
    description="Vector Arithmetic Multiplication",
    group="Math Operators",
)

SUB = functions.new_evaluator(
    "SUB",
    arg_evaluators=[arg_ev.Real0, arg_ev.Real1],
    kwargs_schema=None,
    alias="SUB",
    description="Vector Arithmetic Subtraction",
    group="Math Operators",
)

SUM = functions.new_evaluator(
    "SUM",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="SUM",
    description="Summation over a specified period",
    group="Math Operators",
)


##########################
# STATISTIC FUNCTIONS #
##########################

BETA = functions.new_evaluator(
    "BETA",
    arg_evaluators=[arg_ev.Real0, arg_ev.Real1],
    kwargs_schema=kt.TimePeriod,
    alias="BETA",
    description="Beta (measures the volatility of an asset in comparison to the market as a whole)",
    group="Statistic Functions",
)

CORREL = functions.new_evaluator(
    "CORREL",
    arg_evaluators=[arg_ev.Real0, arg_ev.Real1],
    kwargs_schema=kt.TimePeriod,
    alias="CORREL",
    description="Pearson's Correlation Coefficient (r) (measures the linear correlation between two datasets)",
    group="Statistic Functions",
)

LINEARREG = functions.new_evaluator(
    "LINEARREG",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="LINEARREG",
    description="Linear Regression (calculates a linear regression for a series of values)",
    group="Statistic Functions",
)

LINEARREG_ANGLE = functions.new_evaluator(
    "LINEARREG_ANGLE",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="LINEARREG_ANGLE",
    description="Linear Regression Angle (calculates the angle of the linear regression line)",
    group="Statistic Functions",
)

LINEARREG_INTERCEPT = functions.new_evaluator(
    "LINEARREG_INTERCEPT",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="LINEARREG_INTERCEPT",
    description="Linear Regression Intercept (calculates the y-intercept of the linear regression line)",
    group="Statistic Functions",
)

LINEARREG_SLOPE = functions.new_evaluator(
    "LINEARREG_SLOPE",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="LINEARREG_SLOPE",
    description="Linear Regression Slope (calculates the slope of the linear regression line)",
    group="Statistic Functions",
)

STDDEV = functions.new_evaluator(
    "STDDEV",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.TimePeriod, kt.NbDev),
    alias="STDDEV",
    description="Standard Deviation (measures the amount of variation or dispersion of a set of values)",
    group="Statistic Functions",
)

TSF = functions.new_evaluator(
    "TSF",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="TSF",
    description="Time Series Forecast (calculates a linear regression forecast for a series of values)",
    group="Statistic Functions",
)

VAR = functions.new_evaluator(
    "VAR",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.TimePeriod, kt.NbDev),
    alias="VAR",
    description="Variance (measures how far a set of numbers are spread out from their average value)",
    group="Statistic Functions",
)


#################################
# OVERLAP STUDIES FUNCTIONS #
#################################

BBANDS = functions.new_evaluator(
    "BBANDS",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.TimePeriod, kt.NbDevUpandDown, kt.MAType),
    alias="BBANDS",
    description="Bollinger Bands (technical analysis tool defining upper and lower price range levels)",
    group="Overlap Studies",
)

DEMA = functions.new_evaluator(
    "DEMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="DEMA",
    description="Double Exponential Moving Average (reduces the lag of the standard EMA)",
    group="Overlap Studies",
)

EMA = functions.new_evaluator(
    "EMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="EMA",
    description="Exponential Moving Average (places greater weight on the most recent data)",
    group="Overlap Studies",
)

HT_TRENDLINE = functions.new_evaluator(
    "HT_TRENDLINE",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=None,
    alias="HT_TRENDLINE",
    description="Hilbert Transform - Instantaneous Trendline (identifies current trend direction)",
    group="Overlap Studies",
)

KAMA = functions.new_evaluator(
    "KAMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="KAMA",
    description="Kaufman Adaptive Moving Average (adapts to market volatility)",
    group="Overlap Studies",
)

MA = functions.new_evaluator(
    "MA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.TimePeriod, kt.MAType),
    alias="MA",
    description="Moving Average (smooths out price data to identify the trend direction)",
    group="Overlap Studies",
)

MAMA = functions.new_evaluator(
    "MAMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.FastandSlowLimit,
    alias="MAMA",
    description="MESA Adaptive Moving Average (adjusts based on market conditions)",
    group="Overlap Studies",
)

MAVP = functions.new_evaluator(
    "MAVP",
    arg_evaluators=[arg_ev.Real, arg_ev.Periods],
    kwargs_schema=MergeKwargsSchemas(kt.MinandMaxPeriod, kt.MAType),
    alias="MAVP",
    description="Moving Average with Variable Period (changes period dynamically based on input)",
    group="Overlap Studies",
)

MIDPOINT = functions.new_evaluator(
    "MIDPOINT",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="MIDPOINT",
    description="MidPoint over period (average of the maximum and minimum values)",
    group="Overlap Studies",
)

MIDPRICE = functions.new_evaluator(
    "MIDPRICE",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=kt.TimePeriod,
    alias="MIDPRICE",
    description="Midpoint Price over period (average of the high and low prices)",
    group="Overlap Studies",
)

SAR = functions.new_evaluator(
    "SAR",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=MergeKwargsSchemas(kt.Acceleration, kt.Maximum),
    alias="SAR",
    description="Parabolic SAR (tracks the price over time and identifies potential reversals)",
    group="Overlap Studies",
)

SAREXT = functions.new_evaluator(
    "SAREXT",
    arg_evaluators=[arg_ev.High, arg_ev.Low],
    kwargs_schema=KwargsSchema(
        "SAREXT_Params",
        {
            "startvalue": attrs.field(type=float, default=0),
            "offsetonreverse": attrs.field(type=float, default=0),
            "accelerationinitlong": attrs.field(type=float, default=0),
            "accelerationlong": attrs.field(type=float, default=0),
            "accelerationmaxlong": attrs.field(type=float, default=0),
            "accelerationinitshort": attrs.field(type=float, default=0),
            "accelerationshort": attrs.field(type=float, default=0),
            "accelerationmaxshort": attrs.field(type=float, default=0),
        },
    ),
    alias="SAREXT",
    description="Parabolic SAR - Extended (extended version of Parabolic SAR with additional parameters)",
    group="Overlap Studies",
)

SMA = functions.new_evaluator(
    "SMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="SMA",
    description="Simple Moving Average (calculates the average of a selected range of prices)",
    group="Overlap Studies",
)

T3 = functions.new_evaluator(
    "T3",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=MergeKwargsSchemas(kt.TimePeriod, kt.VFactor),
    alias="T3",
    description="Triple Exponential Moving Average (T3) (offers a smoother average with less lag)",
    group="Overlap Studies",
)

TEMA = functions.new_evaluator(
    "TEMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="TEMA",
    description="Triple Exponential Moving Average (reduces lag more effectively than DEMA)",
    group="Overlap Studies",
)

TRIMA = functions.new_evaluator(
    "TRIMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="TRIMA",
    description="Triangular Moving Average (gives more weight to the middle portion of the period)",
    group="Overlap Studies",
)

WMA = functions.new_evaluator(
    "WMA",
    arg_evaluators=[arg_ev.Real],
    kwargs_schema=kt.TimePeriod,
    alias="WMA",
    description="Weighted Moving Average (gives more weight to recent data)",
    group="Overlap Studies",
)
