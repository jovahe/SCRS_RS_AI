#coding:utf-8
import os,sys,fire
from ulitities.base_functions import get_file,find_file
from tqdm import tqdm
try:
    from osgeo import ogr, osr, gdal
    gdal.UseExceptions()
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')
def band_combine(file_list,outputfile):
    result = []
    dataset_a = gdal.Open(file_list[0])
    dataset_b = gdal.Open(file_list[1])
    band_n_a = dataset_a.RasterCount
    band_n_b = dataset_b.RasterCount
    band_n = band_n_a + band_n_b

    result.append(dataset_a.ReadAsArray())
    result.append(dataset_b.ReadAsArray())

    X = dataset_a.RasterXSize
    Y = dataset_a.RasterYSize

    driver = gdal.GetDriverByName('GTiff')

    outdataset = driver.Create(outputfile, X,
                              Y, band_n, gdal.GDT_Byte)
    count = 0
    cc = result[0]
    bb=cc[1]
    for i in range(band_n_a):
        count = count + 1
        outdataset.GetRasterBand(count + 1).WriteArray(result[0][i])
    for j in range(band_n_b):
        outdataset.GetRasterBand(count + 1).WriteArray(result[1])
        count = count + 1
    outdataset.FlushCache()
    # del outdataset


def batch_band_combine(indir,outdir,nodata=65535):
    if not os.path.isdir(indir):
        print("Error:input is not a directory")
        return -1

    if not os.path.isdir(indir+'/a/') or not os.path.isdir(indir+'/b'):
        print("Error: please check dir img and index")
        return -2

    filelist_a, nb = get_file(indir+'/a/')
    if nb ==0:
        print("Error: there is no file in dir a")
        return -3
    if not os.path.isdir(outdir):
        print("Warning: outdir is not exist, it will be created")
        os.mkdir(outdir)
    for fileA in tqdm(filelist_a):
        basename=os.path.basename(fileA).split(".")[0]
        fileB = find_file(indir+'/b/',basename)
        print(fileB)
        flist=[]
        flist.append(fileA)
        flist.append(fileB)
        outfile = outdir+'/'+basename+'.tif'
        ret =0
        ret = band_combine(flist,outfile)
        if ret!=0:
            print("Error:combinig failed :{}".format(basename))
            continue

    return 0

# batch_band_combine(r"C:\Users\scrs\Desktop\8bit",r"C:\Users\scrs\Desktop\8",255)

# indir = "D:\\water\\src\\8bitOrigin"
# # list = os.listdir(indir)
# # for file in list:
# #     basename = os.path.basename(file).split(".")[0]
# #     try:
# #         print(file)
# #         infile_1= "D:\\water\\src\\8bitOrigin\\" +file
# #         infile_2 =  "D:\\water\\src\\8bitIndex\\" +basename + "_ndwi.tif"
# #         filelist = [infile_1,infile_2]
# #         band_list = [[0,1,2,3],[0]]
# #         band_combine(filelist,[[0,1,2,3],[0]])
# #
# #     except:
# #         print("filed  : "+file)
# variable_str='3_13'
#
# input_files =['/home/omnisky/PycharmProjects/data/samples/isprs/4_Ortho_RGBIR/top_potsdam_{}_RGBIR.tif'.format(variable_str),
#               '/home/omnisky/PycharmProjects/data/samples/isprs/1_DSM_normalisation/1_DSM_normalisation/dsm_potsdam_0{}_normalized_lastools.jpg'.format(variable_str)]
# output_file = '/home/omnisky/PycharmProjects/data/samples/isprs/train/src/top_potsdam_{}.tif'.format(variable_str)

if __name__=="__main__":
    fire.Fire()
    print("")
