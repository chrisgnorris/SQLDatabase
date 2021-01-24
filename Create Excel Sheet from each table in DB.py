#Fron stack overflow, un tested https://stackoverflow.com/questions/36028759/how-to-open-and-convert-sqlite-database-to-pandas-dataframe
import os, fnmatch
import sqlite3
import pandas as pd

#creates a directory without throwing an error
def create_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
    print("Created Directory : ", dir)
  else:
    print("Directory already existed : ", dir)
  return dir

#finds files in a directory corresponding to a regex query
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result



#convert sqlite databases(.db,.sqlite) to pandas dataframe(excel with each table as a different sheet or individual csv sheets)
def save_db(dbpath=None,excel_path=None,csv_path=None,extension="*.sqlite",csvs=True,excels=True):
    if (excels==False and csvs==False):
      print("Atleast one of the parameters need to be true: csvs or excels")
      return -1

    #little code to find files by extension
    if dbpath==None:
      files=find(extension,os.getcwd())
      if len(files)>1:
        print("Multiple files found! Selecting the first one found!")
        print("To locate your file, set dbpath=<yourpath>")
      dbpath = find(extension,os.getcwd())[0] if dbpath==None else dbpath
      print("Reading database file from location :",dbpath)

    #path handling

    external_folder,base_name=os.path.split(os.path.abspath(dbpath))
    file_name=os.path.splitext(base_name)[0] #firstname without .
    exten=os.path.splitext(base_name)[-1]   #.file_extension

    internal_folder="Saved_Dataframes_"+file_name
    main_path=os.path.join(external_folder,internal_folder)
    create_dir(main_path)


    excel_path=os.path.join(main_path,"Excel_Multiple_Sheets.xlsx") if excel_path==None else excel_path
    csv_path=main_path if csv_path==None else csv_path

    db = sqlite3.connect(dbpath)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(len(tables),"Tables found :")

    if excels==True:
      #for writing to excel(xlsx) we will be needing this!
      try:
        import XlsxWriter
      except ModuleNotFoundError:
        print('!pip install XlsxWriter')

    if (excels==True and csvs==True):
      writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
      i=0
      for table_name in tables:
          table_name = table_name[0]
          table = pd.read_sql_query("SELECT * from %s" % table_name, db)
          i+=1
          print("Parsing Excel Sheet ",i," : ",table_name)
          table.to_excel(writer, sheet_name=table_name, index=False)
          print("Parsing CSV File ",i," : ",table_name)
          table.to_csv(os.path.join(csv_path,table_name + '.csv'), index_label='index')

      writer.save()


    elif excels==True:
      writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
      i=0
      for table_name in tables:
          table_name = table_name[0]
          table = pd.read_sql_query("SELECT * from %s" % table_name, db)
          i+=1
          print("Parsing Excel Sheet ",i," : ",table_name)
          table.to_excel(writer, sheet_name=table_name, index=False)

      writer.save()

    elif csvs==True:
      i=0
      for table_name in tables:
          table_name = table_name[0]
          table = pd.read_sql_query("SELECT * from %s" % table_name, db)
          i+=1
          print("Parsing CSV File ",i," : ",table_name)
          table.to_csv(os.path.join(csv_path,table_name + '.csv'), index_label='index')
    cursor.close()
    db.close()
    return 0
save_db();