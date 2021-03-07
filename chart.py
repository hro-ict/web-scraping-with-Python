
#https://www.delftstack.com/howto/matplotlib/how-to-set-the-figure-title-and-axes-labels-font-size-in-matplotlib/
import matplotlib.pylab as plt
import os
parameters = {'ytick.labelsize': 25,
'xtick.labelsize': 18,
              'axes.titlesize': 60}
plt.rcParams.update(parameters)
#plt.rcParams.update({'font.size': 18})

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 40,
        }
def chart(x,y, file,title):
    plt.figure(figsize=(40.5, 20.5))
    #plt.plot(range(100))
    x_ax= x
    y_ax= y
    plt.xticks(rotation=70)
    plt.suptitle(title, fontsize=60)
    plt.xlabel('Time',fontdict=font)
    plt.ylabel('Value',fontdict=font)
    plt.plot(x,y)
    plt.grid(color='red', linestyle='--', linewidth=0.5)
    plt.savefig('{}.png'.format(file))
