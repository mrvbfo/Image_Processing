import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

iFolder = "C:/Users/Asus/Desktop/hw1_images" #input folder
oFolder = "C:/Users/Asus/Desktop/output" #output folder
os.makedirs(oFolder, exist_ok=True)

#filter files with .tif extension from input folder
images = [file for file in os.listdir(iFolder) if file.endswith('.tif')]

#1.RENK DAĞILIMI HİSTOGRAM ÇIKARMA
for file in images:
    imagePath = os.path.join(iFolder, file)
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    #Drawing Histogram
    plt.figure()
    plt.hist(image.ravel(), bins=256, range=(0, 255), color='gray')
    plt.title(f"Histogram {file}")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")

    #Save Histogram
    histogramPath = os.path.join(oFolder, f"{file}_histogram.png")
    plt.savefig(histogramPath)
    plt.close()

#2. BİNARİZATİON

#The threshold values according to the pixel densities of the histograms
tresholdValues = {
    "Fig0107(a)(chest-wray-vandy).tif": 200,
    "Fig0120(a)(ultrasound-fetus1).tif": 40,
    "Fig0304(a)(breast_digital_Xray).tif": 80,
    "Fig0359(a)(headCT_Vandy).tif": 160
}

for file in images:
    imagePath = os.path.join(iFolder, file)

    # reads the image in greyscale
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    # threshold of images, get the treshold value or use defualt value 128
    treshold = tresholdValues.get(file, 128)

    _, binaryImg = cv2.threshold(image, treshold, 255, cv2.THRESH_BINARY)

    binaryPath = os.path.join(oFolder, f"{file}_binarizedimage.png")
    cv2.imwrite(binaryPath, binaryImg)

#3. Resmi ikiden fazla bölgeye ayırma

#The threshold values according to the pixel densities of the histograms
multi_threshold_values = {
    "Fig0107(a)(chest-wray-vandy).tif": [50, 100, 200],
    "Fig0120(a)(ultrasound-fetus1).tif": [20, 40, 80],
    "Fig0304(a)(breast_digital_Xray).tif": [30, 80, 100],
    "Fig0359(a)(headCT_Vandy).tif": [100, 120, 180]
}

for img in images:
    imagePath = os.path.join(iFolder, img)
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    #The threshold values of the images are taken and the default value is used to avoid errors.
    thresholds = multi_threshold_values.get(img, [50, 100, 150])

    #An empty matrix is created for the segmentation
    segmented_image = np.zeros_like(image) #same size as input image

    for i, t in enumerate(thresholds):
        if i == 0:
            segmented_image[image <= t] = (i + 1) * 50
        else:
            segmented_image[(image > thresholds[i -1]) & (image <= t)] = (i+1) * 50

    segmented_image[image > thresholds[-1]] = (len(thresholds) + 1) * 50

    segmentedPath = os.path.join(oFolder, f"{img}_multi_segmented.png")
    cv2.imwrite(segmentedPath, segmented_image)

# 4. Morfolojik Operatörler Uygulama

#A 3x3 kernel matrix with elements of 1
kernel = np.ones((3,3), np.uint8)

for file in images:
    imagePath = os.path.join(iFolder, file)
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    # The threshold values of the images are taken, the default is 128 to avoid errors.
    treshold = tresholdValues.get(file, 128)

    #binarization
    _, binaryImg = cv2.threshold(image, treshold, 255, cv2.THRESH_BINARY)

    #reduces the size of white pixels and reduces the image borders.
    erosionProcess = cv2.erode(binaryImg, kernel, iterations=1)
    erosionPath = os.path.join(oFolder, f"{file}_erosion.png")
    cv2.imwrite(erosionPath, erosionProcess)

    #increases the size of the white regions and enlarges the image classes.
    dilationProcess = cv2.dilate(binaryImg, kernel, iterations=1)
    dilationPath = os.path.join(oFolder, f"{file}_dilation.png")
    cv2.imwrite(dilationPath, dilationProcess)

    #apply first erosion and then dilation.
    openingProcess = cv2.morphologyEx(binaryImg, cv2.MORPH_OPEN,kernel)
    openingPath = os.path.join(oFolder, f"{file}_opening.png")
    cv2.imwrite(openingPath, openingProcess)

    #To fill the gaps, first expansion dilation and then erosion are applied.
    closingProcess = cv2.morphologyEx(binaryImg, cv2.MORPH_CLOSE, kernel)
    closingPath = os.path.join(oFolder, f"{file}_closing.png")
    cv2.imwrite(closingPath, closingProcess)

