import time
import logging
import inspect
import threading

def triggered_by(list_of_triggers):
    if (list_of_triggers == []):
        raise ValueError("No arguments for triggered_by decorator!")
    def decorator(func):
        def new_callback(self_pointer, queue, lock, *args, **kwargs):
            lock.acquire()
            trigger_to_process = queue[0]
            lock.release()
            if trigger_to_process in list_of_triggers:
                return func(*args, **kwargs)
            else:
                return (lambda: False)
        return new_callback
    return decorator

class Core:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock() 
        logging.basicConfig()
        self.logger = logging.getLogger('core')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Core started!")

    def _get_functions(self, start_of_string):
        all_methods = inspect.getmembers(self, predicate=inspect.ismethod)
        func_list = []
        for (name, func) in all_methods:
            if name.startswith(start_of_string):
                func_list.append(func)
        return func_list

    def _get_triggers(self):
        return self._get_functions("trigger")

    def _get_callbacks(self):
        return self._get_functions("callback")

    def _start_triggers(self, list_of_triggers):
        for trigger in list_of_triggers:
            threading.Thread(target=trigger, args=(self.queue, self.lock,), name=str(trigger)).start()
            self.logger.debug("Started function {} as thread".format(str(trigger)))

    def _run_callbacks(self, list_of_callbacks):
        for callback in list_of_callbacks:
            callback(self.queue, self.lock)
            self.logger.debug("Processed callback {}".format(str(callback)))

    def _monitor_queue(self):
        callback_list = self._get_callbacks()
        while True:
            self.logger.debug("Heartbeat: Queue = {}".format(self.queue))
            self.lock.acquire()
            if (len(self.queue) != 0):
                self.logger.debug("Heartbeat: Processing {}".format(self.queue[0]))
                self.lock.release()
                self._run_callbacks(callback_list) #Run the callbacks if the queue is not empty
                self.lock.acquire()
                self.queue.pop(0) #Delete the processed callback
                self.lock.release()
            else:
                self.lock.release()
            time.sleep(1)

    # Starts the triggers and manages the execution
    def run(self):
    	trigger_list = self._get_triggers()
        self.logger.debug("Found list of triggers is {}".format(trigger_list))
        self._start_triggers(trigger_list)
        self._monitor_queue()