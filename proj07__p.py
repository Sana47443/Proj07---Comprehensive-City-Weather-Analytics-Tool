#########################################################################################################################################################
#  Computer Project #7
#
#  Algorithm
#    import all the necessary modules such as csv, datetime and itemgetter from operator
#    writing function definition for open_files() which returns city_list and list of file pointers
#    writing function definition read_files() which takes in one parameter and returns list of list of tuples
#    writing function definition get_data_in_range() which has 3 parameters and returns filtered data according to the given start and end dates
#    writing function definition get_min() which takes in 3 parameters and returns a list of tuples having cities and min vals in that col
#    writing function definition get_max() which takes in 3 parameters and returns a list of tuples having cities and max vals in that col
#    writing function definition get_average() which takes in 3 parameters and returns a list of tuples having cities and average vals in that col
#    writing function definition to_check_tol() which takes 2 numbers and checks whether they satify the tolerance value or not
#    writing function definition actual_fun() which takes in a list and returns the mode and it's frequency
#    writing function definition get_modes() which has 3 parametrs and returns cities with their modes and their frequency
#    writing function definition high_low_averages() which takes in 3 parameters and returns cities with average values (overall) according to categories
#    writing function defintion display_statistics() which has 3 parameters and prints the summary staistics in a formtted way
#    writing function defintion main() which calls all the above functions according to the user's needs
#
#########################################################################################################################################################

import csv                          #importing csv module
from datetime import datetime       #importing datetime from datetime
from operator import itemgetter     #importing itemgetter from operator module
        
def open_files():
    '''
    Prompts for a sequence of cities(comma seperated) and returns the file 
    pointers of theose cities' csv files and displays an error if a file
    corresponding to the city does not exist.
    
    Parameters
    ----------
    None

    Returns
    -------
    list_of_cities : List
                     It is the list of cities having a valid csv file
                     
    list_of_fp : File Pointers
                 It is the list of file pointers corresponding to the cities'
                 csv files

    '''
    string_of_cities = input("Enter cities names: ")   #inputting string of cities
    list_of_cities = string_of_cities.split(",")     #strings to list
    list_of_cities_to_remove=[]    #initializing various lists
    list_of_fp=[]
    for name in list_of_cities:     #going through the list made before(cities)
        f_name = name+".csv"
        #print(f_name)
        try:                       #try except for FileNotFoundError
            fp_city=open(f_name ,"r")
            list_of_fp.append(fp_city)  #append the file pointer if exists
        except FileNotFoundError:
            print("\nError: File {} is not found".format(f_name))
            list_of_cities_to_remove.append(name) #to remove if not
    for name2 in list_of_cities_to_remove:
        list_of_cities.remove(name2)   #remove those who don't exist
    
    return list_of_cities, list_of_fp

def read_files(cities_fp):
    '''
    From the given list of file pointers, this function opens each file, goes 
    through it line by line, change to the corresponding datatype, stores it 
    in a tuple which are eventually stored in a list for that file and which
    are eventually append to the final list

    Parameters
    ----------
    cities_fp : List
                List of file pointers of the files

    Returns
    -------
    main_list : List
                List of list of tuples which have the files' data
    '''
    main_list=[]      #the main list which is the outer list
    for file_obj  in cities_fp:    #going through the list of file pointers
        new_list=[]
        reader = csv.reader(file_obj)  #assigning reader object
        file_obj.readline()            #skipping the 2 header lines
        file_obj.readline()
        for data in reader:      #using try except for all the below just for ValueError
            date_val = data[0]
            try:
                t_average = float(data[1])
            except ValueError:
                t_average = None
            try:
                t_max_val = float(data[2])
            except ValueError:
                t_max_val = None
            try:
                t_min_val = float(data[3])
            except ValueError:
                t_min_val = None
            try:
                precip_val = float(data[4])
            except ValueError:
                precip_val = None
            try:
                snow_val = float(data[5])
            except ValueError:
                snow_val = None
            try:
                snwd_val = float(data[6])
            except ValueError:
                snwd_val = None
            weather_vals = (date_val,t_average,t_max_val,t_min_val,\
precip_val,snow_val,snwd_val)    #Forming a tuple
            new_list+=[weather_vals]
        main_list+=[new_list]  #appending
    return main_list