#5. Bölge genişletme tekniği ile nesne bulma (Region Growing)
def region_growing(image, seed_point, threshold=5):
    rows, cols = image.shape
    segmented = np.zeros_like(image)
    region_color = 255 #white color is used
    seed_value = image[seed_point]

    stack = [seed_point] #to keep the pixels
    while stack:
        x, y = stack.pop() #to take a pixel from the stack
        if segmented[x,y] == 0 and abs(int(image[x,y]) - int(seed_value)) < threshold:
            segmented[x,y] = region_color
            # 4 neighborhood
            if x > 0: stack.append((x-1, y)) #top
            if x < rows - 1: stack.append((x+1, y)) #bottom
            if y > 0: stack.append((x, y-1)) #left
            if y < cols - 1: stack.append((x, y+1)) #right
    return segmented

for file in images:
    segmentedPath = os.path.join(oFolder, f"{file}_multi_segmented.png")
    segmented_image = cv2.imread(segmentedPath, cv2.IMREAD_GRAYSCALE)

    seed_points = [(50,50), (100,100), (150,150)]
    threshold = 10 #difference in pixel values

    region_growing_result = np.zeros_like(segmented_image) #empty image for result
    color_step = 50 # increase value for color
    current_color = 50 #first color


    for seed in seed_points:
        if region_growing_result[seed[0], seed[1]] == 0:
            region_segment = region_growing(segmented_image, seed, threshold)  #region growing
            region_growing_result[region_segment == 255] = current_color
            #Provides color enhancement in different areas
            current_color += color_step

    region_growing_path = os.path.join(oFolder, f"{file}_region_growing.png") #save region growing
    cv2.imwrite(region_growing_path, region_growing_result)

#6. Histogram Eşikleme
for file in images:
    imagePath = os.path.join(iFolder, file)
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    #histogram equalization and contrast increase
    equalized_image = cv2.equalizeHist(image)

    #6.1 Histogram Çıkartma
    #draw equalizated histogram
    plt.figure()
    plt.hist(equalized_image.ravel(), bins=256, range=(0, 255), color='gray')
    plt.title(f"Equalized Histogram {file}")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")

    #save histogram
    histogramPath = os.path.join(oFolder, f"{file}_histogram_eq.png")
    plt.savefig(histogramPath)
    plt.close()

    #6.2 Binarization
    #thresholds I determined according to the new histogram distribution
    tresholdValuesEq = {
        "Fig0107(a)(chest-wray-vandy).tif": 190,
        "Fig0120(a)(ultrasound-fetus1).tif": 100,
        "Fig0304(a)(breast_digital_Xray).tif": 150,
        "Fig0359(a)(headCT_Vandy).tif": 110
    }

    # threshold values of the images are taken, otherwise the default value 128 is used to avoid errors.
    treshold = tresholdValuesEq.get(file, 128)

    # binarization
    # turns pixel values above the threshold to white, and those below to black
    _, equalizedbinaryImg = cv2.threshold(equalized_image, treshold, 255, cv2.THRESH_BINARY)

    equalized_binaryPath = os.path.join(oFolder, f"{file}_equalized_binarized.png")
    cv2.imwrite(equalized_binaryPath, equalizedbinaryImg)



#6.3. Resmi İkiden Fazla Bölgeye Ayırma (Histogram Equalization Sonrası)
#3 threshold values that I chose by eye for new images
multi_threshold_values_eq = {
    "Fig0107(a)(chest-wray-vandy).tif": [80, 150, 200],
    "Fig0120(a)(ultrasound-fetus1).tif": [40, 70, 120],
    "Fig0304(a)(breast_digital_Xray).tif": [90, 210, 250],
    "Fig0359(a)(headCT_Vandy).tif": [100, 130, 170]
}

