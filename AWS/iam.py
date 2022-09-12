from email import policy
from email.policy import Policy
from pydoc import pager
import re
from urllib import response
import boto3
import json

def create_user(name):
    iam = boto3.client('iam')
    iam.create_user(UserName='name')


def list_users():
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_users')
    for response in paginator.paginate():
        for user in response["Users"]:
            print(f"username: {user['UserName']}, Arn: {user['Arn']}")

def create_group(groupName):
    iam = boto3.client('iam')
    iam.create_group(GroupName=groupName)


def list_policies():
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_policies')
    for response in paginator.paginate(Scope="Local"):
        for policy in response["Policies"]:
            print(f"Policy name: {policy['PolicyName']} Arn: {policy['Arn']}")


def create_iam_policy():
    iam = boto3.client('iam')

    my_managed_policy = { 
        "Version": "2012-10-17",
        "Statement" : [
            {
                "Effect": "Allow",
                "Action": [ 
                    "dynamodb:GetItem",
                    "dynamodb:Scan",
                ],
                "Resource": "*"
            }
        ]
    }

    reponse = iam.create_policy(
        PolicyName='testDynamoDbPolicy',
        PolicyDocument=json.dumps(my_managed_policy)
    )
    print(response)


def attach_user_policy(policy_arn, username):
    iam = boto3.client('iam')
    response = iam.attach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

def create_iam_role():
    iam = boto3.client('iam')

    assume_role_policy_document = json.dumps( {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "glue.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })

    response = iam.create_role(
        RoleName="glueS3CrawlerRole",
        AssumeRolePolicyDocument= assume_role_policy_document
    )
    return response["Role"]["RoleName"]




