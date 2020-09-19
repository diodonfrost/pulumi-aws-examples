# coding: utf8

"""Deploy basic instance with network"""

import pulumi
import pulumi_aws as aws

from settings import *


ami = aws.get_ami(
    most_recent="true",
    owners=["099720109477"],
    filters=[
        {
            "name": "name",
            "values": ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"],
        },
        {"name": "virtualization-type", "values": ["hvm"]},
    ],
)

vpc = aws.ec2.Vpc(
    "vpc-http",
    cidr_block=vpc_cidr,
    enable_dns_hostnames=True,
    tags={"Name": "vpc-http"},
)

subnet = aws.ec2.Subnet(
    "subnet-http",
    vpc_id=vpc.id,
    cidr_block=http_cidr,
    tags={"Name": "subnet-http"},
)

internet_gateway = aws.ec2.InternetGateway(
    "internet-gateway", vpc_id=vpc.id, tags={"Name": "internet-gateway"}
)

route_table = aws.ec2.RouteTable(
    "default-route",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0", gateway_id=internet_gateway.id
        )
    ],
)

route_table_association = aws.ec2.RouteTableAssociation(
    "default-route-association", subnet_id=subnet.id, route_table_id=route_table.id
)

admin_sg = aws.ec2.SecurityGroup(
    "admin",
    description="Allow default administration service",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "icmp",
            "from_port": 8,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]},
    ],
)

http_sg = aws.ec2.SecurityGroup(
    "http",
    description="Allow http incgress trafic",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 443,
            "to_port": 443,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
)

user_data = """
#!/bin/bash

echo "hello world"
"""

http_instance = aws.ec2.Instance(
    "http-instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[http_sg.id, admin_sg.id],
    user_data=user_data,
    ami=ami.id,
    subnet_id=subnet.id,
    tags={"Name": "http-instance"},
)

http_eip = aws.ec2.Eip(
    "lb", instance=http_instance.id, vpc=True, tags={"Name": "http-eip"}
)

pulumi.export("public_ip", http_eip.public_ip)
pulumi.export("public_dns", http_eip.public_dns)
