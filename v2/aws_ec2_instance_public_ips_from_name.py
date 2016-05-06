# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a 'Name' tag value
of and ec2 instance and returns the current public IP address.

Example Usage:
{{ lookup('aws_ec2_instance_public_ips_from_name', ('eu-west-1', 'server1') }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.ec2
except ImportError:
    raise AnsibleError("aws_ec2_instance_public_ips_from_name lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        region = terms[0][0]
        instance_name = terms[0][1]
        conn = boto.ec2.connect_to_region(region)
        filters = {'tag:Name': instance_name}
        ec2_instances = conn.get_only_instances(filters=filters)
        return [instance.ip_address.encode('utf-8') for instance in ec2_instances if instance.ip_address is not None]
