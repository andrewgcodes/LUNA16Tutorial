import SimpleITK as sitk
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt

def load_itk_image(filename):
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
    numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
    return numpyImage, numpyOrigin, numpySpacing

def readCSV(filename):
    lines = []
    with open(filename, "r") as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            lines.append(line)
    return lines
#what is going onnnn
def worldToVoxelCoord(worldCoord, origin, spacing):
    stretchedVoxelCoord = np.absolute(worldCoord - origin)
    voxelCoord = stretchedVoxelCoord / spacing
    return voxelCoord


def normalizePlanes(npzarray):
    maxHU = 400.
    minHU = -1000.

    npzarray = (npzarray - minHU) / (maxHU - minHU)
    npzarray[npzarray > 1] = 1.
    npzarray[npzarray < 0] = 0.
    return npzarray

img_path  = '/Users/andrewgao/Downloads/TUTORIAL/data/1.3.6.1.4.1.14519.5.2.1.6279.6001.148447286464082095534651426689.mhd'
cand_path = '/Users/andrewgao/Downloads/TUTORIAL/data/candidates.csv'

numpyImage, numpyOrigin, numpySpacing = load_itk_image(img_path)
print (numpyImage.shape)
print (numpyOrigin)
print (numpySpacing)

cands = readCSV(cand_path)
print(cands)
# get candidates
for cand in cands[1:]:
    worldCoord = np.asarray([float(cand[3]),float(cand[2]),float(cand[1])])
    voxelCoord = worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
    voxelWidth = 65

for cand in cands[1:]:
    worldCoord = np.asarray([float(cand[3]), float(cand[2]), float(cand[1])])
    voxelCoord = worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
    voxelWidth = 65
    patch = numpyImage[int(voxelCoord[0]), int(voxelCoord[1]) - int(voxelWidth / 2):int(voxelCoord[1]) + int(voxelWidth / 2),
            int(voxelCoord[2]) - int(voxelWidth / 2):int(voxelCoord[2]) + int(voxelWidth / 2)]
    patch = normalizePlanes(patch)
    print ('data')
    print  (worldCoord)
    print (voxelCoord)
    print (patch)
    outputDir = '/Users/andrewgao/Downloads/TUTORIAL/patches/'
    plt.imshow(patch, cmap='gray')
    plt.show()
    Image.fromarray(patch * 255).convert('L').save(os.path.join(outputDir, 'patch_' + str(worldCoord[0]) + '_' + str(
        worldCoord[1]) + '_' + str(worldCoord[2]) + '.tiff'))
