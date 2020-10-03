import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker


def plot_persistence(filtration, name, filename):
    lifetimes = np.array(filtration.lifetimes)
    sizes = np.array(filtration.sizes)

    fig = plt.figure(figsize = (6,6))
    ax = fig.add_axes([0,0,1,1], aspect = 1)
    ax.scatter(lifetimes, sizes, c = lifetimes/sizes, cmap = "cool", zorder = 2)

    k = 1
    for xy in zip(filtration.lifetimes, filtration.sizes):
        plt.annotate(f"{k}", xy, bbox = dict(facecolor = 'white', edgecolor = 'white',
            alpha = 0.5, zorder = 1))
        k += 1

    ax.xlabel('Lifetime (normalised)')
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1))
    ax.ylabel('Size (normalised)')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1))
    
    ax.title(name)
    fig.savefig(filename)

