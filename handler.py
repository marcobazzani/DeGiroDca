try:
  import unzip_requirements
except ImportError:
  pass

import os
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import json, logging, csv, random
import boto3
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeGiroDcaException(Exception):
    pass

def run(event, context):
    current_time = datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    try:
        return  {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(DeGiroDca(context.function_name).run())
        }

    except DeGiroDcaException as e:
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "headers": {},
            "body": e
        }

class DeGiroDca():
    
    orders = {}
    degiro = degiroapi.DeGiro()
    appconfig = boto3.client('appconfig')
    ssm_client = boto3.client('ssm')

    def __init__(self, context):
        json_dump = self.appconfig.get_configuration(
            Application=os.environ['APPLICATION'],
            Environment=os.environ['ENVIRONMENT'],
            Configuration=os.environ['CONFIGURATION'],
            ClientId=context
        )['Content'].read().decode()

        self.config = json.loads(json_dump)

        logger.info('[CONFIG LOADED SUCCESSFULLY]')
        
        self.username = self.ssm_client.get_parameter(Name="/degirodca/account/username",WithDecryption=True)['Parameter']['Value']
        self.password = self.ssm_client.get_parameter(Name="/degirodca/account/password",WithDecryption=True)['Parameter']['Value']

        self.amount = int(self.config['amount'])
        if self.username == "" or self.password == "":
            message = '[MISSING USERNAME OR PASSWORD FROM CONFIG FILE]'
            logger.error(message)
            raise DeGiroDcaException(message)


            
    def login(self): # log into your account
        return self.degiro.login(self.username, self.password)
        
    def get_product_data(self): # get info from the config file and update a dict with the wty to buy
        for product in self.config['ETF']:
            # check the amount dedicated to each ETF
            m = float(self.amount * float(product['percentile']) / 100)
            # get actual price
            realprice = self.degiro.real_time_price(str(product['id']), degiroapi.Interval.Type.One_Day)
            # get the amount of share to buy in respect to real time price
            to_buy = int(m/realprice[0]['data']['lastPrice'])
            # update the dict
            self.orders.update({product['id']:to_buy})
        # amount cash held on the account
        self.amount_on_broker  = float(str(self.degiro.getdata(degiroapi.Data.Type.CASHFUNDS)[0]).split(" ")[1])
        return {
            "amount_on_broker": self.amount_on_broker,
            "orders": self.orders
        }
        
    def buy_product(self):
        payload = []
        if self.amount_on_broker > self.amount:
            for order in self.orders:
                self.degiro.buyorder(Order.Type.MARKET, order, 3, int(self.orders.get(order)))
                logger.info('[BUY ORDER][ID: ' + order + '][QUANTITY: ' + str(self.orders.get(order)) + ']')

            # check if orders were successfull
            orders = self.degiro.orders(datetime.now() - timedelta(days = 1), datetime.now())
            i = len(self.onfig['ETF'])
            while (i != 0):
                if orders[-i]['status'] == 'CONFIRMED':
                    productID = orders[-i]['productId']
                    amountBought = orders[-i]['size']
                    name = self.degiro.product_info(productID)['name']
                    price = orders[-i]['price']
                    description = name + ' x ' + str(amountBought)
                    
                    logger.info('[ORDER CONFIRMED][ID: ' + productID + '][NAME: ' + name + '][QUANTITY: ' + str(amountBought) + ']')

                    value = {
                        'timestamp': str(date.today()),
                        'productId': productID,
                        'name': name,
                        'amountBought': amountBought,
                        'price': price, 
                        'total': price * amountBought
                    }
                    payload.append(value)
                    self.send_webhook('ORDER CONFIRMED', description, '008000')
                else:
                    logger.warning('[ORDER NOT CONFIRMED]')
                    self.send_webhook('ORDER FAILED',  orders[-i]['productId'], 'ff0000')
                i -= 1
        else:
            logger.warning('[NOT ENOUGHT MONEY TO START BUYING]')
            self.send_webhook('FAILED BUYING',  'NOT ENOUGHT MONEY TO START BUYING', 'ff0000')
        return payload
            
    def portfolio_update(self):
        labels = []
        sizes = []
        colors = []
        portfolio = self.degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        payload = []
        for data in portfolio:
            if data['id'] != 'FLATEX_EUR':
                productID = data['id']
                name = self.degiro.product_info(productID)['name']
                value = {
                    'timestamp': str(date.today()),
                    'productId': productID,
                    'name': name,
                    'size': data['size'],
                    'value': data['value'], 
                    'value_price': data['value']/data['price']
                }
                payload.append(value)
        return payload
                # color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                # labels.append(name)
                # sizes.append(float(data['value']))
                # colors.append(color)
                
        #plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        #plt.savefig('outcome/portfolio_status.png')
        #plt.show()
        
    def logout(self): # logout from de giro account
        self.degiro.logout()
        return True

            
        
    def send_webhook(self, title, descriprion, color):
        pass
        #embed = DiscordEmbed(title = title, description = descriprion, color = color)

            
    def run(self):
        return {
            "login": self.login(),
            "product_data": self.get_product_data(),
            "bought_product": self.buy_product(),
            "portfolio": self.portfolio_update(),
            "logout": self.logout()
        }





    