for file in images:
    imagePath = os.path.join(iFolder, file)
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    equalized_image = cv2.equalizeHist(image)

    #The threshold values of the images are taken and the default value is used to avoid errors.
    thresholds = multi_threshold_values_eq.get(file, [50, 100, 150])

    #An empty matrix is created for the  segmantation operation.
    segmented_image = np.zeros_like(equalized_image) #in whole size with the input image

    #divides the image into different regions depending on the threshold values
    #pixels less than or equal to the first threshold to the first region
    #pixels between middle thresholds to other regions
    for i, t in enumerate(thresholds):
        if i == 0:
            segmented_image[equalized_image <= t] = (i + 1) * 85
        else:
            segmented_image[(equalized_image > thresholds[i -1]) & (equalized_image <= t)] = (i+1) * 85

    segmented_image[equalized_image > thresholds[-1]] = min((len(thresholds) + 1) * 85, 255)

    segmentedPath = os.path.join(oFolder, f"{file}_multi_segmented_eq.png")
    cv2.imwrite(segmentedPath, segmented_image)



#6.4. Morfolojik Operatörler
for file in images:
    imagePath = os.path.join(iFolder, file)
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    # histogram equalization and contrast increase
    equalized_image = cv2.equalizeHist(image)

    # A 3x3 kernel matrix with elements of 1
    kernel = np.ones((3, 3), np.uint8)

    # The threshold values of the images are taken, the default is 128 to avoid errors.
    treshold = tresholdValuesEq.get(file, 128)

    #image binarization
    _, binaryImg = cv2.threshold(equalized_image, treshold, 255, cv2.THRESH_BINARY)

    #reduces the size of white pixels and reduces the image borders.
    erosionProcess = cv2.erode(binaryImg, kernel, iterations=1)
    erosionPath = os.path.join(oFolder, f"{file}_erosion_eq.png")
    cv2.imwrite(erosionPath, erosionProcess)

    #increases the size of the white regions and enlarges the image classes.
    dilationProcess = cv2.dilate(binaryImg, kernel, iterations=1)
    dilationPath = os.path.join(oFolder, f"{file}_dilation_eq.png")
    cv2.imwrite(dilationPath, dilationProcess)

    #apply first erosion and then dilation.
    openingProcess = cv2.morphologyEx(binaryImg, cv2.MORPH_OPEN,kernel)
    openingPath = os.path.join(oFolder, f"{file}_opening_eq.png")
    cv2.imwrite(openingPath, openingProcess)

    #To fill the gaps, first expansion dilation and then erosion are applied.
    closingProcess = cv2.morphologyEx(binaryImg, cv2.MORPH_CLOSE, kernel)
    closingPath = os.path.join(oFolder, f"{file}_closing_eq.png")
    cv2.imwrite(closingPath, closingProcess)

#6.5. Bölge genişletme tekniği ile nesne bulma (Region Growing)

for file in images:
    segmentedPath = os.path.join(oFolder, f"{file}_multi_segmented_eq.png")
    segmented_image = cv2.imread(segmentedPath, cv2.IMREAD_GRAYSCALE)

    # histogram eşikleme ile kontrast attırılır
    equalized_image = cv2.equalizeHist(segmented_image)

    seed_points = [(50,50), (100,100), (150,150)] #starting point
    threshold = 40 #I reached this value by trying the difference in pixel values

    region_growing_result = np.zeros_like(equalized_image)

    color_step = 50 # color increment value
    current_color = 50 # first color

    for seed in seed_points:
        if region_growing_result[seed[0], seed[1]] == 0:
            region_segment = region_growing(equalized_image, seed, threshold)  #region growing
            region_growing_result[region_segment == 255] = current_color
            #provides regional color increase
            current_color += color_step

    region_growing_path = os.path.join(oFolder, f"{file}_region_growing_eq.png") #for saving region growing output
    cv2.imwrite(region_growing_path, region_growing_result)
