# (c) 2015, Jon Hadfield <jon@lessknown.co.uk>
"""
Description: This lookup takes an AWS region and a 'Name' tag value
of and ec2 instance and returns the current state.

Example Usage:
{{ lookup('aws_ec2_instance_status_from_name', ('eu-west-1', 'server1') }}
"""
from ansible import errors
try:
    import boto.ec2
except ImportError:
    raise AnsibleError("aws_ec2_instance_status_from_name lookup cannot be run without boto installed")

class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
	                        self.basedir = basedir

    def run(self, terms, variables=None, **kwargs):
        region = terms[0]
        instance_name = terms[1]
        conn = boto.ec2.connect_to_region(region)
        filters = {'tag:Name': instance_name}
        ec2_instance = conn.get_only_instances(filters=filters)
        if ec2_instance and ec2_instance[0].state:
            return [ec2_instance[0].state.encode('utf-8')]
        return None
