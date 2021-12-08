# DeGiroDca (Dollar Cost Averaging)
DeGiro Lambda Function for Dollar Cost Averaging

### If you find this code useful you can donate here:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=CZXXCPF8BTUD6)

Inspired by https://github.com/CristaudoGiuseppe/DeGIRO-PAC

# How to set up

You need an AWS account

You also need [Docker Desktop](https://www.docker.com/products/docker-desktop) to build it

1. open serverless.yml and edit the Content section in DeGiroDcaConfigurationVersion resource 
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

1. Go to Degiro 

1. search for your product

   for example MSCI World 

1. Copy the ID in the URL and set the percentage 

   https://trader.degiro.nl/trader/#/products/4622784/overview

1. configure your aws login through `aws configure`

1. run `setup.sh username password` of your degiro account

1. [install serverless framework](https://www.serverless.com/framework/docs/getting-started)  

1. run `sls deploy --use-local-credentials`

by defult it will buy the configured amount the first monday of the month see schedule in serverless.yml to change it according [AWS Doc](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html) you can use  [Cron expression describer
](https://en.rakko.tools/tools/88/) to help with the syntax (keep in mind that AWS doesn't support seconds so you have to prepend a 0 for seconds in the expression)
