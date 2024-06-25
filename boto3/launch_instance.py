import boto3

def connect_to_ec2(region_name, aws_access_key_id, aws_secret_access_key):
    """
    Function to connect to EC2.
    """
    ec2 = boto3.client('ec2',
                       region_name=region_name,
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key)
    return ec2

def run_ec2_instance(ec2_client, instance_type, max_count, min_count, image_id, subnet_id):
    """
    Function to run EC2 instances.
    """
    instances = ec2_client.run_instances(
        InstanceType=instance_type,
        MaxCount=max_count,
        MinCount=min_count,
        ImageId=image_id,
        SubnetId=subnet_id
    )
    return instances

if __name__ == '__main__':

    print("Enter AWS credentials:")
    aws_access_key_id = input("AWS Access Key ID: ")
    aws_secret_access_key = input("AWS Secret Access Key: ")


    print("\nEnter EC2 instance details:")
    region_name = input("AWS Region: ")
    instance_type = input(f"Instance Type (default: t2.micro): ") or 't2.micro'
    max_count = int(input("Max Count (default 1): ") or 1)
    min_count = int(input("Min Count (default 1): ") or 1)
    image_id = input("Image ID (AMI ID): ")
    subnet_id = input("Subnet ID: ")


    ec2_client = connect_to_ec2(region_name, aws_access_key_id, aws_secret_access_key)


    instances = run_ec2_instance(ec2_client, instance_type, max_count, min_count, image_id, subnet_id)

    print("\nInstances launched:")
    print(instances)
