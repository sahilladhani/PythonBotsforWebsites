import requests, bs4
import json
from fuzzywuzzy import fuzz
import re
from credentials.credentials import Credentials
import platform
from datetime import datetime
import time

class FetchProductData:

    def __init__(self):
        self.product_list = []

    def product_details(self, link, unit_of_measurement, min_order_weight, product_origin, product_description, prices,currency,converted_min_price,converted_max_price):
        min_price = None
        max_price = None
        if len(prices) == 1:
            min_price = prices[0]
            max_price = prices[0]
        else:
            min_price = prices[0]
            max_price = prices[1]
        self.product_list.append(
            {'description': product_description,
             'min_price': prices,
             'max_price': prices,
             'currency': currency,
             'weight': min_order_weight,
             'unit': unit_of_measurement,
             'origin': product_origin,
             'link': link,
             'website': "ishopping.pk",
             'converted_min_price':converted_min_price,
             'converted_max_price':converted_max_price})

    def find_data(self, description, origin,credentials):

        data = None
        api_result = None

        web_soup = None

        check = True

        while(check):
            try:

                base_url = 'https://www.ishopping.pk/search/?q='
                params = credentials.get_proxycrawl_credentails(url = base_url + description)
                params['token']='dB35Y2RoUcjbCxqapH1w0w'
                params['page_wait']=3000
                proxy_url = credentials.get_proxycrawl_url()
                api_result = requests.get(proxy_url, params)
                web_soup = bs4.BeautifulSoup(api_result.content, "html.parser")

                check = False
            except Exception as e:
                print(e)
                check = True
                pass

        if len(web_soup.findAll('div',{'class':'kuName'})) != 0:
            data = self.fetch_data(web_soup, description, origin)
            print(data)
        else:
           data = []

        # return_dict['ishopping'] = data
        #
        # return return_dict


    def fetch_data(self, web_soup, description, origin):

        list_of_products = web_soup.findAll('div',{'class':'kuName'})
        price_list = web_soup.findAll('div',{'class':'kuSalePrice'})
        index=0
        try:
            for Data_from_websites in list_of_products:
                price_from_website = price_list[index].text
                min_order_weight = None
                min_order_unit = None
                link = None
                product_description = None
                prices = None
                currency = None
                convertedprice1  = None
                convertedprice2 =  None

                if price_from_website is not None and price_from_website != '':
                    try:
                        link = Data_from_websites.find('a').get('href')
                        product_description = Data_from_websites.find('a').text
                        P1= price_from_website
                        currency ="PKR"
                        unit_of_measurement = None
                        prices=str(P1).replace("PKR",'').split('/')
                        min_order_weight = None
                        description = description.lower()
                        product_description = product_description.lower()

                        convertedprice1=0
                        convertedprice2=0
                    except Exception as ex:
                        print(ex)
                        print("line 201 EXCEPTION")
                            # prices = [float(p) for p in re.findall(r'-?\d+\.?\d*', list_of_prices)]

                    product_description = product_description.lower()
                    product_origin = "PK"
                    description = description.lower()
                    reCheck = re.search(r'(\D*)?(\d+)\s*/?(\w+)$', product_description)
                    if reCheck is not None and len(reCheck.groups()) != 0:
                        if len(reCheck.groups()) > 1:
                            unit_of_measurement= reCheck.groups()[-1]
                            min_order_weight = reCheck.groups()[-2]

                    if description in product_description:

                        self.product_details(link, unit_of_measurement, min_order_weight, product_origin,
                                                product_description, prices,currency,convertedprice1,convertedprice2)

                    elif fuzz.token_set_ratio(description, product_description) >= 85:

                        self.product_details(link, min_order_unit, min_order_weight, product_origin,
                                                product_description, prices,currency,convertedprice1,convertedprice2)



                else:
                    print("price not fetched")
                index = index + 1
        except:
            pass

        return self.product_list


if __name__ == "__main__":
    origin = ''
    description = 'phone'
    credentials=Credentials()
    fetch_products = FetchProductData()
    fetch_products.find_data(description, origin,credentials)
