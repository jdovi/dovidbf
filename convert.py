from dbfpy import dbf
import pdb
import csv
import os

def makecsv(ifile,ofile):
    db = dbf.Dbf(ifile)
    hdr = ''
    with open(ofile, 'w') as f:
        c = csv.writer(f)

        # write the head to the CSV file
        c.writerow(db.fieldNames)

        # loop through all the records and write each line to the CSV file
        for rec in db:
            # using asList makes a list as opposed to asDict
            c.writerow(rec.asList())

ifile = '/media/adam/adamcache/Accar/Data/Journals.106'
oname = '.csv'.join(os.path.basename(ifile))
opath = '/media/adam/csvfiles'
ofile = opath + oname

makecsv(ifile,ofile)
