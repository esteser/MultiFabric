import re
from ansible.errors import AnsibleError, AnsibleFilterError, AnsibleFilterTypeError
from ansible.module_utils.common.text.converters import to_native


def bgp_asn(asn_dotted: str) -> int:
    """Accepts an 4-byte BGP ASN in dotted notation returns a standard 4-byte BGP ASN

    :param asn_dotted: A dotted notation 4-byte BGP ASN
    :type iteration: str
    :raises AnsibleFilterTypeError: Iteration must be an integer between 0 and 65535
    :raises AnsibleFilterTypeError: ASN2 must be an integer between 0 and 65535
    :return: 4-byte BGP ASN
    :rtype: int
    """
    asn_parts = str(asn_dotted).split('.')
    iteration = asn_parts[1]
    asn2 = asn_parts[0]
    if not iteration.isdigit():
        raise AnsibleFilterTypeError('Iteration must be an integer!')
    if int(iteration) > 65535:
        raise AnsibleFilterTypeError('Iteration must be in range 0-65535!')
    if not asn2.isdigit() and int(asn2) > 65535:
        raise AnsibleFilterTypeError('ASN2 must be an integer!')
    if int(asn2) > 65535:
        raise AnsibleFilterTypeError('ASN2 must be in range 0-65535!')
    iteration = int(iteration)
    asn2 = int(asn2)
    asn4 = int('{:016b}'.format(asn2) + '{:016b}'.format(iteration), 2)
    return asn4

def mlag_address(switch_name: str, mlag_side: str, ip_type: str) -> str:
    """Accepts a switch name and returns a dictionary of MLAG IP addresses

    :param switch_name: Name of the switch
    :type switch_name: str
    :param mlag_side: Side of the MLAG pair (local or remote) from the switch perspecitive
    :type mlag_side: str
    :param ip_type: Type of peering; mlag or bgp peering over the mlag
    :type ip_type: str
    :return: String of MLAG local or remote IP address
    :rtype: str
    """

    if ip_type not in ['mlag', 'bgp']:
        raise AnsibleFilterTypeError('type must be either mlag or bgp')
    if mlag_side not in ['local', 'remote']:
        raise AnsibleFilterTypeError('mlag side must be either local or remote')
    if not switch_name[-1].isdigit():
        raise AnsibleFilterTypeError('Switch name must end with a number')
    if int(switch_name[-1]) % 2 != 0:
        if mlag_side == 'local':
            if ip_type == 'mlag':
                return '192.0.0.0'
            else:
                return '192.0.0.2'
        else:
            if ip_type == 'mlag':
                return '192.0.0.1'
            else:
                return '192.0.0.3'
    else:
        if mlag_side == 'local':
            if ip_type == 'mlag':
                return '192.0.0.1'
            else:
                return '192.0.0.3'
        else:
            if ip_type == 'mlag':
                return '192.0.0.0'
            else:
                return '192.0.0.2'


class FilterModule(object):
    """ Ansible core jinja2 filters """

    def filters(self):
        """ Filter to function mapping """
        return {
            'bgp_asn': bgp_asn,
            'mlag_address': mlag_address
        }