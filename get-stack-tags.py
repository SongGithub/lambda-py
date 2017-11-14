#!/usr/bin/env python
import boto3


def get_stack_tags(stack_name):
    '''given a CloudFormation stack name, return an array of dicts of Tags'''
    client = boto3.client('cloudformation')
    response = client.describe_stacks(
        StackName=stack_name
    )
    tags_dict = response['Stacks'][0]['Tags']
    return tags_dict


if __name__ == '__main__':
    print(get_stack_tags('ops-buildkite-agent-linux'))
