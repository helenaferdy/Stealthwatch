import yaml
import pickle
import os
import time
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone, timedelta

requests.packages.urllib3.disable_warnings()

# CONFIG_FILE = "/opt/devnet/config.yaml"
# SESSION_FILE = "/opt/devnet/session.pkl"
CONFIG_FILE = "config.yaml"
SESSION_FILE = "session.pkl"

QUERY_MINUTES = 10

datetime.now(timezone.utc)
BASE_TIME = datetime.now(timezone.utc)
print(BASE_TIME.strftime("\n%d/%m/%Y %H:%M:%S"))

def read_config():
    with open(CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)
    return config

def update_config(key, value):
    config = read_config() 
    config[key] = value 
    
    with open(CONFIG_FILE, "w") as file:
        yaml.safe_dump(config, file)

CONFIG = read_config()
SMC_USER = CONFIG['smc_user']
SMC_PASSWORD = CONFIG['smc_pass']
SMC_HOST = CONFIG['smc']
TENANT_ID = CONFIG['smc_tenant_id']

session = requests.Session()

def save_session():
    with open(SESSION_FILE, "wb") as file:
        pickle.dump(session.cookies, file)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "rb") as file:
            session.cookies.update(pickle.load(file))

def auth():
    url = f"https://{SMC_HOST}/token/v2/authenticate"
    creds = {
        "username": SMC_USER,
        "password": SMC_PASSWORD
    }

    try:
        response = session.post(url, data=creds, verify=False)
        if response.status_code == 200:
            cookies = session.cookies.get_dict()
            xsrf_token = cookies.get('XSRF-TOKEN')

            if xsrf_token:
                print(f'XSRF-TOKEN | {xsrf_token}')
                save_session()
                update_config("smc_token", xsrf_token)
                return xsrf_token
            else:
                print("XSRF-TOKEN not found in cookies!")
                return "0"
        else:
            print(f"AUTH FAILED | {response.status_code} | {response.text}")
            return "0"
    except Exception as e:
        print(f"EXCEPTION | {e}")

## GET TENANT
def get_tenant():
    url = f"https://{SMC_HOST}/sw-reporting/v2/tenants/"
    response = session.get(url, verify=False)

    try:
        if response.status_code == 200:
            tenants = response.json().get('data', [])
            tenant_name = tenants[0]['displayName']
            tenant_id = tenants[0]['id']
            print(f'TENANT | {tenant_id} | {tenant_name}')
            update_config("smc_tenant_id", tenant_id)
            return tenant_id
        else:
            print(f"TENANT ERROR | {response.status_code}: {response.text}")
    except Exception as e:
        print(f"EXCEPTION | {e}")

## GET QUERY ID
def get_query(xsrf_token):
    start_time = BASE_TIME - timedelta(minutes=QUERY_MINUTES)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = BASE_TIME.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"https://{SMC_HOST}/sw-reporting/v2/tenants/{TENANT_ID}/flows/queries"
    params = {
        "startDateTime": start_time_str,
        "endDateTime": end_time_str,
        "subject": {
            "ipAddresses": {
                "includes": [],
                "excludes": []
            },
            "hostGroups": {
                "includes": [],
                "excludes": []
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": xsrf_token
    }

    try:
        response = session.post(url, headers=headers, json=params, verify=False)
        if response.status_code == 201:
            query = response.json().get("data", {}).get("query")
            query_id = query['id']
            print(f"QUERY CREATED | {QUERY_MINUTES} MINUTES | {query_id}")
            return query_id
        elif response.status_code == 401:
            print("UNAUTHENTICATED")
            return "0"
        else:
            print(f"QUERY ERROR | {response.status_code} | {response.text}")
            return "0"
    except Exception as e:
        print(f"EXCEPTION | {e}")

## QUERY STATUS
def get_query_status(xsrf_token, query_id):
    url = f"https://{SMC_HOST}/sw-reporting/v2/tenants/{TENANT_ID}/flows/queries/{query_id}"
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": xsrf_token
    }

    try:
        response = session.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            query = response.json().get("data", {}).get("query")
            query_status = query['status']
            query_percent =  round(query['percentComplete'], 1)
            print(f'{query_status} | {query_percent}%')
            if query_status.upper() == 'IN_PROGRESS':
                time.sleep(5)
            return query_status
        else:
            print(f"QUERY STATUS ERROR | {response.status_code} | {response.text}")
            return "NULL"
    except Exception as e:
        print(f"EXCEPTION | {e}")

## QUERY RESULT
def get_query_result(xsrf_token, query_id):
    url = f"https://{SMC_HOST}/sw-reporting/v2/tenants/{TENANT_ID}/flows/queries/{query_id}/results"
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": xsrf_token
    }

    try:
        response = session.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            result = response.json().get("data", {}).get("flows")
            return result
        else:
            print(f"QUERY RESULT ERROR | {response.status_code} | {response.text}")
            return "0"
    except Exception as e:
        print(f"EXCEPTION | {e}")

load_session()
token = CONFIG['smc_token']
query_id = '0'
query_status = 'NULL'

if not CONFIG.get("smc_tenant_id"):
    TENANT_ID = get_tenant()

init = True
xcount = 0
while init == True:
    init = False
    query_id = get_query(token)
    if query_id == '0' and xcount < 5:
        xcount += 1
        token = auth()
        if query_id == '0':
            init = True
    else:
        query_status = 'CREATED'
        time.sleep(5)

# query_id = '67eac2ea018a6b2fc74ab483'
xcount = 0
while query_status.upper() != 'COMPLETED' and xcount < 20:
    xcount += 1
    query_status = get_query_status(token, query_id)
    ## xcheck !!
    if query_status.upper == 'NULL':
        token = auth()

flows = []
if query_status.upper() == 'COMPLETED':
    flows = get_query_result(token, query_id)


## INFLUX
inf_url = CONFIG['influx']
inf_token = CONFIG['influx_token']
inf_org = CONFIG['influx_org']
inf_bucket = CONFIG['influx_bucket']


from influxdb_client import Point, WritePrecision

client = InfluxDBClient(url=inf_url, token=inf_token, org=inf_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

points = []
if flows:
    print(f'WRITING {len(flows)} FLOWS | ', end="")
    for flow in flows:
        print(".", end="", flush=True)
        flow_id = flow['id']
        flow_time = flow['statistics']['firstActiveTime']
        flow_protocol = flow["protocol"]
        flow_src = flow['subject']['ipAddress']
        flow_src_port = flow['subject']['portProtocol']['port']
        flow_dst = flow['peer']['ipAddress']
        flow_dst_port = flow['peer']['portProtocol']['port']
        flow_byte = flow['statistics']['byteCount']
        flow_packet = flow['statistics']['packetCount']
        timestamp_ns = int(datetime.strptime(flow_time, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp() * 1e9)

        point = (
            Point("network_flow")
            .field("id", flow_id)
            .field("byte", flow_byte)
            .field("packet", flow_packet)
            .tag("protocol", flow_protocol)
            .tag("src_ip", flow_src)
            .tag("dst_ip", flow_dst)
            .tag("src_port", flow_src_port)
            .tag("dst_port", flow_dst_port)
            .time(timestamp_ns, WritePrecision.NS)
        )

        points.append(point)
else:
    print('FLOWS EMPTY')

try:
    write_api.write(bucket=inf_bucket, org=inf_org, record=points)
    client.close()
    print(f' | UPLOADED')
except Exception as e:
    print(f" | EXCEPTION | {e}")