import boto3
from botocore.exceptions import ParamValidationError


region = "us-east-1"


class EcrRepos:

    def __init__(self):
        self.client_private = boto3.client('ecr', region_name=region)
        self.client_public = boto3.client('ecr-public', region_name=region)
     
    def attach_private_policy(self, user_profile, policy):
		
        try:
            response = self.client_private.describe_repositories(
            registryId=user_profile
            )
        except self.client_private.exceptions.InvalidParameterException:
            return "invalid user_profile"

        for repo in response['repositories']:
            print(f"Repo name: {repo['repositoryName']}\n\n")
            try:
                lifecycle_policy = self.client_private.get_lifecycle_policy(
                                registryId=user_profile,
                                repositoryName=repo['repositoryName']
                                )
                print(lifecycle_policy)
            except self.client_private.exceptions.LifecyclePolicyNotFoundException as ex:
                print("Lifecycle policy was not attached.\nAttaching...")
                try:
                    self.client_private.put_lifecycle_policy(
                        registryId=user_profile,
                        repositoryName=repo['repositoryName'],
                        lifecyclePolicyText=policy
                    )
                    print("policy attached")
                except (ParamValidationError, self.client_private.exceptions.InvalidParameterException) as ex:
                    print("incorrect policy.\nPlease check your policy")

    def attach_public_policy(self, user_profile, policy):

        try:
            response = self.client_public.describe_repositories(
                registryId=user_profile
            )
        except self.client_public.exceptions.InvalidParameterException as ex:
            return "invalid user_profile"

        for repo in response['repositories']:
            print(f"Repo name: {repo['repositoryName']}\n\n")

            try:

                response = self.client_public.get_repository_policy(
                    registryId=user_profile,
                    repositoryName=repo['repositoryName']
                )
                print(response)

            except self.client_public.exeptions.RepositoryPolicyNotFoundException as ex:
                print("Lifecycle policy was not attached.\nAttaching...")
                try:
                    lifecycle_policy = self.client_public.set_repository_policy(
                        registryId=user_profile,
                        repositoryName=repo['repositoryName'],
                        policyText=policy
                    )
                    print("policy attached")
                except (ParamValidationError, self.client_public.exceptions.InvalidParameterException) as ex:
                    print("incorrect policy.\nPlease check your policy")
                    
    def main(self, user_profile, policy):
        self.attach_private_policy(user_profile=user_profile, policy=policy)
        self.attach_public_policy(user_profile=user_profile, policy=policy)


test = EcrRepos()
