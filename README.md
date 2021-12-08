# DeGiroDca (Dollar Cost Averaging)
DeGiro Lambda Function for Dollar Cost Averaging

Inspired by https://github.com/CristaudoGiuseppe/DeGIRO-PAC

# How to set up

You need an AWS account

open serverless.yml and edit the Content section in DeGiroDcaConfigurationVersion resource

configure your aws login through `aws configure`

run `setup.sh username password` of your degiro account

[install serverless framework](https://www.serverless.com/framework/docs/getting-started)  

run sls deploy --use-local-credentials
