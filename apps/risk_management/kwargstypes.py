"""Collection of custom keyword argument types for TA-LIB functions"""

import attrs

from .criteria.kwargtypes import KwargsType


TimePeriod = KwargsType("TimePeriod", {"timeperiod": attrs.field(type=int, default=14)})

Penetration = KwargsType(
    "Penetration", {"penetration": attrs.field(type=float, default=0.0)}
)

FastandSlowPeriod = KwargsType(
    "FastandSlowPeriod",
    {
        "fastperiod": attrs.field(type=int, default=0),
        "slowperiod": attrs.field(type=int, default=0),
    },
)

FastandSlowMAType = KwargsType(
    "FastandSlowMAType",
    {
        "fastmatype": attrs.field(type=int, default=0),
        "slowmatype": attrs.field(type=int, default=0),
    },
)

MAType = KwargsType(
    "MAType",
    {
        "matype": attrs.field(type=int, default=0),
    },
)

SignalMAType = KwargsType(
    "SignalMAType",
    {
        "signalmatype": attrs.field(type=int, default=0),
    },
)

SignalPeriod = KwargsType(
    "SignalPeriod",
    {
        "signalperiod": attrs.field(type=int, default=0),
    },
)

FastK_Period = KwargsType(
    "FastK_Period",
    {
        "fastk_period": attrs.field(type=int, default=0),
    },
)

SlowK_Period = KwargsType(
    "SlowK_Period",
    {
        "slowk_period": attrs.field(type=int, default=0),
    },
)


FastD_Period = KwargsType(
    "FastD_Period",
    {
        "fastd_period": attrs.field(type=int, default=0),
    },
)

SlowD_Period = KwargsType(
    "SlowD_Period",
    {
        "slowd_period": attrs.field(type=int, default=0),
    },
)

FastK_MAType = KwargsType(
    "FastK_MAType",
    {
        "fastk_matype": attrs.field(type=int, default=0),
    },
)

SlowK_MAType = KwargsType(
    "SlowK_MAType",
    {
        "slowk_matype": attrs.field(type=int, default=0),
    },
)

FastD_MAType = KwargsType(
    "FastD_MAType",
    {
        "fastd_matype": attrs.field(type=int, default=0),
    },
)

SlowD_MAType = KwargsType(
    "SlowD_MAType",
    {
        "slowd_matype": attrs.field(type=int, default=0),
    },
)

