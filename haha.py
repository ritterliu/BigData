#!/usr/bin/python

import os
import shutil


alllist = (
"./2017-05-10/D6_2G_1_7.5.10dev/4f802dd0/csv/result.txt"
,"./2017-05-11/D6_2G_1_7.5.11dev/4f802dd0/csv/result.txt"
,"./2017-05-24/D6_2G_2_7.5.24dev/4f802ed3/csv/result.txt"
,"./2017-05-31/D6_2G_3_7.5.31dev/4f802ed3/csv/result.txt"
,"./2017-06-02/D6_2G_4_7.6.2dev/4f802ed3/csv/result.txt"
,"./2017-06-05/D6_2G_5_7.6.5dev/4f802ed3/csv/result.txt"
,"./2017-06-07/D6_2G_6_7.6.7dev/58169ad6/csv/result.txt"
,"./2017-06-12/D6_2G_7_7.6.12dev/58169ad6/csv/result.txt"
,"./2017-06-19/D6_2G_8_7.6.19dev/58169ad6/csv/result.txt"
,"./2017-06-21/D6_2G_9_7.6.21dev/58169ad6/csv/result.txt"
,"./2017-06-23/D6_2G_10_interpret-only/4f5acab8/csv/result.txt"
,"./2017-06-24/D6_2G_10_interpret-only/4f5acab8/csv/result.txt"
,"./2017-06-24/D6_2G_11_speed/58169ad6/csv/result.txt"
,"./2017-06-27/D6_2G_10_7.6.27dev/c5ad4f00/csv/result.txt"
,"./2017-06-28/D6_2G_14_7.6.26dev/c5ad4f00/csv/result.txt"
,"./2017-06-29/D6_2G_15_7.6.21dev/c5ad4f00/csv/result.txt"
,"./2017-07-03/D6_2G_16_7.7.3dev/c5ad4f00/csv/result.txt"
,"./2017-07-05/D6_2G_17_7.7.5dev/c5ad4f00/csv/result.txt"
,"./2017-07-10/D6_2G_18_7.7.10dev/c5ad4f00/csv/result.txt"
,"./2017-07-12/D6_2G_19_7.7.12dev/5a1a0d6/csv/result.txt"
,"./2017-07-13/D6_2G_19_7.7.12dev/5a1a0d6/csv/result.txt"
,"./2017-07-17/D6_2G_20_7.7.17dev/5a1a0d6/csv/result.txt"
,"./2017-07-19/D6_2G_21_7.7.19dev/5a1a0d6/csv/result.txt"
,"./2017-07-25/D6_2G_22_7.7.25dev/5a1a0d6/csv/result.txt"
,"./2017-07-26/D6_2G_23_7.7.26dev/5a1a0d6/csv/result.txt"
,"./2017-08-02/D6_2G_24_7.8.1dev/5a1a0d6/csv/result.txt"
,"./2017-08-04/D6_2G_25_7.8.4dev/5a1a0d6/csv/result.txt"
,"./2017-08-08/D6_2G_26_7.8.8dev/5a1a0d6/csv/result.txt"
,"./2017-08-09/D6_2G_27_7.8.9dev/5a1a0d6/csv/result.txt"
,"./2017-08-14/D6_2G_28_7.8.14dev/5a1a0d6/csv/result.txt"
,"./2017-08-15/D6_2G_28_7.8.15dev/5a1a0d6/csv/result.txt"
,"./2017-08-16/D6_2G_28_7.8.16dev/5a1a0d6/csv/result.txt"
,"./2017-08-29/D6_2G_32_7.8.29dev/5a1a0d6/csv/result.txt"
,"./2017-08-30/D6_2G_33_7.8.30dev/5a1a0d6/csv/result.txt"
,"./2017-09-06/D6_2G_35_7.9.6dev/5a1a0d6/csv/result.txt"
,"./2017-09-12/D6_2G_36_7.9.12dev/5a1a0d6/csv/result.txt"
,"./2017-10-10/D6_2G_40_7.10.10dev/5a1a0d6/csv/result.txt"
,"./2017-10-11/D6_2G_42_7.11.10dev/5a1a0d6/csv/result.txt"
,"./2017-10-24/D6_2G_10_7.10.24pre/5a1a0d6/csv/result.txt"
)


for i in alllist:
    fileName = i.split("/")[2]
    newname = "./folder/" + fileName + "_result.txt"
    print 'fileName:', fileName
    shutil.copyfile(i,newname)