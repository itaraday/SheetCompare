import pandas as pd
import numpy as np
import os.path
#import xlrd

def getworksheets(workbook):
    #xls = xlrd.open_workbook(workbook, on_demand=True)
    #worksheets = xls.sheet_names()
    worksheets = pd.ExcelFile(workbook)
    worksheets = worksheets.sheet_names
    return worksheets     

def getfiletype(filename):
    fileExtension = os.path.splitext(filename)[1]
    return fileExtension
    
def checkduplicatedID(df, ID, name):
    if (len(df.loc[df[ID].duplicated(), ID])):
        print "Duplciated IDs in {} : {} \n\n".format(name, df.loc[df[ID].duplicated(), ID])
        return True
    return False
    
  
class data:         
    def __init__(self):
        self.df = [pd.DataFrame(), pd.DataFrame()]
        
    def loaddata(self, dfnumber, filename, worksheet=None):
        fileExtension = getfiletype(filename)
        if fileExtension == '.csv':
            df = pd.read_csv(filename, dtype=unicode)
        elif (fileExtension == '.xlsx') and (worksheet != None):
            df = pd.read_excel(filename, sheetname=worksheet)
        else:
            print "error, not good file"
            return
        self.df[dfnumber] = df
        self.df[dfnumber] = self.df[dfnumber].rename(columns=lambda x: x.strip())
        print "DF {} loaded".format(dfnumber+1)
            
    def getcolumns(self, dfnumber):
        return sorted(self.df[dfnumber].columns.tolist())

 
    def betterrun(self, filename, ids, cols, commonID):
        old = self.df[0].dropna(how="all")
        new = self.df[1].dropna(how="all")  
        print "Running Compare"
        if ((len(old.loc[old[ids[0]].isnull(), ids[0] ]) > 0) or (len(new.loc[new[ids[1]].isnull(), ids[1] ]))) > 0:
            print "DF 1 blanks {}".format(len(old.loc[old[ids[0]].isnull(), ids[0] ]))
            print "DF 2 blanks {}".format(len(new.loc[new[ids[1]].isnull(), ids[1] ]))
            return
        if (checkduplicatedID(old, ids[0], "DF 1") or checkduplicatedID(new, ids[1], "DF 2")):
            print "Error, there are duplicated IDs"
            return
        
        #need to make columns the same for old and new
        old = old.rename(columns={ids[0]: commonID})
        new = new.rename(columns={ids[1]: commonID})        
        mycols = [commonID]
             
        for col in cols:          
            old = old.rename(columns={col.split('>')[0].strip():col.strip()})
            new = new.rename(columns={col.split('>')[1].strip():col.strip()})
            #old[col] = old[col].str.decode('iso-8859-1').str.encode('utf-8')
            #new[col] = new[col].str.decode('iso-8859-1').str.encode('utf-8')             
            mycols.append(col.strip())
        old = old[mycols]
        new = new[mycols]
        
        #combining datasets and marking duplicated accounts
        old["myversion"] = "old"
        new["myversion"] = "new"
        full_set = pd.concat([old,new],ignore_index=True)
        full_set["duplicate"] = False
        dupe_accts = full_set.set_index(commonID).index.get_duplicates()
        full_set.loc[full_set[commonID].isin(dupe_accts), 'duplicate'] = True
        
        #droping obvious rows that are the same
        changes = full_set.drop_duplicates(subset=mycols,take_last=True)    
        changed_accts = changes.set_index(commonID).index.get_duplicates()
        #Get all the duplicated ID's (will have changes)
        dupes = changes[changes[commonID].isin(changed_accts)]
        change_new = dupes[(dupes["myversion"] == "new")]
        change_old = dupes[(dupes["myversion"] == "old")]
        change_new = change_new[mycols]
        change_old = change_old[mycols]
        change_new = change_new.set_index(commonID)
        change_old = change_old.set_index(commonID)
        def report_diff(x): 
            if (str(x[0]).strip().lower() == str(x[1]).strip().lower() or (pd.isnull(x[0]) and pd.isnull(x[1]))):
                val = np.nan
            else:
                val = '{} | {}'.format(x[1], x[0])
            return val 

        my_panel = pd.Panel(dict(df1=change_new,df2=change_old))
        my_panel = my_panel.apply(report_diff, axis=0)
        #my_panel = None
        #finding new accounts
        added_accounts = changes[(changes["duplicate"] == False) & (changes["myversion"] == "old")]

        #finding removed accounts
        removed_accounts = changes[(changes["duplicate"] == False) & (changes["myversion"] == "new")]
 
        #cleanup and writing
        try:
            diffs = pd.DataFrame(my_panel)
        except:
            diffs = pd.DataFrame(columns=my_panel.minor_axis)
        #np.NaN seems to be returning a string
        diffs = diffs.replace('nan', np.nan)
        diffs = diffs.dropna(axis=1,how='all')
        diffs = diffs.dropna(axis=0,how='all')
        
        
        #writer = pd.ExcelWriter(filename, options={'encoding':'utf-8'})
        #diffs.to_excel(writer,"changed")
        #removed_accounts.to_excel(writer,"removed",index=False, columns=mycols)
        #added_accounts.to_excel(writer,"added",index=False, columns=mycols)
        filename = filename.split('.csv')[0]
        diffs.to_csv(filename + "_Change.csv")
        removed_accounts.to_csv(filename + "_Removed.csv", columns=mycols)
        added_accounts.to_csv(filename + "_Added.csv", columns=mycols)
        
        #writer.save() 
        print "Done"       
    
    def run(self, filename, ids, cols, commonID):       
        df1 = self.df[0]
        df2 = self.df[1]  
        print "Running Compare"
        if ((len(df1.loc[df1[ids[0]].isnull(), ids[0] ]) > 0) or (len(df2.loc[df2[ids[1]].isnull(), ids[1] ]))) > 0:
            print "DF 1 blanks {}".format(len(df1.loc[df1[ids[0]].isnull(), ids[0] ]))
            print "DF 2 blanks {}".format(len(df2.loc[df2[ids[1]].isnull(), ids[1] ]))
        df1 = df1[df1[ids[0]].notnull()]
        df2 = df2[df2[ids[1]].notnull()]
        #if (df1[ids[0]].dtype == )
        #df1[ids[0]] = df1[ids[0]].astype(str)
        #if (df2[ids[1]].dtype == "float64"):
        #    df2[ids[1]] = df2[ids[1]].astype(int) 
        #df2[ids[1]] = df2[ids[1]].astype(str) 
        
        if (checkduplicatedID(df1, ids[0], "DF 1") or checkduplicatedID(df2, ids[1], "DF 2")):
            print "Error, there are duplicated IDs"
            return
        #find missing IDs
        myids = df1[ids[0]].unique().tolist()
        myids2 = df2[ids[1]].unique().tolist()
        df2 = df2[df2[ids[1]].isin(myids)]
        missing = list(set(myids) - set(myids2))
        for missingid in missing:
            s = {ids[1]: missingid}
            df2 = df2.append(s, ignore_index=True)
        
        if len(missing) > 0:
            print "The following ID's are missing in DF2: {}".format(', '.join(map(str, missing)))
        df2 = df2.sort([ids[1]])
        df1 = df1.sort([ids[0]])
        
        #need to make columns the same for DF1 and DF2
        df1 = df1.rename(columns={ids[0]: commonID})
        df2 = df2.rename(columns={ids[1]: commonID})        
        mycols = [commonID]
             
        for col in cols:
            df1 = df1.rename(columns={col.split('>')[0].strip():col.strip()})
            df2 = df2.rename(columns={col.split('>')[1].strip():col.strip()})
            mycols.append(col.strip())
        df1 = df1[mycols]
        df2 = df2[mycols]

        
        
        #get ready to compare data
        df1.set_index(commonID, inplace=True)
        df2.set_index(commonID, inplace=True)
        #df1["Change"]= False
        #df2["Change"] = False
        #df1.loc[df1.index[np.any(df1 != df2,axis=1)],"Change"] = True
        #df2.loc[df1.index[np.any(df1 != df2,axis=1)],"Change"] = True
        self.compareDFs(filename, df1, df2)
        
        
    def compareDFs(self, filename, df1, df2):
        def report_diff(x): 
            if (str(x[0]).strip().lower() == str(x[1]).strip().lower() or (pd.isnull(x[0]) and pd.isnull(x[1]))):
                val = np.NAN
            else:
                val = '{} | {}'.format(*x)
            return val
            #return np.NaN if (x[0] == x[1] or (pd.isnull(x[0]) and pd.isnull(x[1]))) else '{} | {}'.format(*x)

        my_panel = pd.Panel(dict(df1=df1,df2=df2))
        my_panel = my_panel.apply(report_diff, axis=0)
        #np.NaN seems to be returning a string
        my_panel = my_panel.replace('nan', np.nan)
        my_panel=my_panel.dropna(axis=0,how='all')
        my_panel=my_panel.dropna(axis=1,how='all')
        my_panel.to_csv(filename)
        print "DONE!!"