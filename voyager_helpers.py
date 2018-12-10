import unicodecsv

def get_csv(source_csv):
    """grabs a csv and returns a list just a shortcut"""
    return [row for row in unicodecsv.reader(open(source_csv, 'r'))]

def get_text_file(source_text):
    return open(source_text).read().splitlines() 

def get_list_from_regex(regex, items):
    """ Returns a list of matches or NONE based on regex example: get_list_from_regex("Voyager:\w+", all_images_list"""
    import re
    r = re.compile(regex)
    return [m.group() if m else None for item in items for m in [r.search(str(item))]]

def save_csv(headers, rows, outputfile):
    """a convience wrapper for saving). takes a header row and a list of data rows"""
    with open (outputfile, 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

def get_all_files(directory):
    """Get a list of all the files to filter from"""
    from os import listdir
    from os.path import join, isfile

    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]

def filter_by_list(source, filter_list):
    """grab things that are in the filter list via set list"""
    return [item for item in source if set(item)&set(filter_list)]

def filter_by_not_in_list(source, filter_list):
    """grab things that aren't in the list via set """
    return [item for item in source if not set(item)&set(filter_list)]

def filter_all_collections(all_images, headers, inputdir, outputdir):
    """ This takes a set of images data and filters out all public collections 
    the inputs are a list of all images, a list of public collections text files which contain pids
    and a list of headers

    all_images = list of lists
    headers = list 
    list_of_public_collections
    DEPRECATED::: USE pd_filter_all_collections

    """ 
    from os.path import join, basename
    list_of_public_collections = get_all_files(inputdir)
    # copy the list 
    filtered_images = [item for item in all_images]
    for c in list_of_public_collections:
        filtered_ids = get_text_file(c)
        items = filter_by_list(filtered_images, filtered_ids)
        filtered_images = filter_by_not_in_list(filtered_images, filtered_ids)
        save_csv(headers, items, join(outputdir, basename(c)+"filtered.csv"))
    save_csv(headers, filtered_images, join(outputdir, 'not_in_lists.csv'))

def pd_filter_all_collections(data_frame, column, inputdir, outputdir):
    """ use  pandas to filter out all collections"""
    from os.path import join, basename

    list_of_public_collections = get_all_files(inputdir)
    df = data_frame
    for c in list_of_public_collections:
        filtered_ids = get_text_file(c)
        items_df = df[df[column].isin(filtered_ids)]

        df = df[~df[column].isin(filtered_ids)]
        items_df = items_df.dropna(axis='columns', how='all')
        items_df.sort_index(axis = 1, inplace = True)
        items_df.to_csv(join(outputdir, basename(c)+'filtered.csv'), encoding= "utf-8")
    df = df.dropna(axis='columns', how='all')
    df.sort_index(axis = 1, inplace = true)
    df.to_csv(join(outputdir, 'not_in_lists.csv'), encoding = "utf-8")

def remove_empty_columns(inputdir, outputdir):
    """takes an input directory of csv, uses the first row as headers, iterates through it and aggressively
    looks for empty columns (no data all they way down). It then removes each cell and header. 
    The output is saved to the output directory. If you put the same directory in 
    input and output the changes will be destructive. 
    >>> for i, v in enumerate(test[0]):
            if not [x[i] for x in test[1:] if x[i]]:
                [x.pop(i) for x in test]
    
    THIS DOESN'T work consistently. I went with PANDAs as it's a more straightforward approach. 
    """
    from os.path import join, basename
    
    # get all the files
    csv_paths = get_all_files(inputdir)
    for path in csv_paths:
        csv = get_csv(path)
        #enumerate the first row assume it's headers
        for i,v in enumerate(csv[0]):
            # iterate through and build a list. If the list is empty, pop the cells
            if not [row[i] for row in csv[1:] if row[i]]:
                # if it's empty pop them all including the header row
                removed = [row.pop(i) for row in csv]
                print removed
        # save out the csv to the output directory
        print len(csv[0])
        print csv[1]
        save_csv(csv[0], csv[1:], join(outputdir, basename(path)))



def pd_remove_empty_columns(inputdir, outputdir):
    """ Use Pandas to drop the na column"""

    from pandas.io.parsers import read_csv
    from os.path import join, basename
    
    csv_paths = get_all_files(inputdir)
    for path in csv_paths:
        data = read_csv(path, encoding='utf-8')
        filtered_data = data.dropna(axis='columns', how='all')
        filtered_data.to_csv(join(outputdir, basename(path)), encoding='utf-8')

def get_unique_values_from_column(inputdir, output_file, regex_filter):
    """Gets the row index for a regex, then collects
    all the data from the row.
    get the data in to pandas 
    WIP to work on this more Monday. 
    Below was my brainstorm/notes while working out the method.  
    >>> df = pandas.read_csv('/Users/dsc712/Desktop/output_remove_empty/postcards.txtfiltered.csv')
    >>> filtered = df.filter(regex='subject\[.*\]$').values
    >>> subjects = df.filter(regex="subject\[.*\]$").values.flatten() # flattened subjects from a spreadsheet using regex 
    >>> subjects = [item for item in subject if str(item) != 'nan']
    >>> unique_subjects = list(set(subjects)) 
    
    """ 

    import pandas
    
    csv_paths = get_all_files(inputdir)
    #empty set of values
    values = []
    for path in csv_paths:
        print path
        df = pandas.read_csv(path)
        # Filter out and flatten anythign that matches a column header from regex
        filtered = df.filter(regex=regex_filter).values.flatten()
        # filter out the nan values, kind of a pain, but I couldn't drop them in panda without
        # dropping whole rows. 
        values = values+[item for item in filtered if str(item) != 'nan']#list(filtered)
    values = list(set(values)) 
    with open(output_file, 'wb') as f:
        f.write("\n".join(values))

    return list(set(values)) # list(set(values))

