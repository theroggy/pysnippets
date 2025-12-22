import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point


def plot(polygon, ax):
    ax.plot(*polygon.exterior.xy, color="b")
    for i in polygon.interiors:
        ax.plot(*i.xy, color="r")


if __name__ == "__main__":
    # show on a unit circle                                                                    
    r = 1.0

    # create a linestring that from a closed circle of radius `r`                          
    L = LineString(Point([0, 0]).buffer(r).exterior)

    fig, axs = plt.subplots(3, 3)

    # try padding by different amounts                                                     
    for i, pad in enumerate(np.linspace(0.001, r * 2, 9)):
        # apply the buffer                                                                 
        padded = L.buffer(pad)

        # plot it                                                                          
        ax = axs[i // 3, i % 3]
        plot(padded, ax)
        ax.set_xlabel(f"pad={pad}")

        # if we have buffered the closed curve by more than the original radius            
        # there should be no interiors?                                                    
        if pad > r:
            print("should be no interiors?")
            # assert len(padded.interiors) == 0                                            

    plt.show()
