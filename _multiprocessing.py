'''
A reference implementation of multiprocessing using shared memory via manager and pipe
'''
from multiprocessing import Manager, Pipe, Process


def __fetcher(shared_list):
    '''
    This function is resposible of fetching data from an external source and appending it to shared memory object.
    
    shared_list(multiprocessing.managers.ListProxy): It is a shared list for storing data.
    '''

    # This list is an imitation of commands data acquired from an external source like API, file, socket etc..
    msgs = [-1, 'OPERATION THREE', 'OPERATION TWO', 'OPERATION ONE']

    index = 0
    while index < len(msgs):
        # Appending data elements to the shared memory 
        shared_list.append(msgs[index])
        index += 1
    

def __dispatcher(endpoint, shared_list):
    """
    This fucntion is responsible for reading the shared list and sendind it via the pipe endpoint.
    
    endpoint(multiprocessing.connection.Connection); An endpoint for transfering data.
    shared_list(multiprocessing.managers.ListProxy): It is a shared list for reading data.
    """

    while True:
        if shared_list:
            # Accessing data element from the shared list
            msg = shared_list.pop()
            # Transfering data element to via pipe endpoint
            endpoint.send(msg)
            # Terminating loop 
            if msg == -1: break
    # Closing pipe endpoint    
    endpoint.close()

def __processor(endpoint):
    """
    This fucntion is responsible for receiving the data sent via pipe endpoint
    
    endpoint(multiprocessing.connection.Connection); An endpoint for transfering data.
    """
    
    while True:
        # Accessing message send via other endpoint 
        msg = endpoint.recv()
        print(f'Receive data element: {msg}')
        # Terminating loop
        if msg == -1: break
    
    # Closing pipe endpoint    
    endpoint.close()

def main():
    '''
    This is the main function
    '''
    with Manager() as manager:
    
        # Getting a shared list
        shared_list = manager.list([])
    
        # Getting a pipe endpoints
        endpoint_, _endpoint = Pipe()
    
        # Initializing processes
        fetcher  = Process(target=__fetcher, args=(shared_list,))
        dispatcher = Process(target=__dispatcher, args=(endpoint_, shared_list))
        processor = Process(target=__processor, args=(_endpoint,))
    
        # Starting processes
        fetcher.start()
        dispatcher.start()
        processor.start()
    
        # Waiting on processes to complete
        fetcher.join()
        dispatcher.join()
        processor.join()

        # End of script
        print('Script is exiting')

# Driver code
if __name__ == "__main__":

    main()
