# AWS IoT pub/sub over MQTT

## Introduction

Hello, in this post we would create an IoT thing on AWS, use it's credentials, to create two virtual clients on a Linux VM with python and test publishing from one client and subscribing from the other.

### VM
Use your Linux machine or a VM as a virtual IoT device. We would be doing all of the CLI / coding tasks in the post, on this VM.

### AWS
Install and setup the AWS CLI. Here is the region I have set as default.

### Endpoint
Goto AWS IoT > Settings on the cloud console, and get the Device data endpoint which is unique to the AWS account/region. Or get it from the AWS CLI.

```bash
$ IOT_DEV_EP=$(aws iot describe-endpoint --region us-east-2 --output text --query endpointAddress)

$ echo $IOT_DEV_EP
<some-id>.iot.ap-south-1.amazonaws.com

# Check connectivity to this endpoint from the Linux VM, which is your virtual IoT device.
# Check connectivity to this endpoint from the Linux VM, which is your virtual IoT device.

$ ping -c 1 $IOT_DEV_EP
---TRUNCATED---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 196.145/196.145/196.145/0.000 ms
```

### Thing
Goto AWS IoT > Manage > Things > Create Things
on the cloud console and create a new thing with the name temp-sensor, set unnamed shadow(classic) and choose
Auto-generate a new certificate (recommended).

In the policies section, create and select a new policy with the name temp-sensor and the following JSON.


```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect",
        "iot:Publish",
        "iot:Receive",
        "iot:RetainPublish",
        "iot:Subscribe"
      ],
      "Resource": "*"
    }
  ]
}
```


Download all the certificates/keys and name those as needed, I have named them as follows.

```bash
$ ls *.pem
ca-cert.pem  pub-cert.pem  pub-key.pem  pvt-key.pem
```

### SDK
We would be using the AWS IoT SDK for Python.
#### Clone the repository
``` git clone https://github.com/aws/aws-iot-device-sdk-python-v2.git ```

#### Install using Pip
``` python3 -m pip install ./aws-iot-device-sdk-python-v2 ```

#### Remove  the clone, if it isn't required anymore
``` $ rm -rf aws-iot-device-sdk-python-v2 ```


### Connect

We have to first import the mqtt_connection_builder package from the awsiot sdk.
```python from awsiot import mqtt_connection_builder ```

We need the endpoint, the cerificate/key paths and a client_id to initiate a connection. We can generate a client_id using the uuid package.

```python 
from uuid import uuid4
client_id = 'client-' + str(uuid4())
```

We can then pass the files as arguments using the argparse package.

##### parse arguments

```python 
import argparse

parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")

parser.add_argument('--ep', help="IoT device endpoint <some-prefix>.iot.<region>.amazonaws.com", required=True, type=str)
parser.add_argument('--pubcert', help="IoT device public certificate file path", required=True, type=str)
parser.add_argument('--pvtkey', help="IoT device private key file path", required=True, type=str)
parser.add_argument('--cacert', help="IoT device CA cert file path", required=True, type=str)
parser.add_argument('--topic', help="Topic name", required=True, type=str)

args = parser.parse_args()
```

You can also skip the parse arguments step and add the parameters directly.

We have the necessary parameters to initiate the connection.
```python 
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=args.ep,
    cert_filepath=args.pubcert,
    pri_key_filepath=args.pvtkey,
    ca_filepath=args.cacert,
    client_id=client_id
)

connect_future = mqtt_connection.connect()

# result() waits until a result is available
connect_future.result()
print(f'{client_id} is connected!')
```

Put the code we saw in the connect section so far in a file called connect.py and run the following.
```bash 
python connect.py --ep $IOT_DEV_EP --pubcert pub-cert.pem --pvtkey pvt-key.key --cacert ca-cert.pem --topic temperatureTopic                               
client-3924e5d4-97d3-43e6-b214-169d008b2d02 is connected!
```

Great, the connection is successful.






### Reference : [Dev.to](https://dev.to/aws-builders/aws-iot-pubsub-over-mqtt-1oig)
