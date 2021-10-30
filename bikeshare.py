# Athors' Name: Sameer Khalifa
# Bike share system project

import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june'] 
# Note that the data available is only for months from Jan to Jun. 
# These months are not included ['july', 'august', 'september', 'october', 'november', 'december']

days_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


#----------------------------------------------------------------------------------
def get_long_name(short_name, long_name_list):
    """
    This function searches long_name_list for a name LIKE short_name and returns it.
    eg: if long_name_list = [saturday, sunday, monday, ...]
        and short_name = 'sun', ===> the function will return 'sunday'.
    if none or multi matches where found ===> the function will return '',
     like if short_name = 's' in the example above.
     
    Args:
        (str) short_name: first few characters of a name
        (list) long_name_list: list of full-names (months, days, cities)
    Returns:
        (str) full_name: equivalent to the short_name
    """

    slen = len(short_name)
    matches = 0
    for name in long_name_list:
        if short_name == name[:slen]:
            matches += 1
            full_name = name
    if matches == 1:
        return full_name
    else:   # If none OR multi matches found
        return ''

    
#----------------------------------------------------------------------------------
def get_entry(items_list, item_label):
    """
    This function returns the name of a city, month or day that the user has provided.
    The user input will be processed and the full-name of the item is returned.
    Args:
        (list) items_list: list of related items (months, days, cities)
        (str) item_label:  label of related item (month, day, citie)
    Returns:
        (str) item: a processed equivalent to the user input.
    """
    
    no_answer = 1
    msg = 'Please enter ' + item_label + ' name: '
    while no_answer:
        item = input(msg).lower().strip()
        item = get_long_name(item, items_list)
        msg = 'Invalid ' + item_label + ' name, Please enter correct ' + item_label + ' name: '
        if item in items_list:
            no_answer = 0      # To exit the while loop

    print('******  Selected ' + item_label.title() + ' Is: ' + item.title(),'   ******\n')
    return item


#----------------------------------------------------------------------------------
def time_break (in_seconds):
    """
    This function takes number of seconds and returns its equivalent in days, hours, minutes
     and seconds as a string.
    Args:
        (int) in_seconds: total number of seconds
    Returns:
        (str) time_string: a breakdown of in_seconds to days, hours, minutes, and seconds.

    """
    
    seconds = in_seconds % 60
    minutes = int(in_seconds / 60)
    hours   = int(minutes / 60)
    minutes = int(minutes % 60)
    days    = int(hours / 24)
    hours   = int(hours % 60)

    time_string = ''
    if days:
        time_string = str(days) + ' day, '
    if hours:
        time_string = time_string + str(hours) + ' hour, '
    if minutes:
        time_string = time_string + str(minutes) + ' min, '
    if seconds:
        time_string = time_string + str(seconds) + ' sec, '

    if time_string == '':
        return '0:00'
    else:
        return time_string[0:-2]


#----------------------------------------------------------------------------------
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('To specify the scope of the analysis; city, month and day need to be provided...')
    print('Note: you may provide a unique short names like Chi:for Chicago or Jan:for January...\n')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Cities are: ',[key.title() for key, value in CITY_DATA.items()],'\n')
    city = get_entry(list(CITY_DATA.keys()), 'city')

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Months are: ',[m.title() for m in months_list[1:]],' (All:For all months)\n')
    month = get_entry(months_list, 'month')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Days are: ',[d.title() for d in days_list[1:]],' (All:For all days)\n')
    day = get_entry(days_list, 'day')

    print('-'*40)
    return city, month, day


#----------------------------------------------------------------------------------
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = months_list[1:]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


#----------------------------------------------------------------------------------
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\n=========  Calculating The Most Frequent Times of Travel...  =========\n')
    start_time = time.time()

    #### Find and display the most common month
    # Use 'month' column that was already created in the 'load_data' function to 
    #  get most commom month.
    if month == 'all':       # Do the calculations only if "month" is not provided
        most_common_month = df['month'].mode()[0]
        print('#>  Most Common Month:       ', months_list[most_common_month].title())
    else:
        print('#>  Most Common Month:       ', month.title(), ' -  (Provided)')
        
    #### Find and display the most common day of week
    # Use 'day_of_week' column that was already created in the 'load_data' function 
    #  to get most commom day of week.
    if day == 'all':       # Do the calculations only if "day" is not provided
        most_common_day_of_week = df['day_of_week'].mode()[0]
        print('#>  Most Common Day Of Week: ', most_common_day_of_week.title())
    else:
        print('#>  Most Common Day Of Week: ', day.title(), ' -  (Provided)')

    #### Find and display the most common start hour
    # Extract hour from 'Start Time' to create new column. Note that 'Start Time'
    #  column was already converted to 'datetime' in the 'load_data' function.
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('#>  Most Common Start Hour:  ', str(most_common_start_hour)+':00  o`clock')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
#----------------------------------------------------------------------------------
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n=========  Calculating The Most Popular Stations and Trip...  =========\n')
    start_time = time.time()

    #### Find and display the most commonly used start station.
    # Use 'Start Station' column as is.
    most_common_start_station = df['Start Station'].mode()[0]
    print('#>  Most Commonly Used Start Station: ', most_common_start_station)

    #### Find and display the most commonly used end station.
    # Use 'End Station' column as is.
    most_common_end_station = df['End Station'].mode()[0]
    print('#>  Most Commonly Used End Station:   ', most_common_end_station)

    #### Find and display the most frequent combination of start station and end station trip.
    # Concatinate 'Start Station' and 'End Station' columns.
    most_common_station_combination = (df['Start Station'] + ' / ' + df['End Station']).mode()[0]
    print('#>  Most Frequent Combination Of Start Station And End Station Trip: \n        ', most_common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#----------------------------------------------------------------------------------
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n=========  Calculating Trip Duration...  =========\n')
    start_time = time.time()

    #### Find and display the total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print('#>  Total Travel Time (in seconds): ', total_travel_time, '  ('+time_break(total_travel_time)+')')

    #### Find and display the mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print('#>  Mean Travel Time  (in seconds): ', mean_travel_time, '  ('+time_break(mean_travel_time)+')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#----------------------------------------------------------------------------------
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\n=========  Calculating User Stats...  =========\n')
    start_time = time.time()

    #### Find and display the counts of user types.
    user_types_counts = df['User Type'].value_counts()
    print('#>  Counts Of User Types: \n', user_types_counts.to_string())    # use user_types_counts.to_string() to remove dtype line

    #### Find and display the counts of gender.
    # Note that there is no data available for Washington about gender or birth-year. So no need to do any calculations
    if city == 'washington':
        print('\n#>  Counts Of Gender: No Data Available For City: ' + city.title()) 
        print('\n#>  Birth Year Stats: No Data Available For City: ' + city.title()) 
    else:
        gender_counts = df['Gender'].value_counts()
        print('\n#>  Counts Of Gender: \n', gender_counts.to_string())          # use gender_counts.to_string() to remove dtype line

        #### Find and display the earliest year of birth.
        earliest_yob = df['Birth Year'].min()
        print('\n#>  Earliest Year Of Birth:    ', int(earliest_yob))

        #### Find and display the most recent year of birth.
        most_recent_yob = df['Birth Year'].max()
        print('#>  Most Recent Year Of Birth: ', int(most_recent_yob))

        #### Find and display the most common year of birth.
        most_common_yob = df['Birth Year'].mode()[0]
        print('#>  Most Common Year Of Birth: ', int(most_common_yob))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
        restart = get_long_name(restart, ['yes','no'])    # So it will accept y or n
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