def get_data_in_range(data, start_date, end_date):
    '''
    With the given data(list of list of tuples) and the start and end date, 
    this function extracts the data which lie between the dates(both inclusive)

    Parameters
    ----------
    data : List 
           List of list of tuples
           
    start_date : String
                 Given in mm/dd/yyyy format
                 
    end_date : String
               Given in mm/dd/yyyy format

    Returns
    -------
    range_data_list : List
                      List of list of tuples(filtered)

    '''
    range_data_list = []
    st_date = start_date.split("/")
    st_date_val = datetime(int(st_date[2]), int(st_date[0]), \
                        int(st_date[1])).date()  #making into date
    end_dat = end_date.split("/")
    end_date_val = datetime(int(end_dat[2]), int(end_dat[0]), \
                            int(end_dat[1])).date()  #making into date
    for file_by_file in data:    #extracting the data between the dates using for loop
        filtered_data = []
        for vals in file_by_file:
            date_str= vals[0]
            date_list = date_str.split("/")
            date_vals = datetime(int(date_list[2]), int(date_list[0]),\
                                 int(date_list[1])).date()
            if date_vals>=st_date_val and date_vals<=end_date_val:
                filtered_data+=[vals]
        range_data_list+=[filtered_data]   #appending to be the filtered one
        
    return range_data_list
        

def get_min(col, data, cities):
    '''
    With the data, cities and column given, it goes through the list of list
    of tuples and fetches the min value in the particular column/category
    for each city

    Parameters
    ----------
    col : Integer
          Index value corresponding to the category in COLUMNS list
          
    data : List
           List of list of tuples
           
    cities : List 
             List of cities

    Returns
    -------
    list_finale : List
                  List of tuples

    '''
    list_finale = []        #the final list to be returned
    for i in range(len(data)):    #gouing through the data
        min_vals=[]
        for values in range(len(data[i])):
            if data[i][values][col]!= None:   #avoiding None values
                min_vals+=[data[i][values][col]]
        min_value= min(min_vals)   #min vals
        city_min = (cities[i], min_value)
        list_finale+=[city_min]   #appeninding to the main
    return list_finale
        
def get_max(col, data, cities):
    '''
    With the data, cities and column given, it goes through the list of list
    of tuples and fetches the max value in the particular column/category
    for each city    

    Parameters
    ----------
    col : Integer
          Index value corresponding to the category in COLUMNS list
          
    data : List
           List of list of tuples
        
    cities : List 
             List of cities

    Returns
    -------
    list_finale : List
                  List of tuples

    '''
    list_finale = []     
    for i in range(len(data)):
        max_vals=[]
        for values in range(len(data[i])):
            if data[i][values][col]!= None:
                max_vals+=[data[i][values][col]]
        max_value= max(max_vals)
        city_max = (cities[i], max_value)
        list_finale+=[city_max]
    return list_finale 

def get_average(col, data, cities):
    '''
    With the data, cities and column given, it goes through the list of list
    of tuples and fetches the average value in the particular column/category
    for each city    

    Parameters
    ----------
    col : Integer
          Index value corresponding to the category in COLUMNS list
          
    data : List
           List of list of tuples
        
    cities : List 
             List of cities

    Returns
    -------
    list_finale : List
                  List of tuples

    '''
    list_finale = []
    for i in range(len(data)):
        avg_vals=[]
        n_count=0
        for values in range(len(data[i])):
            if data[i][values][col]!= None:
                avg_vals+=[data[i][values][col]]
                n_count+=1
        avg_value= round((sum(avg_vals)/n_count),2)
        city_avg = (cities[i], avg_value)
        list_finale+=[city_avg]
    return list_finale

