import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib
import numpy as np
from pyproj import Proj
from shapely.geometry import shape, Polygon

matplotlib.use("TkAgg")

fig, ax = plt.subplots(figsize=(20, 15), dpi=334)

x = [-106.91057, -106.91059, -106.91082, -106.91085, -106.9109, -106.91097, -106.911156, -106.911156, -106.911156,
     -106.911385, -106.912, -106.912025, -106.912025, -106.912285, -106.91248, -106.912895, -106.914154, -106.91486,
     -106.91495, -106.91505, -106.91512, -106.91522, -106.91546, -106.91548, -106.915634, -106.92165, -106.921936,
     -106.921936, -106.93207, -106.941956, -106.94203, -106.94203, -106.94247, -106.943184]
y = [32.570984, 32.571163, 32.57705, 32.56993, 32.57075, 32.57756, 32.57144, 32.57144, 32.571342, 32.57029, 32.57019,
     32.57024, 32.57019, 32.578255, 32.570854, 32.57057, 32.571262, 32.57651, 32.57646, 32.576305, 32.57513, 32.576565,
     32.57641, 32.57651, 32.572212, 32.579327, 32.579506, 32.579403, 32.585396, 32.596455, 32.596428, 32.59638, 32.5972,
     32.597042]
##################################
cx = [-106.91057, -106.91059, -106.91082, -106.91097, -106.911156, -106.911156, -106.912285, -106.94247, -106.943184,
      -106.93207, -106.915634, -106.914154, -106.912895, -106.912025, -106.91085]
cy = [32.570984, 32.571163, 32.57705, 32.57756, 32.57144, 32.57144, 32.578255, 32.5972, 32.597042, 32.585396, 32.572212,
      32.571262, 32.57057, 32.57019, 32.56993]
##################################
hx = [-106.91085, -106.91057, -106.91082, -106.91097, -106.94247, -106.943184, -106.93207, -106.915634, -106.914154,
      -106.912895, -106.912025]
hy = [32.56993, 32.570984, 32.57705, 32.57756, 32.5972, 32.597042, 32.585396, 32.572212, 32.571262, 32.57057, 32.57019]

# plt.plot(x, y, 'bo', ms=0.5)
# plt.plot(hx, hy, 'r+', ms=0.5)


# trans input to np.array
points_list = []
for i in range(len(x)):
    points_list.append([x[i], y[i]])
points = np.array(points_list)

# remove the duplicated points
unique_points = np.unique(points, axis=0)

# find the convex hull
hull = ConvexHull(unique_points)

# draw the input points
plt.plot(unique_points[:, 0], unique_points[:, 1], 'o', ms=0.5)
# plt.plot(points[:, 0], points[:, 1], 'o')


# # # #
# draw the convex hull
# plt.plot(hx, hy, 'r--', lw=1)
# plt.plot([hx[-1], hx[0]], [hy[-1], hy[0]], 'r--', lw=1)

# draw the convex hull by using the simplices of the hull
for simplex in hull.simplices:
    plt.plot(unique_points[simplex, 0], unique_points[simplex, 1], 'k-')

print()

"""
https://stackoverflow.com/questions/4681737/how-to-calculate-the-area-of-a-polygon-on-the-earths-surface-using-pytho
"""
# project coordinates
lon, lat = zip(*[unique_points[hull.vertices, :]][0])
pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=39.0 +lon_0=-106.55")
x, y = pa(lon, lat)

# calculate the area by using the shape object
cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
print(shape(cop).area)  # 268952044107.43506

# calculate by using the Polygon object
ob = [zip(x, y)]
print(Polygon(ob[0], ob[1:]).area / 1e+6)  # square meters to square kilometer

# plt.show()
