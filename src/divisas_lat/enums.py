from enum import Enum

class Country(str, Enum):
    """Supported countries in Divisas.lat"""
    GUATEMALA = "GT"
    HONDURAS = "HN"
    EL_SALVADOR = "SV"
    COSTA_RICA = "CR"
    NICARAGUA = "NI"
    MEXICO = "MX"
    REPUBLICA_DOMINICANA = "DO"


class Currency(str, Enum):
    """Commonly used currencies"""
    USD = "USD"
    EUR = "EUR"
    MXN = "MXN"
    GTQ = "GTQ"
    HNL = "HNL"
    CRC = "CRC"
    NIO = "NIO"
    DOP = "DOP"
    SVC = "SVC"
