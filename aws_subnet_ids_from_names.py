# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a list of one or more
subnet names and returns a list of matching subnet ids.

Example Usage:
{{ lookup('aws_subnet_ids_from_names', ('eu-west-1', ['subnet1', 'subnet2'])) }}
"""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import codecs

from ansible.errors import *
from ansible.plugins.lookup import LookupBase

try:
    import boto
    import boto.vpc
except ImportError:
    raise AnsibleError("aws_subnet_ids_from_names lookup cannot be run without boto installed")

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        if isinstance(terms, basestring):
            terms = [terms]
        subnet_ids = []
        region = terms[0]
        subnet_names = terms[1]
        vpc_conn = boto.vpc.connect_to_region(region)
        for subnet_name in subnet_names:
            filters = {'tag:Name': subnet_name}
            subnet = vpc_conn.get_all_subnets(filters=filters)
            if subnet and subnet[0]:
                subnet_ids.append(subnet[0].id.encode('utf-8'))
        return subnet_ids
