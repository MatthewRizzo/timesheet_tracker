# -- External Packages -- #
import threading
import time

# -- Project Defined Imports -- #
from backend import constants

class DataLogger(threading.Thread):
    def __init__(self):
        """:brief Responsible for logging all existing data to an external file. Updates the file once every thread period
        """
        threading.Thread.__init__(self)

        # Its isSet() can be used to check if thread has closed
        self._thread_status = threading.Event()
        self._worker = threading.Thread(target = self._thread_function)
        self._worker.daemon = True
        
        # TODO: Decide if this call should be moved to backend controller / under which cases it gets called
        self.start_thread()
        

    #####################
    # Public Functions  #
    #####################
    def start_thread(self):
        """:Note Clears any previously existing status flags and starts the worker"""
        self._thread_status.clear()
        self._worker.start()

    def stop_thread(self):
        """Close down the thread safetly and make sure the worker stops running"""
        # Thread worker will not be allowed to run
        self._thread_status.set()
        self._worker.join()

    ######################
    # Private Functions  #
    ######################
    def _thread_function(self):
        while not self._thread_status.isSet():
            # This controls the thread period / how often it runs
            time.sleep(constants.LOGGER_THREAD_PERIOD)
            print("Thread called")