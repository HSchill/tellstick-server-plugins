
from datetime import date, datetime
import time
import pytz
from base import Plugin, Settings, Application, configuration, ConfigurationDict
import holidays
from telldus import DeviceManager, Device
from iso3166 import countries
import logging
from pluginloader import ConfigurationDropDown

# pylint: disable=E0211,E0213,W0622,W0312
class WorkDay(Device):

	def __init__(self):
		super(WorkDay, self).__init__()

	def _command(self, action, value, success, failure, **kwargs):
    		logging.debug('Sending command %s to dummy device', action)
		success()

	def localId(self):
    		return 1
        
	def typeString(self):
            return 'workday'

class Country(object):
    def __init__(self):
        self.s = Settings('telldus.scheduler')
        self.timezone = self.s.get('tz', 'UTC')
        self.country_code = self.countryCode()

    def countryCode(self):
        countr_code=""
        for countrycode in pytz.country_timezones:
            timezones = pytz.country_timezones[countrycode]
            for timezone in timezones:
                if timezone == self.timezone:
                    countr_code = countrycode
        return countr_code

    def getCountry(self):
        return countries.get(self.country_code).name


@configuration(
	countryList=ConfigurationDropDown(
        menuList={
            "Argentina":"Argentina", "Australia":"Australia", "Austria":"Austria", "Belgium":"Belgium", "Canada":"Canada", "Colombia":"Colombia",
            "Czech":"Czech", "Denmark":"Denmark", "England":"England","Finland":"Finland", "France":"France", "Germany":"Germany", 
            "Hungary":"Hungary", "India":"India", "Ireland":"Ireland", "Italy":"Italy", "Japan":"Japan", "Mexico":"Mexico", "Netherlands":"Netherlands",
            "NewZealand":"NewZealand", "Northern Ireland":"Northern Ireland", "Norway":"Norway", "Polish":"Polish", "Portugal":"Portugal", 
            "PortugalExt":"PortugalExt", "Scotland":"Scotland", "Slovenia":"Slovenia", "Slovakia":"Slovakia","South Africa":"South Africa", 
            "Spain":"Spain", "Sweden":"Sweden", "Switzerland":"Switzerland", "UnitedKingdom":"UnitedKingdom", "UnitedStates":"UnitedStates", 
            "EuropeanCentralBank":"EuropeanCentralBank", "Wales":"Wales",
        },
        selected=Country().getCountry()
    )
)

class WorkDaySensor(Plugin):

    def __init__(self):
		self.country = Country()
		self.selected = self.configuration['countryList'].selected
		self.device = WorkDay()
		self.deviceManager = DeviceManager(self.context)
		self.deviceManager.addDevice(self.device)
		self.deviceManager.finishedLoading('workday')
		Application().registerScheduledTask(self.checkDay, minutes=1, runAtOnce=True)

    def checkDay(self):
        date_time = datetime.now(pytz.timezone(self.country.timezone))
        try:
            country_holidays = holidays.CountryHoliday(self.selected)
        except self.country.country_code == "":
            pass
        except:
            country_holidays = holidays.CountryHoliday(countries.get(self.selected).alpha3)
        if date(date_time.year, date_time.month, date_time.day) in country_holidays and date_time.hour==00 and date_time.minute==01 and self.selected=="":
    	    self.deviceAction(2)
        elif date_time.hour==00 and date_time.minute==01:
            self.deviceAction(1)

    def deviceAction(self,action):
        self.device.command(action=action)

    def configWasUpdated(self, key, value):
        if key == 'selected':
            self.selected = value