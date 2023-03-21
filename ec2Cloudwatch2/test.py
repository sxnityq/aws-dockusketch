import datetime
import os

import boto3
from botocore.exceptions import ClientError

region = "us-east-2"
base_dir = os.path.dirname(os.path.realpath(__file__))


class CloudWatchService:
    
    def __init__(self):
        self.client = boto3.client("cloudwatch", region_name=region)

    
    def get_CPUUtilization(self, instance="i-020f00d453a8f41f3"):
        response = self.client.get_metric_statistics(
            Namespace = "AWS/EC2",
            MetricName = "CPUUtilization",
            Dimensions = [
                    {
                        "Name" : "InstanceId",
                        "Value" : instance
                    }
                ],
            Period = 300,
            Statistics= ["Average"],
            StartTime = datetime.datetime(2023, 3, 19, 19),
            EndTime = datetime.datetime(2023, 3, 19, 20)
        )
        return response['Datapoints']   


class EC2Service:
    
    def __init__(self):
        self.client = boto3.client("ec2", region_name=region)
    
    
    def create_instance_from_AMI(self, KeyPairName, SecurityGroup, AMIID="ami-07f14a50ac6da05e2", InstanceType='t2.micro'):
        
        try:
            key_pair = self.client.create_key_pair(KeyName=KeyPairName)
            print(f"{key_pair} successfully created")
        except ClientError as ex:
            return f"{KeyPairName} key already exists"
        
        pem_rel_path = f".pem/{KeyPairName}.pem"

        with open(f"{os.path.join(base_dir, pem_rel_path)}", mode="w", encoding="utf-8") as f:
            f.write(key_pair.get('KeyMaterial'))
        
        try:
            security_group = self.client.create_security_group(
                        Description='This security group was created by boto3',
                        GroupName=SecurityGroup,
                    )
            group_id = security_group.get('GroupId')
            
            self.client.authorize_security_group_ingress(
                        GroupId=group_id,
                        IpPermissions=[
                            {
                                "FromPort" : 22,
                                "IpProtocol" : "tcp",
                                "IpRanges" : [
                                    {
                                        "CidrIp" : "0.0.0.0/0",
                                        "Description" : "open all ports by boto3"
                                    }
                                ],
                                "ToPort" : 22,
                            }
                        ]
                    )
            
            print(f"Security group {SecurityGroup} successfully created")
            
        except ClientError as ex:
            print(f"Security group {SecurityGroup} already exists.\nAssigning existed security group...")
        
        response = self.client.run_instances(
            ImageId = AMIID,
            InstanceType = InstanceType,
            MinCount = 1,
            MaxCount = 1,
            KeyName=key_pair[
                'KeyName'
                ],
            SecurityGroups=[
                SecurityGroup
            ]
        )
        
        return response['Instances'][0]['InstanceId']
    
    def start_instance(self, instance_ID="i-00292baeab9e9065c"):
        response = self.client.start_instances(
            InstanceIds = [
                instance_ID,
                ]
            )
        return response
    
    def stop_instance(self, instance_ID="i-00292baeab9e9065c"):
        response = self.client.stop_instances(
                InstanceIds=[
                        instance_ID,
                        ]
                )
        return response

    def reboot(self, instance_ID="i-00292baeab9e9065c"):
        response = self.client.reboot_instances(
                InstanceIds=[
                        instance_ID,
                        ]
                )
        return response



# a = EC2Service()
# print(a.reboot(instance_ID="i-00292baeab9e9065c"))
# print(a.create_instance_from_AMI(KeyPairName='tired1', SecurityGroup='MySecurityGroup')) -> i-00292baeab9e9065c
# print(a.start_instance())