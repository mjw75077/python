#!/usr/bin/python


import boto3
import sys

ec2 = boto3.resource('ec2', region_name='us-east-1')
cli = boto3.client('ec2', region_name='us-east-1')



def get_vids(iid):
    instance = ec2.Instance(iid)
    volumes = instance.volumes.all()
    return volumes

  #grab attachnment info from volume
def get_attach_info(vid,pkey):
    volume = ec2.Volume(vid).attachments
    for i in volume:
       return i[pkey]


def detach_volume(volid):
    try:
         ec2 = boto3.resource("ec2")
         volume = ec2.Volume(volid)
         volume.detach_from_instance()
         return True
    except:
         a, b, c = sys.exc_info()
         fail("Could not detach volume: " + str(b))
         return False

#main

vols = get_vids('i-088f7608eba2f7a2e')
target_iid='i-148fb225'

for v in vols:
    print v
    dev = get_attach_info(v.id,'Device')
    if dev == '/dev/sdf':
        snap = ec2.create_snapshot(VolumeId=v.id,Description="mjwcreate snap")
        waiter_snapshot_complete=cli.get_waiter('snapshot_completed')
        waiter_snapshot_complete.wait(SnapshotIds=[snap.id])

        new_volume = cli.create_volume(SnapshotId=snap.id,AvailabilityZone='us-east-1c')
        #print new_volume.id
        waiter_volume = cli.get_waiter('volume_available')
        waiter_volume.wait(VolumeIds= [new_volume.get('VolumeId')])
        #attach snap to diff machine
        vid=new_volume['VolumeId']
        print  vid
        #volume=ec2.Volume(new_volume['VolumeId'])
        volume=ec2.Volume(vid)
        print  volume
        cli.attach_volume(VolumeId=vid,InstanceId=target_iid, Device=dev)
        '''
        try:
           cli.attach_volume(VolumeId=volume,InstanceId=target_iid, Device=dev)
        except:
           print "problem with attach"
        '''
