# The provided dictionary
flow_data = {
    'id': 1635,
    'tenantId': 301,
    'flowCollectorId': 301,
    'mplsLabel': -1,
    'protocol': 'TCP',
    'serviceId': 3,
    'tlsVersion': 'NONE',
    'vlanId': -1,
    'applicationId': 168,
    'cipherSuite': {
        'id': 'N/A',
        'name': 'N/A',
        'protocol': 'N/A',
        'keyExchange': 'N/A',
        'authAlgorithm': 'N/A',
        'encAlgorithm': 'N/A',
        'keyLength': 'N/A',
        'messageAuthCode': 'N/A'
    },
    'nbarApp': {
        'id': 218103809,
        'name': 'unknown',
        'description': 'Unknown application'
    },
    'statistics': {
        'activeDuration': 59000,
        'numCombinedFlowRecords': 2,
        'firstActiveTime': '2025-03-30T04:14:41.000+0000',
        'lastActiveTime': '2025-03-30T04:15:40.000+0000',
        'tcpRetransmissions': -2,
        'byteCount': 299,
        'packetCount': 6,
        'byteRate': 5.067796610169491,
        'packetRate': 0.1016949152542373,
        'tcpConnections': 0,
        'roundTripTime': 0,
        'serverResponseTime': 0,
        'subjectPeerRatio': 100.0,
        'rttAverage': -1,
        'rttMaximum': -1,
        'rttMinimum': -1,
        'srtAverage': -1,
        'srtMaximum': -1,
        'srtMinimum': -1,
        'flowTimeSinceStart': 274893,
        'tcpRetransmissionsRatio': -33.333333333333336
    },
    'subject': {
        'hostGroupIds': [65534],
        'countryCode': 'XR',
        'payload': 'ctldl.windowsupdate.com/msdownload/update/v3/static/trustedr/en/disallowedcertstl.cab?e577a692d598b4d5',
        'ipAddress': '172.17.1.21',
        'natPort': -1,
        'portProtocol': {'port': 60847, 'protocol': 'TCP', 'serviceId': 0},
        'percentBytes': 100.0,
        'bytes': 299,
        'packets': 6,
        'byteRate': 5.067796610169491,
        'packetRate': 0.1016949152542373,
        'orientation': 'client',
        'finPackets': 1,
        'rstPackets': 0,
        'synPackets': 1,
        'synAckPackets': 0,
        'tlsVersion': 'NONE',
        'trustSecId': -1
    },
    'peer': {
        'hostGroupIds': [61529],
        'countryCode': 'SG',
        'ipAddress': '124.155.222.153',
        'natPort': -1,
        'portProtocol': {'port': 80, 'protocol': 'TCP', 'serviceId': 0},
        'percentBytes': 0.0,
        'bytes': 0,
        'packets': 0,
        'byteRate': 0.0,
        'packetRate': 0.0,
        'orientation': 'server',
        'finPackets': 0,
        'rstPackets': 0,
        'synPackets': 0,
        'synAckPackets': 0,
        'tlsVersion': 'NONE',
        'trustSecId': -1
    }
}

# Mapping values to variables
flow_id = flow_data['id']
tenant_id = flow_data['tenantId']
protocol = flow_data['protocol']
service_id = flow_data['serviceId']
tls_version = flow_data['tlsVersion']
application_id = flow_data['applicationId']

# Cipher Suite
cipher_suite_id = flow_data['cipherSuite']['id']
cipher_suite_name = flow_data['cipherSuite']['name']

# NBAR Application Info
nbar_app_id = flow_data['nbarApp']['id']
nbar_app_name = flow_data['nbarApp']['name']
nbar_app_description = flow_data['nbarApp']['description']

# Statistics
active_duration = flow_data['statistics']['activeDuration']
tcp_retransmissions = flow_data['statistics']['tcpRetransmissions']
byte_count = flow_data['statistics']['byteCount']
packet_count = flow_data['statistics']['packetCount']
byte_rate = flow_data['statistics']['byteRate']
packet_rate = flow_data['statistics']['packetRate']

# Subject (Client)
subject_ip = flow_data['subject']['ipAddress']
subject_country = flow_data['subject']['countryCode']
subject_port = flow_data['subject']['portProtocol']['port']
subject_bytes = flow_data['subject']['bytes']
subject_packets = flow_data['subject']['packets']
subject_tls_version = flow_data['subject']['tlsVersion']

# Peer (Server)
peer_ip = flow_data['peer']['ipAddress']
peer_country = flow_data['peer']['countryCode']
peer_port = flow_data['peer']['portProtocol']['port']
peer_bytes = flow_data['peer']['bytes']
peer_packets = flow_data['peer']['packets']
peer_tls_version = flow_data['peer']['tlsVersion']

# Printing some values for verification
print(f"Flow ID: {flow_id}, Tenant ID: {tenant_id}, Protocol: {protocol}")
print(f"Subject IP: {subject_ip} ({subject_country}), Port: {subject_port}")
print(f"Peer IP: {peer_ip} ({peer_country}), Port: {peer_port}")
print(f"Byte Count: {byte_count}, Packet Count: {packet_count}")