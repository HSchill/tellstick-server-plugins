# -*- coding: utf-8 -*-

from base import configuration, ConfigurationString, Plugin, implements
import httplib, urllib

__name__ = 'influx'


@configuration(
	influxServer = ConfigurationString(
		defaultValue='',
		title='InfluxDB server name',
		description='Address to the database server',
		minLength=4
	),
	port = ConfigurationString(
		defaultValue='8086',
		title='InfluxDB server port',
		minLength=2,
		maxLength=5
	),
	database = ConfigurationString(
		defaultValue='tellstick',
		title='Database name',
		description='name of the database (create database <name>)',
		minLength=4
	),
	username = ConfigurationString(
		defaultValue='',
		title='Username',
		description='Leave blank if not needed'
	),
	password = ConfigurationString(
		defaultValue='',
		title='Password',
		description='Leave blank if not needed'
	)
)

class DB(Plugin):
	def acode(self, src):
		if isinstance(src, (str, bytearray)):
			return src.replace(' ', '_').decode('utf-8','replace').encode('ascii','replace')
		elif isinstance(src, unicode):
			return src.replace(' ', '_').encode('ascii','replace')
		else:
			return src

	def send(self, measurment, location, devname, devid, data, datatype, scale='0'):

		params = "%s,location=%s,id=%s,name=%s,scale=%s,type=%s data=%s" % (self.acode(measurment), self.acode(location), self.acode(devid), self.acode(devname), self.acode(scale), self.acode(datatype), self.acode(data))

		headers = { "Content-type" : "application/x-www-form-urlencoded",
			"Accept"       : "*/*",
			"Host"         : "%s" % self.config('influxServer') }

		urlstr = "/write?db=%s" % self.config('database')

		if self.config('username') != '':
			s = '&'
			pu = {'u':'%s' % self.config('username')}
			if self.config('password') != '':
				pu.update({'p':'%s' % self.config('password')})
			urlstr = s.join((urlstr, urllib.urlencode(pu)))

		con = httplib.HTTPConnection(self.config('influxServer'), self.config('port'), timeout=10)
		con.request("POST", urlstr, params, headers)
		resp = con.getresponse()
		data = resp.read()
		con.close()
		return data

