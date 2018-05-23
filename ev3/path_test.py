path = []

def calc_path(startpoint, midpoint, destpoint):
    
    if (midpoint[0] == startpoint[0]):             # mY == sY => increment X
        path.append([startpoint[0], startpoint[1]])
        newpoint = [startpoint[0], startpoint[1]]
        newpoint[1] += 1
    
        while (newpoint[1] < midpoint[1]):
            path.append([newpoint[0], newpoint[1]])
            newpoint[1] += 1
        path.append([midpoint[0], midpoint[1]])
        newpoint2 = [midpoint[0], midpoint[1]]
        newpoint2[0] += 1

        while (newpoint2[0] < destpoint[0]):
            path.append([newpoint2[0], newpoint2[1]])
            newpoint2[0] += 1
        path.append(destpoint)

    else:                            # mY != sY => increment Y
        path.append([startpoint[0], startpoint[1]])
        newpoint = [startpoint[0], startpoint[1]]
        newpoint[0] += 1

        while (newpoint[0] < midpoint[0]):
            path.append([newpoint[0], newpoint[1]])
            newpoint[0] += 1
        path.append([midpoint[0], midpoint[1]])
        newpoint2 = [midpoint[0], midpoint[1]]
        newpoint2[1] += 1
        
        while (newpoint2[1] < destpoint[1]):
            path.append([newpoint2[0], newpoint2[1]])
            newpoint2[1] += 1
        path.append([destpoint[0], destpoint[1]])

calc_path([1,1], [4,1], [4,3])
print(path)
