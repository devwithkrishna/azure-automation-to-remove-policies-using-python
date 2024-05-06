import argparse
import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.policyinsights import PolicyInsightsClient
from azure.core.exceptions import HttpResponseError
from azure.mgmt.resource import PolicyClient
from typing import List, Dict, Any
from azure_resource_graph_query import run_azure_rg_query


def list_azure_policy_in_a_subscription_scope(subscription_id:str):
    """
    subscription name --> scope
    :return:
    """
    try:
        credential = DefaultAzureCredential()
        policy_insights_client = PolicyInsightsClient(credential, subscription_id={subscription_id})
        policy_assignments = policy_insights_client.policy_states.list_query_results_for_subscription(policy_states_resource='latest',subscription_id=subscription_id)
        policy_assignments_list = []
        for assignment in policy_assignments:
            print(f"Policy Assignment ID: {assignment.policy_assignment_id}")
            print(f"Policy Assignment Name: {assignment.policy_assignment_name}")
            print(f"Policy Assignment Scope: {assignment.policy_assignment_scope}")
            print(f"Policy Definition ID: {assignment.policy_definition_id}")
            print(f"Policy Definition Name: {assignment.policy_definition_name}")
            print(f"Policy Assignment Created On: {assignment.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print("------------------------------")
            assignment_dict = {
                "policy_assignment_id": assignment.policy_assignment_id,
                "policy_assignment_name": assignment.policy_assignment_name,
                "policy_assignment_scope": assignment.policy_assignment_scope,
                "policy_definition_id": assignment.policy_definition_id,
                "policy_definition_name": assignment.policy_definition_name,
                "policy_assignment_created_on": assignment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            policy_assignments_list.append(assignment_dict)
            file_name = f'azure_policy_assignment_{subscription_id}.json'
            print(file_name)
            # Assuming policy_assignments_list is the list of dictionaries
            with open(file_name, 'w') as json_file:
                json.dump(policy_assignments_list, json_file, indent=4)
            print(f"Policy assignments successfully retrieved and saved to {file_name} .")

        return policy_assignments_list
    except HttpResponseError as ex:
        print(f"Failed to retrieve policy assignments. Error message: {ex.message}")

    except Exception as ex:
        print(f"An error occurred: {ex}")

def validation_of_policy_name(policy_name: str,policy_assignments_list: list[dict[str, Any]]):
    """
    This function is used to validate the provided policy is there in current subscription scoped aassignment
    :param policy_name:
    :return:
    """
    for policy_assignment in policy_assignments_list:
        if policy_name in policy_assignment['policy_assignment_name']:
            print(f"Policy '{policy_name}' found in assignments")
            return policy_name, policy_assignment['policy_assignment_scope']
    raise Exception(f"Policy '{policy_name}' not found in assignments")


def remove_azure_policy_from_subscription(credential,subscription_id: str, policy_name: str, scope:str):
    """
    Remove the policy specified from the subscription level
    :param subscription_id:
    :param policy_name:
    :return:
    """
    try:
        policy_client = PolicyClient(credential, subscription_id)
        policy_client.policy_assignments.delete(scope=scope, policy_assignment_name=policy_name)
        print(f"Policy '{policy_name}' removed from '{scope}' successfully.")
    except HttpResponseError as ex:
        print(f"Failed to delete policy assignment: {ex}")

def main():
    """ To test the code"""
    parser = argparse.ArgumentParser("Remove azure policies")
    parser.add_argument("--subscription_name", help="subscription name in azure", required=True, type=str)
    parser.add_argument("--policy_name", help="policy name in azure", required=True, type=str)

    args = parser.parse_args()
    subscription_name = args.subscription_name
    policy_name = args.policy_name
    print(f"Process to remove azure policy - {policy_name} begining......")
    load_dotenv()
    credential = DefaultAzureCredential()
    subscription_id = run_azure_rg_query(subscription_name=subscription_name)
    print(f'Subscription id of {subscription_name} is : {subscription_id}')
    os.environ['subscription_id'] = subscription_id
    policy_assignments_list = list_azure_policy_in_a_subscription_scope(subscription_id=subscription_id)
    policy_name, policy_assignment_scope = validation_of_policy_name(policy_name=policy_name, policy_assignments_list=policy_assignments_list)
    if policy_name is not None:
        print(f'Removing policy {policy_name} on the scope {policy_assignment_scope}')
        remove_azure_policy_from_subscription(credential=credential,subscription_id=subscription_id, policy_name=policy_name, scope=policy_assignment_scope)



if __name__ == "__main__":
    main()