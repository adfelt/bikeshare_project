import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_names = ['all','january','february','march','april','may','june']
day_names = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Please select one of these three cities: Chicago, New York, or Washington.')
    # Get's user input for which city they would like to filter by. Either: (Chicago, New York City, Washington).
    
    while True:
        city = input('Enter the name of the city: ').lower()
        if city in (CITY_DATA.keys()):
            print(f'You have chosen: {city.capitalize()}')
            break
        else:
            print("Oops that's not a valid city name. Please select either Washington, Chicago, or New York City!")
    
    
    # Asks the user to specify which month they would like to filter by.
    while True:
        month = input('Enter the name of the month, from January up to June or select all for no filter: ').lower()
        if month in month_names:
            print(f'You have chosen: {month.capitalize()}')
            break
        else:
            print("Oops that's not a valid month. Please select either all or a month ranging from January to June")
    
    #Asks the user to specify which day they would like to filter by.
    while True:
        day = input('Enter a day of the week or all for no filter: ').lower()
        if day in day_names:
            print(f'You have chosen {day.capitalize()}')
            break
        else:
            print("Oops that's not a valid day. Please select a day of the week or all for no filter.")

    print('-'*40)
    # Returns the corresponding city, month, and day that the user selected.
    return city, month, day


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

    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and the day of the week from 'Start Time' to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month.mode()[0]
    df['day_of_week'] = df['Start Time'].dt.weekday


    most_popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]

    most_popular_hour = df['hour'].mode()[0]
    # displays the most common month.
    print(f'The most popular month for bikesharing is {most_popular_month}')

    # displays the most common day of week.
    print(f'The most common day of the week: {popular_day}')

    # displays the most common start hour.
    print(f'The most common hour: {most_popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'This was the most common start station: {common_start_station}')

    # displays most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'This was the most common end station: {common_end_station}')

    # displays most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print(f"This was the most common combination of start's and stop's \n {common_combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays the total travel time in minutes.
    total_travel_time = df['Trip Duration'].sum() / 60
    print(f'This is the total travel time in minutes for bike sharing: {total_travel_time}')
    # displays the average travel time in minutes.
    average_travel_time = df['Trip Duration'].mean() / 60
    print(f'This is the average travel time in miuntes for bike sharing: {average_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'These were all the different user types: {user_types}')

    #Check to see if the dataFrame has a gender column
    if 'Gender' in df.columns:
    # Display counts of gender
        user_gender = df['Gender'].value_counts()
        print(f"These are the stats on users and their genders: {user_gender}")
    else:
        print('This city has no gender records.')      
    # Display earliest, most recent, and most common year of birth
    # Earliest DOB.
    if 'Birth Year' in df.columns:
        earliest_YOB = df['Birth Year'].min()
    # Most recent DOB.
        most_common_YOB = df['Birth Year'].mode()
    # Most recent DOB.
        most_recent_YOB = df['Birth Year'].max()
    #Print Statements.
        print(f"The earliest birth year was: {earliest_YOB}")
        print(f"The most common year of birth was: {most_common_YOB}")
        print(f"The most recent year of birth was: {most_recent_YOB}")
    else:
        print('This city has not birth year records.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function that will allow someone to keep viewing the next five lines of raw data.
def next_five_inputs(df):
    start_time = time.time()
    lower_bound = 5
    upper_bound = 10
    while True:
        #Asks the user if the would like to see the next five lines of data.
        next_five_lines=input("Would you like to see the next five lines of raw data? Enter yes or no. \n")
        if next_five_lines == 'no':
            break
        elif next_five_lines == 'yes':
            print(df.iloc[lower_bound:upper_bound])
            lower_bound += 5
            upper_bound +=5
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)
        else:
            print("I'm sorry I don't think I understand. Please enter yes or no.")


#Function to ask user if they would like to view the raw data!
def raw_inputs(df):
    start_time = time.time()
    #Sets the boundaries for which rows we would like to show if the user inputs "Yes".
    lower_bound = 0
    upper_bound = 5
    while True:
        #User_input: Asks the user if they would like to see the raw data.
        user_input = input("Would you like to see the first five rows of raw data? enter yes or no.\n")
        
        if user_input.lower() != "yes":
            break
        elif user_input.lower() == 'yes':
            print(df.iloc[lower_bound:upper_bound])
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40 + '\n')
            #Shows the next five lines of data and has the user repeat the process until the input "No".
            next_five_inputs(df)
            break
            

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#Function to ask the user if they would like to see the next five lines of data.

            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_inputs(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()