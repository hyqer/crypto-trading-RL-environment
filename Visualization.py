import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style


style.use('dark_background')


class TradingGraph:
    def __init__(self, dfs, title=None):
        self.dfs = dfs
        
        #Needed to be able to iteratively update the figure
        plt.ion()    
        
        #Define our subplots
        self.fig, self.axs = plt.subplots(2,2)

        #Show the plots
        plt.show()
        
    def plot_candles(self, ax, ohlc, idx):
       for row, ix in zip(ohlc, idx):
           if row[3]<row[0]:
               clr = "red"
           else:
               clr = "green"

           ax.plot([ix, ix], [row[1], row[2]], lw=1, color=clr)
           ax.plot([ix, ix], [row[3], row[0]], lw=3, color=clr)
           
                
    def render_prices(self, current_step, lbw):     
        for splot, df in zip(self.axs.flatten(), self.dfs):
            splot.clear()
            #Format data for OHCL candlestick graph
            step_range = range(current_step-lbw, current_step)
            idx = np.array(step_range)
            
            candlesticks = zip(df['open'].values[step_range], 
                               df['high'].values[step_range],
                               df['low'].values[step_range], 
                               df['close'].values[step_range])
    
            #Plot price using candlestick graph
            self.plot_candles(splot, candlesticks, idx)
            
         
    def render_trades(self,  current_step, lbw, trades):
        for splot, coin in zip(self.axs.flatten(), trades):
            for trade in coin:
                if current_step>trade[1]>current_step-lbw:
                    if trade[0]=='buy':
                        clr = 'red'
                        splot.plot(trade[1], trade[2], 'ro')
                    else:
                        clr = 'green'
                        splot.plot(trade[1], trade[2], 'go')
                
                splot.hlines(trade[2], current_step-lbw, current_step, linestyle='dashed', colors=[clr])

    def render(self, current_step, window_size, trades):
        self.render_prices(current_step, window_size)
        self.render_trades(current_step, window_size, trades)

        
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()
        plt.pause(0.1)

    def close(self):
        plt.close()

    
    
    
    
    
