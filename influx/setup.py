#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name='Influx',
	version='1.0',
	icon='influx.png',
	author='Hans Schillstrom',
	author_email='hans@schillstrom.com',
	category='notifications',
	color='#000000',
	description='Send sensor values from lua scripts to influx database',
	long_description="""Use this plugin to add support for sending values to influxdb through Lua scripts.
You need to supply your own influx-server and run create databaase name.

Example to send an insert from Lua:
```lua
local ifdb = require "influx.DB"
ifdb:send{
        measurment='heating',
        location='indoor',
        devname=device:name(),
        devid=device:id(),
        value=Value,
        scale=Scale
}
```
""",
	packages=['influx'],
	entry_points={ \
		'telldus.plugins': ['c = influx:DB [cREQ]']
	},
	extras_require = dict(cREQ = 'Base>=0.1\nTelldus>=0.1'),
)
