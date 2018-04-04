from dbfpy import dbf
import pdb, csv, os, re, datetime, time

def makecsv(ifile,ofile):
    """
    funcstion for converting a dbf file to csv
    takes an input dbf file and returns a csv file.
    The file is put in the csvfiles folder
    """

    db = dbf.Dbf(ifile,ignoreErrors=True)
    hdr = ''
    with open(ofile, 'w') as f:
        c = csv.writer(f)
        
        row = 0
        size = float(db.recordCount)
        # write the head to the CSV file
        c.writerow(db.fieldNames)

        # loop through all the records and write each line to the CSV file
        for rec in db:
            # using asList makes a list as opposed to asDict
            c.writerow(rec.asList())
            """
            percent = round(row/size*100,1)
            if percent < 100:
                #print percent,' percent complete         \r',
            """
            row = row + 1
        """
        #print  '100% percent complete         \r'
        #print ''
        """
        
def get_list(path):
    """
    function to get the list of paths.  returns a list that can be looped through.
    """
    with open(path, 'r') as f:
        path_list = f.readlines()
        path_list = [p.replace('\n','') for p in path_list]
        return path_list

def need_refresh(file_name, csv_file):
    """
    function to check if a file has been modified since last update.  
    returns True if the file has changed.
    """
    #check to see if the file has ever been created.  If it doesn't exist do the update.
    if os.path.exists(file_name) and os.path.exists(csv_file):
        dbf_date = str(datetime.datetime.strptime(time.ctime((os.path.getmtime(file_name))),'%a %b %d %H:%M:%S %Y'))
        csv_date = str(datetime.datetime.strptime(time.ctime((os.path.getmtime(csv_file))),'%a %b %d %H:%M:%S %Y'))
        #Check to see if the csv file is newer than the dbf file
        if csv_date > dbf_date:
            print('%s is already up to date' % csv_file)
            return False
        else:
            return True
    else:
        return True

#set env varibles to build paths from
#for Dovi /media/adam
#pdb.set_trace()
base_ipath = os.environ.get('ADAM_PATH')
base_opath = os.environ.get('ADAM_EXPORT_PATH')
base_adam_path = os.environ.get('BASE_SHARED_PATH')

#get the file list that should be converted to csv
list_file = base_adam_path + '/convert_list.txt'
list_of_paths = get_list(list_file)

for path in list_of_paths:
    
    #create the path for the dbf input file
    ifile = base_ipath + re.sub(r'\r','',path)
    #create the path for the csv output file
    oname = re.sub(r'\.dbf|\.DBF','',os.path.basename(ifile)) + '.csv'
    ofile = base_opath + oname
    #check to see if the line is a valid path and if the path needs refreshing
    if path.startswith('/') and need_refresh(ifile,ofile):
        #convert the dbf file to csv
        try:
            print('attempting to convert %s' % oname)
            
            makecsv(ifile,ofile)
        except Exception, e:
            print ('there was an initial problem with conversion')
            if e.filename.endswith('FPT'):
                print('found a name issue with the FPT file')
                file_name = re.sub(r'\.FPT','.fpt',e.filename)
                os.rename(file_name,e.filename)
                try:
                    print('retry conversion for %s' % oname)
                    makecsv(ifile,ofile)
                except Exception, e:
                    print('failed: %s' % e)            
            print (e)
            pass
    
