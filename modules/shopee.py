# -*- coding: utf-8 -*-
"""
    Coder: indryanto
"""

from assets import write, writeToCsv
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
import cssutils
import logging
import csv

def shopUsername():
    try:
        return str(input('Input shop username: '))
    except ValueError:
        write('Invalid input', 'exit')
    except KeyboardInterrupt:
        write('\nExit by user interrupt.', 'exit')
    except Exception as e:
        write('Error: ' + str(e), 'exit')

def getFirstPage(link):
    driver = webdriver.Chrome('utils/chromedriver')
    driver.get(link)
    sleep(5)
    webpage = driver.page_source
    driver.quit()
    return webpage

def getTotalPage(firstPage):
    soup = BS(firstPage, 'html.parser')
    return soup.find('span', 'shopee-mini-page-controller__total').get_text()

def getAllPages(username, totalPage, firstPage):
    pages = [firstPage]
    driver = webdriver.Chrome('utils/chromedriver')
    for page in range(1, int(totalPage)):
        url = 'https://shopee.co.id/%s?page=%d' % (username, page)
        driver.get(url)
        sleep(5)
        webpage = driver.page_source
        pages.append(webpage)
    driver.quit()
    return pages

def getAllLinkToDetail(allPages):
    divPages = []
    allLinks = []
    for page in allPages:
        divSoup = BS(page, 'html.parser')
        divPages.append(divSoup.find_all('div', 'shop-search-result-view__item col-xs-2-4'))
    for div in divPages:
        for a in div:
            linkSoup = BS(str(a), 'html.parser')
            allLinks.append(linkSoup.find('a').get('href'))
    return allLinks

def checkImageStyle(divTag):
    try:
        if divTag['style']:
            return True
        else:
            return False
    except:
        return False

def gettingData(link, driver):
    finalData = dict()
    try:
        url = 'https://shopee.co.id/%s' % (link)
        data = dict()
        driver.get(url)
        sleep(2)
        webpage = driver.page_source
        print(webpage)
        pageSoup = BS(webpage, 'html.parser')
        print(pageSoup)
        productName = pageSoup.find('div', 'qaNIZv').text
        print(productName)
        if pageSoup.find('div', 'MITExd'):
            print('pricing if')
            price = pageSoup.find('div', '_3n5NQx').text
            print(price)
            discount = pageSoup.find('div', 'MITExd').text
            print(discount)
            originalPrice = pageSoup.find('div', '_3_ISdg').text
            print(originalPrice)
            discountPrice = pageSoup.find('div', '_3n5NQx').text
            print(discount)
        else:
            print('pricing else')
            discount = None
            print(discount)
            price = pageSoup.find('div', '_3n5NQx').text
            print(price)
            originalPrice = pageSoup.find('div', '_3n5NQx').text
            print(originalPrice)
            discountPrice = None
            print(discountPrice)
        variationAvailable = []
        variationUnavailable = []
        if pageSoup.find('button', 'product-variation'):
            print('variation if')
            variationTemp = pageSoup.find_all('button', 'product-variation')
            print(variationTemp)
            for i in variationTemp:
                print('variation for')
                if 'product-variation--disabled' not in i.attrs['class']:
                    print('variation availabe if')
                    variationAvailable.append(BS(str(i), 'html.parser').find('button').text)
                else:
                    print('variation unavailabe if')
                    variationUnavailable.append(BS(str(i), 'html.parser').find('button').text)
        images = []
        imageStyleTemp = pageSoup.find_all('div', '_2Fw7Qu')
        print(imageStyleTemp)
        for i in imageStyleTemp:
            print('imageStyleTemp for')
            cssutils.log.setLevel(logging.CRITICAL)
            divTag = BS(str(i), 'html.parser').find('div')
            print(divTag)
            if checkImageStyle(divTag):   
                imageTemp = cssutils.parseStyle(divTag['style'])['background-image']
                print(imageTemp)
                images.append(imageTemp.replace('url(', '').replace('_tn)', ''))
                print('images.append')
        productDescription = pageSoup.find('div', '_2u0jt9').findChild('span').text
        print(productDescription)
        productCategory = pageSoup.find('div', '_1z1CEl').find_all('a')[1].text
        print(productCategory)
        productStock = pageSoup.find('div', '_1FzU2Y').findChildren('div')[-1].text.replace('tersisa ', '').replace(' buah', '')
        print(productStock)
        data['productName'] = productName
        data['discount'] = discount
        data['price'] = price
        data['originalPrice'] = originalPrice
        data['discountPrice'] = discountPrice
        data['variationAvailable'] = variationAvailable
        data['variationUnavailable'] = variationUnavailable
        data['images'] = images
        data['productDescription'] = productDescription
        data['productCategory'] = productCategory
        data['productStock'] = productStock
        finalData['data'] = data
        finalData['status'] = True
        return finalData
    except KeyboardInterrupt:
        write('Exit by user interrupt', 'exit')
    except:
        finalData['status'] = False
        finalData['data'] = None
        return finalData


def getDataByProduct(links):
    datas = []
    driver = webdriver.Chrome('utils/chromedriver')
    currentLink = 1
    totalLinks = len(links)
    for link in links:
        write('link ' + str(currentLink) + ' from ' + str(totalLinks), 'noLine')
        looping = True
        while looping:
            data = gettingData(link, driver)
            if bool(data['status']):
                datas.append(data['data'])
                currentLink += 1
                looping = False
            else:
                looping = True
    driver.quit()
    return datas

def shopeeScraper():
    try:
        username = shopUsername()
        headers = ['productName', 'discount', 'price', 'originalPrice', 'discountPrice', 'variationAvailable', 'variationUnavailable', 'images', 'productDescription', 'productCategory', 'productStock']
        link = 'https://shopee.co.id/' + username
        firstPage = getFirstPage(link)
        totalPage = getTotalPage(firstPage)
        allPages = getAllPages(username, totalPage, firstPage)
        allLinksToDetail = getAllLinkToDetail(allPages)
        allDataByProduct = getDataByProduct(allLinksToDetail)
        writeToCsv(username, allDataByProduct, headers, 'shopee')
        # writeToCsv(allDataByProduct)
    except KeyboardInterrupt:
        write('\nExit by user interrupt', 'exit')
    except Exception as e:
        write('Error ' + str(e), 'exit')
