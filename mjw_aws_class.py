import boto3
import sys
import os


class MyAWS(object):

    def __init__(self, ec2):

        self.ec2 = ec2

    def fail(self, msg):
        if os.name != "nt":
            print("\033[91m* " + msg + "\033[0m")
        else:
            print("[ERROR] " + msg)

    def success(self, msg):
        if os.name != "nt":
            print("\033[92m* " + msg + "\033[0m")
        else:
            print("[SUCCESS] " + msg)

    def info(self, msg):
        if os.name != "nt":
            print("\033[94m* " + msg + "\033[0m")
        else:
            print("[INFO] " + msg)

    def get_iname(self, instid):
        try:
            #ec2 = boto3.resource("ec2", region_name=vRegion)
            instances = self.ec2.instances.all()
            for i in instances:
                instance = self.ec2.Instance(instid)
                for t in instance.tags:
                    if t["Key"] == 'Name':
                        iname = t["Value"]
                return iname
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not get instance name: " + str(b))
            return False

    def get_vol_attach_info(self, vid, pkey):
        try:
            if pkey not in ('State', 'AttachTime', 'InstanceId', 'Device', 'DeleteOnTermination', 'VolumeId'):
                self.fail("pkey must be one of State, AttachTime, InstanceId, Device , DeleteOnTermination, VolumeId")
                return False
            volume = self.ec2.Volume(vid).attachments
            for v in volume:
                return v[pkey]
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not get Volume info: " + str(b))
            return False

    def get_volids(self, instid):
        try:
            instance = self.ec2.Instance(instid)
            volumes = instance.volumes.all()
            return volumes
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not get vol ids: " + str(b))
            return False

    def dev_exist(self, instid, dev):
        try:
            volumes = self.get_volids(instid)
            for v in volumes:
                attachments = self.ec2.Volume(v.id).attachments
                for a in attachments:
                    if a['Device'] == dev:
                        return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not get device info " + str(b))
            return False

    def create_snapshot(volid, desc):
        try:
            snapshot = self.ec2.create_snapshot(VolumeId=volid, Description=desc)
            return snapshot.id
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not create snapshot: " + str(b))
            return None

    def delete_snapshot(self, snapid):
        try:
            snapshot = self.ec2.Snapshot(snapid)
            snapshot.delete()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not delete snapshot: " + str(b))
            return False

    def start_vm(self, instid):
        try:
            instance = self.ec2.Instance(instid)
            instance.start()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not start VM: " + str(b))
            return False

    def stop_vm(self, instid):
        try:
            instance = self.ec2.Instance(instid)
            instance.stop()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not stop VM: " + str(b))
            return False

    def delete_vm(self, instid):
        try:
            instance = self.ec2.Instance(instid)
            instance.terminate()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not terminate VM: " + str(b))
            return False

    def restart_vm(self, instid):
        try:
            instance = self.ec2.Instance(instid)
            instance.reboot()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not restart VM: " + str(b))
            return False

    def delete_vm(self, instid):
        try:
            instance = self.ec2.Instance(instid)
            instance.terminate()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not terminate VM: " + str(b))
            return False

    def create_volume(self, zone, size):
        try:
            volume = self.ec2.create_volume(Size=size, VolumeType='gp2', AvailabilityZone=zone)
            return volume.id
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not create volume: " + str(b))
            return None

    def detach_volume(self, volid):
        try:
            volume = self.ec2.Volume(volid)
            volume.detach_from_instance()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not detach volume: " + str(b))
            return False

    def delete_volume(self, volid):
        try:
            volume = self.ec2.Volume(volid)
            volume.delete()
            return True
        except:
            a, b, c = sys.exc_info()
            self.fail("Could not delete volume: " + str(b))
            return False
