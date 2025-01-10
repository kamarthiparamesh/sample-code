import random
import time
from concurrent.futures import ThreadPoolExecutor

def functionA():
    """
    Generate random data for a specific number of days.
    Returns a dictionary with days as keys and random 2-digit numbers as values.
    """
    return [random.randint(10, 99) for _ in range(730)]

def functionB(day_data):
    """
    Process a single day's data and return some information.
    """
    # Simulate processing by creating a random float between 1.0 and 10.0
    processed_value = random.uniform(1.0, 10.0)
    time.sleep(0.04)
    return round(processed_value, 2)

def process_data(chunk_data):
    """
    Process a chunk of data (e.g., 15 days or 30 days or 2 years).
    """
    results = []
    for day, value in chunk_data:
        processed_value = functionB(value)
        results.append((day, value, processed_value))
    return results

def sequentialCall():
    """
    Execute logic sequentially for all the days, one by one using process_chunk for each day.
    """
    start_time = time.time()
    # Call FunctionA to get 2 years of data
    data_from_functionA = functionA()
    
    # Process and print data sequentially
    for index, value in enumerate(data_from_functionA, start=1):
        # Treat each day as a chunk (1-day chunk)
        chunk_data = [(index, value)]
        processed_info = process_data(chunk_data)
        
        # Print the processed data directly
        day, original, processed = processed_info[0]  # Extract the single processed result
        #print(f"Day {day}: Original={original}, Processed={processed}")
    
    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nSequential Call: Total Execution Time: {total_time:.2f} seconds")

def parallelChunks(chunk_size):
    """
    Execute logic in parallel for the data, processing chunks of a given size (e.g., 30 days, 15 days).
    """
    start_time = time.time()
    
    # Call FunctionA to get 2 years of data
    data_from_functionA = functionA()
    
    # Split the data into chunks of the given size
    chunked_data = [
        [(i + 1, data_from_functionA[i]) for i in range(start, min(start + chunk_size, len(data_from_functionA)))]
        for start in range(0, len(data_from_functionA), chunk_size)
    ]
    
    # Use ThreadPoolExecutor to process the chunks in parallel and print results directly
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_data, chunk) for chunk in chunked_data]
        
        # Process and print results in a single loop
        for future in futures:
            # Unpack and print the result directly
            for day, original, processed in future.result():
                day = day * 11 #some dummy statement
                #print(f"Day {day}: Original={original}, Processed={processed}")
    
    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nParallel Chunks Call (Chunk size: {chunk_size}): Total Execution Time: {total_time:.2f} seconds")


if __name__ == "__main__":
    # print("Calling Sequential Call:")
    # sequentialCall()
    parallelChunks(1) # parallel all at once  
    parallelChunks(15) # parallel 15 days 
    parallelChunks(30) # parallel montly wise 
    parallelChunks(365) # parallel year wise i.e 2 parallel calls
    
