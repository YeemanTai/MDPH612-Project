import pydicom as dicom
import os
import matplotlib.pyplot as plt


# make it True if you want in PNG format
PNG = False
# Specify the .dcm folder path
folder_path = r"C:\Users\USER\MDPH612 Project\images\DICOM"
# Specify the output jpg/png folder path
jpg_folder_path = r"C:\Users\USER\MDPH612 Project\images\JPG"
images_path = os.listdir(folder_path)

for n, image in enumerate(images_path):
    ds = dicom.dcmread(os.path.join(folder_path, image))
    pixel_array_numpy = ds.pixel_array
    image = image.replace('.dcm', '.jpg')
    plt.style.use('grayscale')
    #plt.imshow(pixel_array_numpy)
    #plt.show()
    #print(pixel_array_numpy)
    #print(pixel_array_numpy.size)
    plt.imsave(os.path.join(jpg_folder_path, image),pixel_array_numpy, format='jpg')
