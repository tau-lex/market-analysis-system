###############################################################################
#                                                                             #
#   Market Analysis System                                                    #
#   https://www.mql5.com/ru/users/terentjew23                                 #
#                                                                             #
#   M A R K E T   A N A L Y S I S   S C R I P T   W I T H   K E R A S         #
#                                                                             #
#   Aleksey Terentew                                                          #
#   terentew.aleksey@ya.ru                                                    #
#                                                                             #
###############################################################################

#load files
#prepare dataset

#dev


#import csv
#
#input_file = open("pr.csv", "rb")
#rdr = csv.reader(input_file)
#
#output_file = open("pr1.csv", "wb")
#wrtr = csv.writer(output_file)
#
#for rec in rdr:
#    try:
#        rec[1] = int(rec[1]) + 1
#    except:
#        pass
#    wrtr.writerow(rec)
#
#input_file.close()
#output_file.close()
#
##################
#
#input_file = open("pr.csv", "rb")
#rdr = csv.DictReader(input_file, fieldnames=['name', 'number', 'text'])
#
#output_file = open("pr1.csv", "wb")
#wrtr = csv.DictWriter(output_file, fieldnames=['name', 'number', 'text'])
#
#for rec in rdr:
#    try:
#        rec['number'] = int(rec['number']) + 1
#    except:
#        pass
#    wrtr.writerow(rec)
#    
#input_file.close()
#output_file.close()
#
#################
#
#from pandas import read_csv
#
#out = read_csv(input_file, sep=';', skiprows=[0], header=None)
#
## Обращаться к полученным данным через индексацию:
#    
#item_str = out[5][5]


