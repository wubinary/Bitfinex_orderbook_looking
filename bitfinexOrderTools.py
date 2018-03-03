from client import *
import time

class BitfinexOrder():
    def __init__(self):
        self.client = Client() #bitfinex 
    def ordersNow(self, symbol='ethusd', limitBids=100, limitAsks=100):
        ordersNow = self.client.order_book(symbol, {'limit_bids':limitBids, 'limit_asks':limitAsks} )   #bids:buyorders, asks:sellorders
        return ordersNow
    def showOrdersNow(self, symbol='ethusd', limitBids=100, limitAsks=100, type_='all'):
    	ordersNow = self.ordersNow(symbol, limitBids, limitAsks)
        if type_=='bids':
            for item in ordersNow['bids']:
                print item
        elif type_=='asks':
            for item in ordersNow['asks']:
                print item
        else:
            for item in ordersNow['bids']:
                print item
            for item in ordersNow['asks']:
                print item
class BitfinexOrderTools(BitfinexOrder):
	def __init__(self):
		pass
	def ordersNowDistribution(self):
		tstart = time.time()
		orders=BitfinexOrder().ordersNow()
		###########
		#find max and min for bids and asks
		par = {'bids':{'max':0,'min':100000},'asks':{'max':0,'min':100000}}
		par['bids']['max'] = int(orders['bids'][0]['price'])
		par['bids']['min'] = int(orders['bids'][len(orders['bids'])-1]['price'])
		par['asks']['min'] = int(orders['asks'][0]['price'])
		par['asks']['max'] = int(orders['asks'][len(orders['asks'])-1]['price'])
		#par complete

		###########
		#initial distribution dictionary
		#EX: dis = {'bids':[[560,2], [561,1], [562,6]...... ], 'asks':[[575,20], [576,4], [577,6]...... ]}
		dis = {'bids':[], 'asks':[]}
		for i in range(par['bids']['min'],par['bids']['max']+1):
			dis['bids'].append([i,0])
		for i in range(par['asks']['min'],par['asks']['max']+1):
			dis['asks'].append([i,0])
		#calculate the distribution of bids and asks
		for order in orders['bids']:
			dis['bids'][int(order['price'])-par['bids']['min']][1]+=1
		for order in orders['asks']:
			dis['asks'][int(order['price'])-par['asks']['min']][1]+=1
		#dis complete
		print 'cost %f sec complete ordersNowDistribution' % (time.time()-tstart)
		return par, dis
	def drawOrdersNowDistribution(self):
		par,dis = self.ordersNowDistribution()
		print par,dis
bitfinexOrderTools = BitfinexOrderTools()
bitfinexOrderTools.drawOrdersNowDistribution()
        
a = {'a':3,'aa':3}
print a.keys()
print a.items()[1][1]
a.clear()
print a