def to_check_tol(n1,n2):
    '''
    This function just checks whether the 2 numbers are within the tolerance 
    level(<=0.02)

    Parameters
    ----------
    n1 : Float/Integer
         Number 1
         
    n2 : Float/Integer
         Number 2

    Returns
    -------
    bool
        Boolean Value(True when they are within the tolerance level and False
        otherwise)

    '''
    if n1==0:
        return False
    else:
        here_diff= (n1-n2)/n1
        abs_diff = abs(here_diff)
        if abs_diff<=0.02:
            return True
        else:
            return False
    
def actual_fun(list1):
    '''
    This function does the process of forming a 2-D list with inner lists
    having each streak and it calculates the modes and frequency and returns 
    the list of modes and the corresponding frequency

    Parameters
    ----------
    list1 : List
            List of floats/integers 

    Returns
    -------
    to_return_list : List
                     List of modes
                     
    high_count : Integer
                 Frequency of the modes

    '''
    sort_l = sorted(list1) 
    final_list=[]
    couple_list=[sort_l[0]]
    c=0
    while c<len(sort_l):
        if c==len(sort_l)-1:
            final_list.append(couple_list)
            break
        else:
            bool_value = to_check_tol(couple_list[0],sort_l[c+1])
            if bool_value== True:
                couple_list.append(sort_l[c+1])
                c+=1
            else:
                final_list.append(couple_list)
                flag=0
                for val in final_list:
                    if sort_l[c+1] in val:
                        flag=1
                        break
                if flag==0:
                    couple_list=[sort_l[c+1]]
                c+=1
                
    final_list = sorted(final_list, key=len, reverse= True)
    
    
    count_ele_list=[]
    for j in final_list:
        count_ele_list.append((len(j),j[0]))
    to_return_list=[]
    high_count=count_ele_list[0][0]
    for y in count_ele_list:
        if y[0]==high_count:
            to_return_list.append(y[1])
            
    if to_return_list==sorted(list1):
        to_return_list=[]
        high_count=1
    
    return to_return_list, high_count  
 
def get_modes(col,data,cities):
    '''
    With the data, cities and column given, it goes through the list of list
    of tuples and fetches the modes value and the frequency in the particular 
    column/category for each city    

    Parameters
    ----------
    col : Integer
          Index value corresponding to the category in COLUMNS list
          
    data : List
           List of list of tuples
        
    cities : List 
             List of cities

    Returns
    -------
    list_finale : List
                  List of tuples

    '''
    list_finale=[]
    for i in range(len(data)):
        column_nos=[]
        for values in range(len(data[i])):
            if data[i][values][col]!= None:
                column_nos+= [data[i][values][col]]
        mode_nos, freq = actual_fun(column_nos)
        mode_tuple = (cities[i], mode_nos, freq)
        list_finale+=[mode_tuple]
    return list_finale
          
def high_low_averages(data, cities, categories):
    '''
    It calculate the high and the low averages of the cities under the given
    categories and returns list of list of tuples

    Parameters
    ----------
    data : List
           List of list of tuples
           
    cities : List
             List of cities
             
    categories : List
                 List of categories

    Returns
    -------
    list_finale : List
                  List of tuples

    '''
    COLUMNS = ["date",  "average temp", "high temp", \
               "low temp", "precipitation", \
               "snow", "snow depth"]
    list_finale = []
    for category in categories:
        if category not in COLUMNS:
            list_finale.append(None)
        else:
            index = COLUMNS.index(category)
            avg_val = get_average(index, data, cities)
            sorted_lowtohigh= sorted(avg_val, key=itemgetter(1))
            sorted_hightolow= sorted(avg_val, key=itemgetter(1), reverse=True)
            category_l= sorted_lowtohigh[0:1]+sorted_hightolow[0:1]
            list_finale.append(category_l)
    return list_finale

