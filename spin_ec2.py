#!/usr/bin/python3


import boto3
import os
import argparse


def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--ami_id",
                        help="the instance id you want to snapshot.  default: current instance id",
                        default='ami-c58c1dd3')
    parser.add_argument("-n", "--name",
                        help="Name for Instance Tag. Default is none", default='')
    parser.add_argument("-t", "--inst_type",
                        help="Amazon Instance Type", default='t2.micro')
    parser.add_argument("-r", "--region", help="Enter Amazon Region", default='us-east-1')

    return parser.parse_args()


def fail(msg):
    if os.name != "nt":
        print("\033[91m* " + msg + "\033[0m")
    else:
        print("[ERROR] " + msg)


def success(msg):
    if os.name != "nt":
        print("\033[92m* " + msg + "\033[0m")
    else:
        print("[SUCCESS] " + msg)


def info(msg):
    if os.name != "nt":
        print("\033[94m* " + msg + "\033[0m")
    else:
        print("[INFO] " + msg)


args = parsed_args()

info('Running with following Arguments:')
info('AMI id: ' + args.ami_id)
info('Region: ' + args.region)
info('Instance Name: ' + args.name)
info('Instance Type' + args.inst_type)


ec2_res = boto3.resource('ec2', region_name=args.region)

ec2_cli = boto3.client('ec2', region_name=args.region)


try:
    instance = ec2_res.create_instances(ImageId=args.ami_id,
                                        MinCount=1,
                                        DryRun=True,
                                        MaxCount=1,
                                        InstanceType='t2.micro',
                                        KeyName='awskey',
                                        BlockDeviceMappings=[
                                            {
                                                'DeviceName': '/dev/sdb',
                                                'Ebs': {
                                                    'VolumeSize': 10,
                                                    'VolumeType': 'gp2'
                                                }
                                            },
                                            {
                                                'DeviceName': '/dev/sdc',
                                                'Ebs': {
                                                    'VolumeSize': 5,
                                                    'VolumeType': 'gp2'
                                                }
                                            },
                                            {
                                                'DeviceName': '/dev/sdd',
                                                'Ebs': {
                                                    'VolumeSize': 5,
                                                    'VolumeType': 'gp2'
                                                }
                                            }
                                        ])

    iid = instance[0].id

    mytags = [
        {
            "Key": "Name",
            "Value": args.name
        }]

    ec2_cli.create_tags(
        Resources=[iid],
        Tags=mytags)

    success("Sucess: Instance id = %s" % iid)

except:
    fail("Check your AMI Id and Dry Run setting")
