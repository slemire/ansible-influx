#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of Ansible

Ansible is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Ansible is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
"""

def main():
    module = AnsibleModule(
        argument_spec=dict(
            influx_host=dict(type='str', required=True),
            influx_port=dict(type='int', required=False, default=8086),
            influx_user=dict(type='str', required=True),
            influx_pass=dict(type='str', required=True, no_log=True),
            influx_db=dict(type='str', required=True),
            influx_precision=dict(type='str', required=False, choices=['n', 'u', 'ms', 's', 'm', 'h'], defaults='n'),
            measurement=dict(type='str', required=True),
            tags=dict(type='dict', required=False),
            fields=dict(type='dict', required=True),
            timeout=dict(type='int', required=False, default=60),
            optional_args=dict(type='dict', required=False, default=None),
        ),
        supports_check_mode=True
    )

    influx_host = module.params['influx_host']
    influx_port = module.params['influx_port']
    influx_user = module.params['influx_user']
    influx_pass = module.params['influx_pass']
    influx_db = module.params['influx_db']
    influx_precision = module.params['influx_precision']
    measurement = module.params['measurement']
    tags = module.params['tags']
    fields = module.params['fields']
    timeout = module.params['timeout']

    if module.params['optional_args'] is None:
        optional_args = {}
    else:
        optional_args = module.params['optional_args']

    try:
        client = InfluxDBClient(influx_host, influx_port, influx_user, influx_pass, influx_db)

        # data to be written to Influx
        json_body = [
            {
                'measurement': measurement,
                'tags': tags,
                'fields': fields,                
            }
        ]

        client.write_points(json_body, time_precision=influx_precision)
        module.exit_json()
    except Exception, e:
        module.fail_json(msg="cannot write data to influxdb: " + str(e))

# standard ansible module imports
from ansible.module_utils.basic import *
from influxdb import InfluxDBClient

if __name__ == '__main__':
    main()
