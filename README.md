## Pulumi introduction

Pulumi is a tool for building, changing, and versioning infrastructure safely and efficiently. Pulumi can manage existing and popular service providers as well as custom in-house solutions.


## Requirements

- (Pulumi)[https://www.pulumi.com/docs/get-started/install/] 2.*
- (Python 3.6 or later)[https://www.python.org/downloads/]

## AWS authentification
The AWS provider is used to interact with the many resources supported by AWS.
The provider needs to be (configured)[https://docs.aws.amazon.com/fr_fr/cli/latest/userguide/cli-configure-envvars.html] 
with the proper credentials before it can be used.

```
export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export AWS_DEFAULT_REGION=us-west-2
```

## Getting Started

Before Pulumi apply you create on account on (pulumi website)[https://www.pulumi.com/docs/intro/console/accounts-and-organizations/accounts/]:

After you can login to pulumi.com with your (authentification token)[https://www.pulumi.com/docs/reference/cli/pulumi_login/#synopsis]:

```
pulumi login
```

## Documentation
- (Pulumi aws getting started)[https://www.pulumi.com/docs/get-started/aws/begin/]
- (AWS Authentification)[https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html]