def display_statistics(col, data, cities):
    '''
    It takes in data, the category index and the list of cities and displays
    them as a statistical summary

    Parameters
    ----------
    col : Integer
          Index of category
          
    data : List 
           List of list of tuples
           
    cities : List
             List of cities

    Returns
    -------
    None.

    '''
    min_list_of_tuples = get_min(col,data,cities)
    max_list_of_tuples = get_max(col,data,cities)
    avg_list_of_tuples = get_average(col, data, cities)
    modes_list_of_tuples = get_modes(col, data,cities)
    for order in range(len(cities)):
        print("\t{}: ".format(cities[order]))
        print("\tMin: {:.2f} Max: {:.2f} Avg: {:.2f}".format(\
min_list_of_tuples[order][1],max_list_of_tuples[order][1],\
    avg_list_of_tuples[order][1]))
        if modes_list_of_tuples[order][2]==1:
            print("\tNo modes.")
        else:
            mode_l=modes_list_of_tuples[order][1][:]
            for val in range(len(mode_l)):
                mode_l[val] = str(mode_l[val])
            mode_l_to_str = ",".join(mode_l)
            print("\tMost common repeated values ({:d} occurrences): \
{:s}\n".format(modes_list_of_tuples[order][2],mode_l_to_str))
             
def main():
    """
    This is the main function which displays the various menu options and 
    performs the activities(calling the above written functions accordingly)
    which the user asks for and loops until the user wants to break.
    
    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
    COLUMNS = ["date",  "average temp", "high temp", "low temp",\
               "precipitation", \
               "snow", "snow depth"]

    BANNER = 'This program will take in csv files with weather data and compare \
the sets.\nThe data is available for high, low, and average temperatures,\
\nprecipitation, and snow and snow depth.'    


    MENU = '''
        Menu Options:
        1. Highest value for a specific column for all cities
        2. Lowest value for a specific column for all cities
        3. Average value for a specific column for all cities
        4. Modes for a specific column for all cities
        5. Summary Statistics for a specific column for a specific city
        6. High and low averages for each category across all data
        7. Quit
        Menu Choice: '''
            
    print(BANNER)
    city_list, fp_list= open_files()
    data = read_files(fp_list)
    choice = int(input(MENU))
    while True:
        if choice == 7:
            print("\nThank you using this program!")
            break
        elif choice == 1:
            start_dat = input("\nEnter a starting date \
(in mm/dd/yyyy format): ")
            end_dat = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            extracted_data = get_data_in_range(data, start_dat, end_dat)
            desired_categ = input("\nEnter desired category: ")
            if desired_categ.lower() not in COLUMNS:
                while desired_categ.lower() not in COLUMNS:
                    print("\n\t{} category is not found.")
                    desired_categ = input("\nEnter desired category: ")
            col = COLUMNS.index(desired_categ.lower())
            ltotuple_to_use = get_max(col, extracted_data, city_list)
            print("\n\t{}: ".format(desired_categ.lower()))
            for ord_n in range(len(ltotuple_to_use)):
                print("\tMax for {:s}: {:.2f}".format(\
ltotuple_to_use[ord_n][0], ltotuple_to_use[ord_n][1]))
            choice = int(input(MENU))
        elif choice == 2:
            start_dat = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_dat = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            extracted_data = get_data_in_range(data, start_dat, end_dat)
            desired_categ = input("\nEnter desired category: ")
            if desired_categ.lower() not in COLUMNS:
                while desired_categ.lower() not in COLUMNS:
                    print("\n\t{} category is not found.")
                    desired_categ = input("\nEnter desired category: ")
            col = COLUMNS.index(desired_categ.lower())
            ltotuple_to_use = get_min(col, extracted_data, city_list)
            print("\n\t{}: ".format(desired_categ.lower()))
            for ord_n in range(len(ltotuple_to_use)):
                print("\tMin for {:s}: {:.2f}".format(\
    ltotuple_to_use[ord_n][0], ltotuple_to_use[ord_n][1]))
            choice = int(input(MENU)) 
        elif choice == 3:
            start_dat = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_dat = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            extracted_data = get_data_in_range(data, start_dat, end_dat)
            desired_categ = input("\nEnter desired category: ")
            if desired_categ.lower() not in COLUMNS:
                while desired_categ.lower() not in COLUMNS:
                    print("\n\t{} category is not found.")
                    desired_categ = input("\nEnter desired category: ")
            col = COLUMNS.index(desired_categ.lower())
            ltotuple_to_use = get_average(col, extracted_data, city_list)
            print("\n\t{}: ".format(desired_categ.lower()))
            for ord_n in range(len(ltotuple_to_use)):
                print("\tAverage for {:s}: {:.2f}".format(\
                    ltotuple_to_use[ord_n][0], ltotuple_to_use[ord_n][1]))
            choice = int(input(MENU))          
        elif choice == 4:
            start_dat = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_dat = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            extracted_data = get_data_in_range(data, start_dat, end_dat)
            desired_categ = input("\nEnter desired category: ")
            if desired_categ.lower() not in COLUMNS:
                while desired_categ.lower() not in COLUMNS:
                    print("\n\t{} category is not found.")
                    desired_categ = input("\nEnter desired category: ")
            col = COLUMNS.index(desired_categ.lower())
            ltotuple_to_use = get_modes(col, extracted_data, city_list)
            print("\n\t{}: ".format(desired_categ.lower()))
            for ord_n in range(len(ltotuple_to_use)):
                if ltotuple_to_use[ord_n][2]==1:
                    print("\tNo modes.")
                else:
                    mode_l=ltotuple_to_use[ord_n][1][:]
                    for val in range(len(mode_l)):
                        mode_l[val] = str(mode_l[val])
                    mode_l_to_str = ",".join(mode_l)
                    print("\tMost common repeated values for \
{:s} ({:d} occurrences): {:s}\n".format(ltotuple_to_use[ord_n][0],\
    ltotuple_to_use[ord_n][2],mode_l_to_str))
            choice = int(input(MENU))
        elif choice== 5:
            start_dat = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_dat = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            extracted_data = get_data_in_range(data, start_dat, end_dat)
            desired_categ = input("\nEnter desired category: ")
            if desired_categ.lower() not in COLUMNS:
                while desired_categ.lower() not in COLUMNS:
                    print("\n\t{} category is not found.".format(\
desired_categ.lower()))
                    desired_categ = input("\nEnter desired category: ")
            col = COLUMNS.index(desired_categ.lower())
            print("\n\t{}: ".format(desired_categ.lower()))
            display_statistics(col, extracted_data, city_list)          
            choice = int(input(MENU))   
        elif choice== 6:
            start_dat = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_dat = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            extracted_data = get_data_in_range(data, start_dat, end_dat)
            desired_categ = input("\nEnter desired categories \
seperated by comma: ")
            categ_list = desired_categ.split(",")
            for val in range(len(categ_list)):
                categ_list[val] = categ_list[val].lower()
            print("\nHigh and low averages for each category across all data.")
            high_low_compared = high_low_averages(extracted_data,\
city_list, categ_list)
            for index in range(len(high_low_compared)):
                if high_low_compared[index]== None:
                    print("\n\t{} category is not found.".format(\
categ_list[index]))
                else:
                    compared_list = high_low_compared[index]
                    print("\n\t{}: ".format(categ_list[index]))
                    print("\tLowest Average: {:s} = {:.2f} Highest \
Average: {:s} = {:.2f}".format(compared_list[0][0],compared_list[0][1],\
compared_list[1][0],compared_list[1][1]))
            choice = int(input(MENU))                   


if __name__ == "__main__":
    main()
                                           
