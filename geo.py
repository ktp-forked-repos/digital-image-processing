"""
IMPORTS
"""
import numpy as np
import ipcv
import cv2

"""
PYTHON METHOD DEFINITION
"""
def remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0):
    """
    Function to transform the src image using the maps

    Args:
        src (array): source image
        map1 (array): the first map, the x value for a given coord
        map2 (array): the second map, the y value for a given coord
        interpolation (optional[int]): type of interpolation to use
            defaults to Nearest-neighbor
        borderMode (optional[int]): type of border to include outside the image
            defaults to constant value
        borderValue (optional[int]): border value for constant value border
            defaults to 0 (black)

    Returns:
        the source modified to the new mappings
    """
    pass

"""
PYTHON TEST HARNESS
"""
if __name__ == '__main__':

    """
    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    src = cv2.imread(filename)

    map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])

    startTime = time.clock()
    dst = ipcv.remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remap) = {0} [s]'.format(elapsedTime))

    srcName = 'Source (' + filename + ')'
    cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(srcName, src)

    dstName = 'Destination (' + filename + ')'
    cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(dstName, dst)

    ipcv.flush()
    """
"""
PYTHON METHOD DEFINITION
"""
def map_rotation_scale(src, rotation=0, scale=[1, 1]):
    """
    Function to rotate or scale image

    Args:
        src (array): source image to transform
        rotation (int): degrees to rotate image by
        scale (array): factors to scale image by in the x (0th) and y (1st)

    Returns:
        two maps, of x values and y values
    """

    # rotation matrix (based on slides)
    rotateMatrix = np.array([
        np.cos(np.radians(rotation)),
        np.sin(np.radians(rotation)),
        -np.sin(np.radians(rotation)),
        np.cos(np.radians(rotation))
    ])
    rotateMatrix = rotateMatrix.reshape(2,2)

    # scale matrix (based on notes)
    scaleMatrix = np.array([
        1/scale[0], 0,
        0, 1/scale[1]
    ])
    scaleMatrix = scaleMatrix.reshape(2,2)

    # max matrix (to get the edges of dst)
    maxMatrix = np.array([
        scale[0], 0,
        0, scale[1]
    ])
    maxMatrix = maxMatrix.reshape(2,2)

    # transformations
    transformMatrix = np.dot(rotateMatrix, scaleMatrix)
    edgeMatrix = np.dot(rotateMatrix, maxMatrix)

    print("TRANSFORM:\n", transformMatrix)
    print("EDGE:\n", edgeMatrix)

    # get the size of the Destination Map
    corners = np.array([
        [0,0],
        [0, src.shape[1]],
        [src.shape[0], 0],
        [src.shape[0], src.shape[1]]
    ])

    # set up min and max values to compare against with
    # the transformed corners
    minX, minY = float('inf'), float('inf')
    maxX, maxY = float('-inf'), float('-inf')

    for xyPair in corners:
        x, y = np.dot(edgeMatrix, xyPair)
        minX = min(minX, x)
        minY = min(minY, y)
        maxX = max(maxX, x)
        maxY = max(maxY, y)

    # print("minX", minX)
    # print("minY", minY)
    # print("maxX", maxX)
    # print("maxY", maxY)

    # we can't have non-zero indexing, so we'll shift after the fact
    xshift = -minX
    yshift = -minY

    xwidth = maxX + xshift
    ywidth = maxY + yshift
    # print("x:", np.ceil(xwidth))
    # print("y:", np.ceil(ywidth))

    xs = np.zeros((xwidth, ywidth))
    ys = np.zeros((xwidth, ywidth))

    for row in range(xs.shape[0]):
        for col in range(xs.shape[1]):

            # offset the values to center the rotation
            offX = row - (xs.shape[0]/2)
            offY = (xs.shape[1]/2) - col

            offs = np.array([offX, offY])
            # print("OFFS", offs)

            # transform the points
            xp, yp = np.dot(transformMatrix, offs)

            # print("TRANS", [xp, yp])

            # un-offset them, and place them in the final maps
            unoffX = (xp + (src.shape[0]/2))
            unoffY = ((src.shape[1]/2) - yp)

            # print("UNOFFS", [unoffX, unoffY])

            xs[row,col] = unoffX
            ys[row,col] = unoffY


    xs = xs.astype('float32')
    ys = ys.astype('float32')
    return (xs, ys)


"""
PYTHON TEST HARNESS
"""
if __name__ == '__main__':

    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    src = cv2.imread(filename)

    startTime = time.clock()
    #map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])
    map1, map2 = ipcv.map_rotation_scale(src, rotation=0, scale=[1.0, 1.0])
    elapsedTime = time.clock() - startTime
    print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime))

    startTime = time.clock()
    dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
    #   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remapping) = {0} [s]'.format(elapsedTime))

    srcName = 'Source (' + filename + ')'
    cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(srcName, src)

    dstName = 'Destination (' + filename + ')'
    cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(dstName, dst)

    ipcv.flush()

"""
PYTHON METHOD DEFINITION
"""
def map_gcp(src, map, srcX, srcY, mapX, mapY, order=1):
    """
    Function to distort map image to fall on the coordinates of the source

    Args:
        src (array): source image
        map (array): image to distort
        srcX (array): list of x values for a set of points on the source image
        srcY (array): list of y values for a set of points on the source image
        mapX (array): list of x values for a set of points on the map image
        mapY (array): list of y values for a set of points on the map image
        order (optional[int]): order of polynomial to do mapping

    Returns:
        An image of the map with the points placed in the coordinates of the src
    """
    pass

"""
PYTHON TEST HARNESS
"""
if __name__ == '__main__':

    """
    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    imgFilename = home + os.path.sep + \
               'src/python/examples/data/registration/image.tif'
    mapFilename = home + os.path.sep + \
               'src/python/examples/data/registration/map.tif'
    gcpFilename = home + os.path.sep + \
               'src/python/examples/data/registration/gcp.dat'
    src = cv2.imread(srcFilename)
    map = cv2.imread(mapFilename)

    srcX = []
    srcY = []
    mapX = []
    mapY = []
    linesRead = 0
    f = open(gcpFilename, 'r')
    for line in f:
        linesRead += 1
        if linesRead > 2:
           data = line.rstrip().split()
           srcX.append(float(data[0]))
           srcY.append(float(data[1]))
           mapX.append(float(data[2]))
           mapY.append(float(data[3]))
    f.close()

    startTime = time.clock()
    map1, map2 = ipcv.map_gcp(src, map, srcX, srcY, mapX, mapY, order=2)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime))

    startTime = time.clock()
    dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
    #   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remap) = {0} [s]'.format(elapsedTime))

    srcName = 'Source (' + srcFilename + ')'
    cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(srcName, src)

    mapName = 'Map (' + mapFilename + ')'
    cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(mapName, map)

    dstName = 'Warped (' + mapFilename + ')'
    cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(dstName, dst)

    ipcv.flush()
    """