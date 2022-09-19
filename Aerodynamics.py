import numpy as np
import json
from matplotlib import pyplot as plt

if __name__ == "__main__":
    filename = "input.json"
    json_string = open(filename).read()
    input_dict = json.loads(json_string),

    airfoils = input_dict["airfoils"]
    AirfoilCords = []
    #### past this point, not python syntax ####

    for i in range(len(airfoils)): # for i in number of airfoils
        with open("NACA_2412_200.txt") as f:
            ListofPoints = []
            for lines in f:
                ListofPoints.append(lines)
            f.close()
        AirfoilCords.append(ListofPoints)

    plt.figure()  # Initialize a plot

    for airfoil in AirfoilCords:
        plt.plot(x values, y values, color = "Blue", label = "Airfoil")
      #  plt.arrow(Give it starting values and difference values with some magntidue of 0.1) # Plot velocity arrow at some alpha

        plt.axes().set_aspect('equal')

    plt.show()

