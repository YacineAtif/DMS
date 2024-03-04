import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Database connection parameters
from Database.db_utils import connect_to_database, close_connection_to_database


def insert_data_from_csv(csv_file, cursor):
    with open(csv_file, newline='') as file:
        # Specify the semicolon as the delimiter
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Adjust the field names to match the actual CSV headers, which appear to include 'ID' rather than 'id'
            data_to_insert = (
                row['ID'],  # Use 'ID' based on your CSV output
                row['Time'],
                row['X'],
                row['Y'],
                row['Speed'],
                row['Type']
            )
            try:
                cursor.execute("""
                    INSERT INTO realtrafficdata (id, timestamp, x, y, speed, type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, data_to_insert)
            except Exception as e:
                print(f"Error inserting row: {e} - Row data: {data_to_insert}")


def insert_data_from_csv_file(csv_file_path):
    # Path to your CSV file
    csv_file_path = '2019-05-17_00h_tracks.csv'
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                insert_data_from_csv(csv_file_path, cur)
                conn.commit()  # Commit changes
                print("Insertion Completed")
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback changes on error
        finally:
            close_connection_to_database(conn)  # Close the connection
    else:
        print("Connection could not be established.")


def analyze_vehicle_types():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
          type,
          COUNT(DISTINCT id) AS count
        FROM 
          realtrafficdata
        GROUP BY 
          type
        ORDER BY 
          type;
    """)
    results = cursor.fetchall()
    for type_id, count in results:
        if type_id == 0:
            print(f"Pedestrians: {count}")
        elif type_id == 1:
            print(f"Bicyclists: {count}")
        elif type_id == 2:
            print(f"Light Vehicles: {count}")
        elif type_id == 3:
            print(f"Heavy Vehicles: {count}")
        else:
            print(f"Other Types ({type_id}): {count}")

    cursor.close()
    close_connection_to_database(conn)


def calculate_data_duration():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
          MIN(timestamp) AS start_time,
          MAX(timestamp) AS end_time
        FROM 
          realtrafficdata;
    """)
    result = cursor.fetchone()
    if result[0] is not None and result[1] is not None:
        start_time, end_time = result
        # Print the start and end dates of data collection
        print(f"Data collection started at: {start_time}")
        print(f"Data collection ended at: {end_time}")

        # Calculate and print the duration in a more human-readable format
        duration = end_time - start_time
        total_seconds = duration.total_seconds()
        days = duration.days
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if days > 0:
            print(
                f"Total data collection duration: {days} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
        else:
            print(f"Total data collection duration: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
    else:
        print("Unable to calculate duration - check if the table is empty or timestamps are null.")

    close_connection_to_database(conn)


def fetch_hourly_traffic_data():
    # SQL query to fetch traffic data
    query = """
    SELECT DATE(timestamp) as day, EXTRACT(HOUR FROM timestamp) as hour, type, COUNT(*) as count
    FROM realtrafficdata
    GROUP BY day, hour, type
    ORDER BY day, hour, type;
    """

    # Connect to the database
    conn = connect_to_database()

    try:
        # Execute the query and fetch data
        traffic_data = pd.read_sql_query(query, conn)

        return traffic_data
    finally:
        close_connection_to_database(conn)


def analyze_data():
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                analyze_vehicle_types(cur)
                print("\nData Collection Duration Analysis:")
                calculate_data_duration(cur)
        except Exception as e:
            print(f"An error occurred during analysis: {e}")
        finally:
            conn.close()
    else:
        print("Connection could not be established.")

    close_connection_to_database(conn)


def plot_hourly_traffic():
    # Fetch the data
    traffic_data = fetch_hourly_traffic_data()
    type_labels = {0: 'Pedestrians', 1: 'Bicyclists', 2: 'Light Vehicles', 3: 'Heavy Vehicles'}

    # Convert type codes to readable labels
    traffic_data['type'] = traffic_data['type'].map(type_labels)

    # Plotting
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=traffic_data, x='hour', y='count', hue='type', marker='o')
    plt.title('Hourly Traffic Patterns')
    plt.xlabel('Hour of Day')
    plt.ylabel('Count')
    plt.xticks(range(0, 24))  # Assuming hour is in 24-hour format
    plt.grid(True)
    plt.legend(title='Traffic Type')
    plt.tight_layout()
    plt.show()


def fetch_vehicle_speeds(vehicle_id):
    query = f"""
    SELECT timestamp, speed
    FROM realtrafficdata
    WHERE type = 2 AND id = {vehicle_id}  -- Adjust the type if necessary
    ORDER BY timestamp;
    """
    # Assuming you've defined connect_to_database() earlier or replace the next line with your connection logic
    conn = connect_to_database()

    try:
        return pd.read_sql_query(query, conn)
    finally:
        close_connection_to_database(conn)


def plot_speed(vehicle_id):
    speed_data = fetch_vehicle_speeds(vehicle_id)
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(speed_data['timestamp'], speed_data['speed'], marker='o', linestyle='-', color='b')
    plt.title(f'Speed Variation for Vehicle ID {vehicle_id}')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.xticks(rotation=45)  # Rotate dates for better readability
    plt.tight_layout()  # Adjust layout to make room for the rotated date labels
    plt.show()


def smooth_speed_plot(vehicle_id):
    speed_data = fetch_vehicle_speeds(vehicle_id)
    speed_data = speed_data.sort_values('timestamp')

    # Now apply a simple moving average with a window size of your choice
    # The window size determines how many data points will be averaged for each point in the smoothed data
    window_size = 5  # This is an example size; adjust it as needed for your dataset
    speed_data['smoothed_speed'] = speed_data['speed'].rolling(window=window_size, center=True).mean()

    # Plotting the original and smoothed speed data
    plt.figure(figsize=(14, 7))
    plt.plot(speed_data['timestamp'], speed_data['speed'], label='Original Speed', color='blue', alpha=0.5)
    plt.plot(speed_data['timestamp'], speed_data['smoothed_speed'], label='Smoothed Speed', color='red', linewidth=2)
    plt.title('Speed Variation for Vehicle ID 1514 (Smoothed)')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    analyze_vehicle_types()
