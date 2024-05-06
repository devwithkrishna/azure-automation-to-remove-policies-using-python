# azure-automation-to-remove-policies-using-python
automation to remove policy from a subscription by name - especially tagging policies with subscription name and policy name as input

# References
* https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.exceptions.httpresponseerror?view=azure-python#azure-core-exceptions-httpresponseerror-message :heavy_check_mark:
* https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.policy.v2022_06_01.operations.policyassignmentsoperations?view=azure-python#azure-mgmt-resource-policy-v2022-06-01-operations-policyassignmentsoperations-delete :heavy_check_mark:
* https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.policy.v2022_06_01.policyclient?view=azure-python :heavy_check_mark: 

# What is azure policy

```
Azure Policy helps to enforce organizational standards and to assess compliance at-scale. 
Through its compliance dashboard, it provides an aggregated view to evaluate the overall state of the environment,
with the ability to drill down to the per-resource, per-policy granularity. It also helps to bring your resources to compliance through bulk remediation for existing resources and automatic remediation for new resources.
```
Read more here: [Azure Governance - Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview)

# What the code does

```
As the name suggests, this is an automation to remove policy from a subscription by name especially tagging policies with subscription name and policy name as input
```

# Athentication 

```markdown
AZURE_CLIENT_ID= "xxxxxxxxxxx"
AZURE_CLIENT_SECRET = "xxxxxxxxxxx"
AZURE_SUBSCRIPTION_ID = "xxxxxxxxxxx"
AZURE_TENANT_ID = "xxxxxxxxxxx"
```
* Replace ` "xxxxxxxxxxx" ` with proper values

**Rest is taken care by `DefaultAzureCredential` from `azure-identity` module** 

# How code works

| file name | funtions |
|-----------|----------|
| azure_resource_graph_query.py | this file takes an argument, your subscription name and returns subscription id |
| remove_azure_policy.py | this is the main py file. takes subscription id and policy name as inputs and removes policy if present |


How to run the program manually from cmd line:

`python3 remove_azure_policy.py --subscription_name "<Subscription name>" --policy_name "<Policy name>"`

- replace the subscription name and policy names and provide correct values.

# parameters 

`Python-dotenv reads key-value pairs from a .env file and can set them as environment variables`

| input name      | type | description                                                 | required |
|-----------------|------|-------------------------------------------------------------|----------|
| subscription_name  | string | Azure subscription name. Default - `TECH-ARCHITECTS-NONPROD` | :heavy_check_mark: |
| policy_name    | string | Azure policy to be removed.  | :heavy_check_mark: |
