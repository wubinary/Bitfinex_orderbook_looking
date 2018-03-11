from client import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import time

class BitfinexOrder():
    def __init__(self):
        self.client = Client() #bitfinex 
    def ordersNow(self, symbol='ethusd', limitBids=1000, limitAsks=1000):
        ordersNow = self.client.order_book(symbol, {'limit_bids':limitBids, 'limit_asks':limitAsks} )   #bids:buyorders, asks:sellorders
        return ordersNow
    def showOrdersNow(self, symbol='ethusd', limitBids=1000, limitAsks=1000, type_='all'):
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
	def ordersNowDistribution(self, symbol='ethusd', limitBids=1000, limitAsks=1000):
		tstart = time.time()
		orders=BitfinexOrder().ordersNow(symbol, limitBids, limitAsks)
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
		#EX: dis = {'bids':[[560, 2, 0.6], [561, 1, 1.2], ...... ], 'asks':[[575, 20, 2.0], [576, 4, 3.1], ..... ]}
		#					[price, transactions, amount]
		dis = {'bids':[], 'asks':[]}
		for i in range(par['bids']['min'],par['bids']['max']+1):
			dis['bids'].append([i,0,0])
		for i in range(par['asks']['min'],par['asks']['max']+1):
			dis['asks'].append([i,0,0])
		#calculate the distribution of bids and asks
		for order in orders['bids']:
			dis['bids'][int(order['price'])-par['bids']['min']][1]+=1
			dis['bids'][int(order['price'])-par['bids']['min']][2]+=order['amount']
		for order in orders['asks']:
			dis['asks'][int(order['price'])-par['asks']['min']][1]+=1
			dis['asks'][int(order['price'])-par['asks']['min']][2]+=order['amount']
		#dis complete
		print 'cost %f sec complete ordersNowDistribution' % (time.time()-tstart)
		return par, dis
	def listReshape(self, list):
		listRet = [[],[],[]]
		for item in list:
			listRet[0].append(item[0])
			listRet[1].append(item[1])
			listRet[2].append(item[2])
		return listRet
	def drawOrdersNowDistribution3D(self, symbol='ethusd', limitBids=1000, limitAsks=1000):
		par,dis = self.ordersNowDistribution(symbol, limitBids, limitAsks)
		disReshape = {'bids':self.listReshape(dis['bids']), 'asks':self.listReshape(dis['asks'])}
		fig = plt.figure(1)
		ax = plt.axes(projection='3d')
		ax.plot3D(disReshape['bids'][0], disReshape['bids'][1], disReshape['bids'][2], color='green')
		ax.plot3D(disReshape['asks'][0], disReshape['asks'][1], disReshape['asks'][2], color='blue')
		ax.set_title('"{}"{}'.format(symbol,' ordersNowDistribution visialize (green:bids,blue:asks)'))
		ax.set_xlabel('price')
		ax.set_ylabel('orders')
		ax.set_zlabel('amount')
		plt.grid(True)
		plt.show()
		#print par,dis
	def drawOrdersNowDistribution3Dcontinuously(self, symbol='ethusd', limitBids=1000, limitAsks=1000):
		fig = plt.figure(1)
		ax = plt.axes(projection='3d')
		while True:
			par,dis = self.ordersNowDistribution(symbol, limitBids, limitAsks)
			disReshape = {'bids':self.listReshape(dis['bids']), 'asks':self.listReshape(dis['asks'])}
			ax.cla()
			ax.plot3D(disReshape['bids'][0], disReshape['bids'][1], disReshape['bids'][2], color='green')
			ax.plot3D(disReshape['asks'][0], disReshape['asks'][1], disReshape['asks'][2], color='blue')
			ax.set_title('"{}"{}'.format(symbol,' ordersNowDistribution visialize (green:bids,blue:asks)'))
			ax.set_xlabel('price')
			ax.set_ylabel('orders')
			ax.set_zlabel('amount')
			ax.grid(True)
			plt.pause(5)
	def drawOrdersNowDistribution2D(self, symbol='ethusd', limitBids=1000, limitAsks=1000):		
		par,dis = self.ordersNowDistribution(symbol, limitBids, limitAsks)
		disReshape = {'bids':self.listReshape(dis['bids']), 'asks':self.listReshape(dis['asks'])}
		fig,(ax0,ax1) = plt.subplots(2,1)
		fig.subplots_adjust(hspace=0.5)
		ax0.plot(disReshape['bids'][0], disReshape['bids'][1], color='green')
		ax0.plot(disReshape['asks'][0], disReshape['asks'][1], color='blue')
		ax0.set_xlabel('price')
		ax0.set_ylabel('orders')
		ax0.grid(True)
		ax0.set_title('"{}"{}'.format(symbol,' ordersNowDistribution visialize (green:bids,blue:asks)'));
		ax1.plot(disReshape['bids'][0], disReshape['bids'][2], color='green')
		ax1.plot(disReshape['asks'][0], disReshape['asks'][2], color='blue')
		ax1.set_xlabel('price')
		ax1.set_ylabel('amount')
		ax1.grid(True)
		plt.show()
		#plt.show()
	def drawOrdersNowDistribution2Dcontinuously(self, symbol='ethusd', limitBids=1000, limitAsks=1000):
		fig,(ax0,ax1) = plt.subplots(2,1)
		fig.subplots_adjust(hspace=0.5)
		while True:
			par,dis = self.ordersNowDistribution(symbol, limitBids, limitAsks)
			disReshape = {'bids':self.listReshape(dis['bids']), 'asks':self.listReshape(dis['asks'])}
			ax0.cla()
			ax0.plot(disReshape['bids'][0], disReshape['bids'][1], color='green')
			ax0.plot(disReshape['asks'][0], disReshape['asks'][1], color='blue')
			ax0.set_xlabel('price')
			ax0.set_ylabel('orders')
			#ax0.set_ylim(0,10)
			ax0.grid(True)
			ax0.set_title('"{}"{}'.format(symbol,' ordersNowDistribution visialize (green:bids,blue:asks)'));
			ax1.cla()
			ax1.plot(disReshape['bids'][0], disReshape['bids'][2], color='green')
			ax1.plot(disReshape['asks'][0], disReshape['asks'][2], color='blue')
			ax1.set_xlabel('price')
			ax1.set_ylabel('amount')
			ax1.grid(True)
			plt.pause(5)
			#plt.clear()
		#plt.show()


bitfinexOrderTools = BitfinexOrderTools()
bitfinexOrderTools.drawOrdersNowDistribution2D('ethusd', 50, 50)
bitfinexOrderTools.drawOrdersNowDistribution3D('zecusd', 150, 150)
bitfinexOrderTools.drawOrdersNowDistribution2Dcontinuously('ethusd', 50, 50)
bitfinexOrderTools.drawOrdersNowDistribution3Dcontinuously('btcusd', 100, 100)
        
#a = {'a':3,'aa':3}
#print a.keys()
#print a.items()[1][1]
#a.clear()
#print a