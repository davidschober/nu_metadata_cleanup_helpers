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

def filter_by_list(source, filter_list):
    """grab things that are in the filter list via set list"""
    return [item for item in source if set(item)&set(filter_list)]

def filter_by_not_in_list(source, filter_list):
    """grab things that aren't in the list via set """
    return [item for item in source if not set(item)&set(filter_list)]

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

def filter_all_collections(all_images, headers, inputdir, outputdir):
    """ This takes a set of images data and filters out all public collections 
    the inputs are a list of all images, a list of public collections text files which contain pids
    and a list of headers

    all_images = list of lists
    headers = list 
    list_of_public_collections

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


    
