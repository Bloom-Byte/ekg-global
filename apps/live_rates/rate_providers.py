import typing
import datetime
import attrs
import cattrs
from django.views.decorators.debug import sensitive_variables
import httpx
from dcrypt import TextCrypt, CryptKey
from django.utils import timezone
from django.conf import settings

from helpers.exceptions.requests import RequestError
from helpers.attrs import type_cast
from helpers.logging import log_exception


crypt = TextCrypt(key=CryptKey(hash_algorithm="MD5"))
psx_rate_converter = cattrs.Converter()


@type_cast(psx_rate_converter)
@attrs.define(auto_attribs=True, kw_only=True)
class MGLinkPSXRate:
    company_id: str = attrs.field(alias="CompanyId")
    company_name: str = attrs.field(alias="CompanyName")
    symbol: str = attrs.field(alias="Symbol")
    created_date_time: datetime.datetime = attrs.field(alias="CreatedDateTime")
    open: float = attrs.field(alias="Open")
    high: float = attrs.field(alias="High")
    low: float = attrs.field(alias="Low")
    close: float = attrs.field(alias="Close")
    volume: int = attrs.field(alias="Volume")
    previous_close: float = attrs.field(alias="Last")
    change: float = attrs.field(alias="Change")
    percentage_change: float = attrs.field(alias="PctChange")


def load_psx_rates(rates_data: typing.List[typing.Dict]):
    for rate_data in rates_data:
        yield psx_rate_converter.structure(rate_data, MGLinkPSXRate)


def psx_rate_to_dict(psx_rate: MGLinkPSXRate) -> typing.Dict:
    return psx_rate_converter.unstructure(psx_rate)


class MGLinkRateProvider:
    provider_auth_url = "https://api.mg-link.net/api/auth/token"
    provider_rates_url = "https://api.mg-link.net/api/Data1/PSXStockPrices"

    @sensitive_variables("username", "password")
    def __init__(self, username: str, password: str, request_timeout: float = 30.0):
        """
        Initialize the client with the necessary credentials

        :param username: client username
        :param password: client password
        :param request_timeout: client request timeout in seconds
        """
        self.username = username
        self.password = crypt.encrypt(password)
        self.authentication_required_at = timezone.now()
        self._client = httpx.Client(
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=httpx.Timeout(request_timeout),
        )

    @property
    def client(self):
        """Returns request client, authenticating if necessary"""
        if self.authentication_required_at <= timezone.now():
            self.authenticate()
        return self._client

    def authentication_successful(self, response_data: typing.Dict):
        """Handles the response data from a successful authentication request"""
        access_token = response_data["access_token"]
        validity_period = float(response_data["expires_in"])
        self._client.headers["Authorization"] = f"Bearer {access_token}"
        self.authentication_required_at = timezone.now() + timezone.timedelta(
            seconds=validity_period
        )
        return

    def authenticate(self) -> str:
        """Authenticate with the provider"""
        try:
            response = self._client.post(
                url=type(self).provider_auth_url,
                data={
                    "grant_type": "password",
                    "username": self.username,
                    "password": crypt.decrypt(self.password),
                },
            )
            if response.status_code != 200:
                response.raise_for_status()
            else:
                self.authentication_successful(response.json())
        except Exception as exc:
            log_exception(exc)
            raise RequestError(exc) from exc

    def fetch_psx_rates(
        self,
        _from: typing.Optional[datetime.date] = None,
        _to: typing.Optional[datetime.date] = None,
        /,
    ):
        """
        Fetch PSX rates from the provider.

        Leave _from and _to empty to get the latest PSX rates

        :param _from: The date from which to fetch the rates
        :param _to: The date to which to fetch the rates
        :return: The fetched rates
        """
        request_params = {
            "StartDate": _from.strftime("%Y-%m-%d") if _from else None,
            "EndDate": _to.strftime("%Y-%m-%d") if _to else None,
        }

        try:
            response = self.client.get(
                url=type(self).provider_rates_url,
                params=request_params,
            )
            if response.status_code != 200:
                response.raise_for_status()
            return response.json()

        except Exception as exc:
            log_exception(exc)
            raise RequestError(exc) from exc


mg_link_provider = MGLinkRateProvider(
    username=settings.MG_LINK_CLIENT_USERNAME, password=settings.MG_LINK_CLIENT_PASSWORD
)
