from config import Config
from core.graceful import Graceful
from core.log import Log
from core.storage import Storage
from common import constant
from database import DB
import importlib
import json
import schedule
import threading
import time
import logging

registered_tasks = []


def thread(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()


class Executor:
    task_name: str = None

    def __init__(self, task_name):
        self.task_name = task_name

    def read_config(self):
        filepath = f"tasks/{self.task_name}.json"
        file = open(filepath, 'r')
        data = file.read()
        file.close()
        return json.loads(data)

    def run(self):
        data = self.read_config()
        tasks = data['tasks']

        log_task_name = f"task={data['name']}"

        Log("").info()
        Log(f"{log_task_name} ... Running").info()
        err = None
        result = {}
        for task in tasks:
            plugin_name = task['plugin']

            Log(f"{log_task_name} {task['description']}").info()

            try:
                context = {'result': result}
                args = task['args']

                plugin = importlib.import_module(f"plugins.{plugin_name}")
                plugin_execute = getattr(plugin, "execute")

                temp_result = plugin_execute(context, args)
                if temp_result['success'] is False:
                    err = temp_result['error']
                    break

                result[task['id']] = temp_result['data'] if 'data' in temp_result else {}
            except Exception as e:
                err = e
                Log(f"{log_task_name} error={e}").error()
                logging.exception(f"{log_task_name} stack-trace")
                break

        if err is None:
            Log(f"{log_task_name} ... Done").info()


class Task:
    storage: any = None

    def __init__(self):
        self.storage = Storage().connect()

    def is_exist(self, task_name: str):
        """
        Check if there's any existing task

        :param task_name:
        :return:
        """

        if len(registered_tasks) == 0:
            return False

        key = f"{constant.KeyTaskName}:{task_name}"
        res = self.storage.get(key)
        if res is None:
            return False
        return True

    def register_task(self, task_name: str, tasks: list):
        """
        Register a new task

        :param task_name:
        :param tasks:
        :return:
        """

        try:
            Log(f"Registering new task, name={task_name} ...").info()
            tasks.append(task_name)
            key = f"{constant.KeyTaskName}:{task_name}"
            self.storage.set(key, 1)

            executor = Executor(task_name)
            data = executor.read_config()
            for item in data['cron']:
                self.register_cron(task_name, executor, item)

            Log(f"Registering new task, name={task_name} ... Done").info()
        except Exception as e:
            Log(f"Failed to register new task, error={e}").error()
            logging.exception()

    @staticmethod
    def register_cron(name=None, executor=None, data=None):
        schedule_type = data['type']
        value = data['value']

        log_task_name = f"Scheduling task_name={name} type={schedule_type}"

        if schedule_type == 'day':
            for item in value:
                for at in item['time']:
                    if item['day'] == 'monday':
                        scheduler = schedule.every().monday.at(at)
                    elif item['day'] == 'tuesday':
                        scheduler = schedule.every().tuesday.at(at)
                    elif item['day'] == 'wednesday':
                        scheduler = schedule.every().wednesday.at(at)
                    elif item['day'] == 'thursday':
                        scheduler = schedule.every().thursday.at(at)
                    elif item['day'] == 'friday':
                        scheduler = schedule.every().friday.at(at)
                    elif item['day'] == 'saturday':
                        scheduler = schedule.every().saturday.at(at)
                    elif item['day'] == 'sunday':
                        scheduler = schedule.every().sunday.at(at)

                    Log(f"{log_task_name} day={item['day']} at={at} ... Done").info()
                    scheduler.do(thread, executor.run).tag(name)
        else:
            if schedule_type == 'seconds':
                scheduler = schedule.every(value).seconds
            elif schedule_type == 'minutes':
                scheduler = schedule.every(value).minutes
            elif schedule_type == 'hours':
                scheduler = schedule.every(value).hours

            Log(f"{log_task_name} value={value} ... Done").info()
            scheduler.do(thread, executor.run).tag(name)

    def deregister_task(self, tasks: list, existing_tasks: list):
        """
        Deregister existing task

        :param tasks:
        :param existing_tasks:
        :return:
        """

        for task in tasks:
            if task not in existing_tasks:
                try:
                    key = f"{constant.KeyTaskName}:{task}"
                    self.storage.delete(key)
                    tasks.remove(task)
                    schedule.clear(task)
                    Log(f"Deregistering existing task, name={task} ... Done").info()
                except Exception as e:
                    Log(f"Failed to deregister existing task, due to connection error to the storage").error()


def worker():
    storage = DB
    t = Task()

    try:
        result = storage.get(constant.KeyTasks)
        if result is None and len(registered_tasks) > 0:
            t.deregister_task(registered_tasks, [])
            return

        if result is not None:
            tasks = json.loads(result)

            for task in tasks:
                if t.is_exist(task):
                    continue

                t.register_task(task, registered_tasks)

            t.deregister_task(registered_tasks, tasks)
    except Exception as e:
        Log(f"Unable to connect to the storage, error={e}").error()
        logging.exception("Unable to connect to the storage")


if __name__ == '__main__':
    Log(f"Initialize storage connection, engine={Config.DB_ENGINE}").info()
    schedule.every().second.do(thread, worker)

    Log('Worker started').info()
    Log('').info()

    shutdown = Graceful()
    while not shutdown.kill_now:
        schedule.run_pending()
        time.sleep(1)
