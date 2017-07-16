#!/usr/bin/python3

import myclass
import boto3
import argparse


def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", help="AWS region you want to use", default='us-east-1')
    return parser.parse_args()


args = parsed_args()

vRegion = args.region

ec2 = boto3.resource("ec2", region_name=vRegion)

aws = myclass.MyAWS(ec2)


# vols = aws.get_volids('i-037d99c63d330947f')

# for v in vols:
#     print v.id

# aws.stop_vm('i-037d99c63d330947f')

if aws.dev_exist('i-037d99c63d330947f', '/dev/xvda') == True:
    print("device exists")
else:
    print("device does not exist")


#print(aws.get_vol_attach_info('vol-0efe07efb22c3c98f', 'State'))
