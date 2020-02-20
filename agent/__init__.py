import json
import threading
import time
from datetime import datetime

from core.time import IDLE_MIN_MS


class AgentRunException(Exception):
    pass


class Agent(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.run_enable = False
        self.run_thread = None

    def load_state_from_file(self, json_file_path):
        json_data = open(json_file_path)
        data = json.load(json_data)
        json_data.close()

        self.state = data

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def run(self, callback=None):
        if self.run_enable or self.run_thread:
            raise AgentRunException("Agent already running.")

        self.run_enable = True

        t = threading.Thread( name='agent_run_loop',
                              target=self._run_loop,
                              args=(callback,),
                              kwargs=None )
        self.run_thread = t
        t.start()

    def _run_loop(self, callback=None):
        self._setup()

        timing_previous = datetime.utcnow()
        while self.run_enable:

            #per step timing
            timing_current = datetime.utcnow()
            elapsed_time_ms = float( (timing_current - timing_previous).microseconds / 1000. )
            timing_previous = timing_current

            #agent process of observe-reason-act
            self.observe(elapsed_time_ms)
            self.reason(elapsed_time_ms)
            self.act(elapsed_time_ms)

            if elapsed_time_ms < IDLE_MIN_MS:
                time.sleep(IDLE_MIN_MS / 1000)

        self._teardown()

    def observe(self, elapsed_time_ms):
        pass

    def reason(self, elapsed_time_ms):
        pass

    def act(self, elapsed_time_ms):
        pass

    def stop(self):
        self.run_enable = False
        if self.run_thread:
            self.run_thread.join()


class StatefulAgent(Agent):

    STATE_RUN_TIME_MS = "runtime_ms"
    STATE_UUID = "uuid"

    def __init__(self, uuid, initial_state={}):
        super(StatefulAgent, self).__init__(uuid)
        self.state = initial_state
        self._set_state(StatefulAgent.STATE_UUID, self.uuid)

    def load_state_from_file(self, json_file_path):
        json_data = open(json_file_path)
        data = json.load(json_data)
        json_data.close()

        self.state = data

    def _get_state(self, key, default=None):
        if key in self.state:
            return self.state[key]

        return default

    def _set_state(self, key, value):
        self.state[key] = value

    def _setup(self):
        self._set_state(StatefulAgent.STATE_RUN_TIME_MS, 0)

    def reason(self, elapsed_time_ms):
        super(StatefulAgent, self).reason(elapsed_time_ms)

        self._increment_runtime(elapsed_time_ms)

    def _increment_runtime(self, elapsed_time_ms):
        elapsed_ms = self._get_state(StatefulAgent.STATE_RUN_TIME_MS, 0)
        elapsed_ms += float(elapsed_time_ms)
        self._set_state(StatefulAgent.STATE_RUN_TIME_MS, elapsed_ms)
