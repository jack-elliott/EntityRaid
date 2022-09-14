import numpy as np
import json
from matplotlib import pyplot as plt

if__name__=="__main__":
    filename = "input.json"
    json_string = open(filename).read()
    input_dict = json.loads(json_string)

    # airfoils = input_dict["airfoils"]
    AirfoilCords = []
    #### past this point, not python syntax ####

    for i in number of airfoils:
        open(airfoilfile as f):
            ListofPoints = []
            for line in f:
                ListofPoints.append(line)
            f.close()
        AirfoilCords.append(ListofPoints)

    plt.figure() # Initialize a plot????

    for airfoil in AirfoilCords:
       # plt.plot(x values, y values, color, label)

    #plt.arrow(Give it starting values and difference values with some magntidue of 0.1) # Plot velocity arrow at some alpha

    # Set aspect ratio to be equal in x and y
    # THIS IS PYTHON NOW

    plt.show()


#### DYNAMICS OF SPACE FLIGHT JUNK
r0 = [1622.39; 5305.10; 3717.44]; # Initial position conditions
v0 = [-7.29936; 0.492329; 2.48304]*3600; # Initial velocity positions

h = 0.05;
x = 0:h:100; # Vector from 0 to 100 in step sizes of h
Y = zeros(1,length(x)); # I'm not sure what's going on here

F_xy = @(mu, r) diff(diff(r)) = (-mu/r^3)*r # This is the differential euqation, but I'm not sure what to do here.
# Also, this is a different type of r and mu than the bolt ones. Is there a difference here?

for i=1:(len(x)-1)
    k_1 = F_xy(x(i),y(i)));
    k_2 = F_xy(x(i)+0.5*h,y(i)+0.5*h*k_1);
    k_3 = F_xy((x(i)+0.5*h),(y(i)+0.5*h*k_2));
    k_4 = F_xy((x(i)+h),(y(i)+k_3*h));
    y(i+1) = y(i) + (1/6)*(k_1+2*k_2+2*k_3+k_4)*h;

end