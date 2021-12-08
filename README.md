# DeGiroDca (Dollar Cost Averaging)
DeGiro Lambda Function for Dollar Cost Averaging

### If you find this code usefull you can donate here:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=CZXXCPF8BTUD6)

Inspired by https://github.com/CristaudoGiuseppe/DeGIRO-PAC

# How to set up

You need an AWS account

You also need [Docker Desktop](https://www.docker.com/products/docker-desktop) to build it

open serverless.yml and edit the Content section in DeGiroDcaConfigurationVersion resource

```
            {   
                "amount":5000,
                "ETF":[
                    {"id":"4622755", "percentile":"33.0"},
                    {"id":"4622784", "percentile":"33.0"},
                    {"id":"4622969", "percentile":"34.0"}
                ]
            }
```
amount is the amount to invest monthly

Ids are DeGiro Ids

Go to Degiro 

search for your product

for example MSCI World 

Copy the ID in the URL

https://trader.degiro.nl/trader/#/products/4622784/overview

configure your aws login through `aws configure`

run `setup.sh username password` of your degiro account

[install serverless framework](https://www.serverless.com/framework/docs/getting-started)  

run `sls deploy --use-local-credentials`
