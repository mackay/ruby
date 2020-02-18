from agent import Agent
import redis
import json


class RedisFrameAgent(Agent):
    def __init__(self, uuid, world, redis_key, redis_host="localhost", redis_port=6379):
        super(RedisFrameAgent, self).__init__( uuid )

        self.world = world
        self.key = redis_key
        self.host = redis_host
        self.port = redis_port

        self.redis = None
        self.subscription = None

        self.messages = [ ]

    def _setup(self):
        self.redis = redis.Redis(host=self.host, port=self.port, db=0)
        self.subscription = self.redis.pubsub(ignore_subscribe_messages=True)
        self.subscription.subscribe(self.key)

    def observe(self, elapsed_time_ms):
        incoming_message = self.subscription.get_message()
        if incoming_message:
            self.messages.append(json.loads(incoming_message["data"]))

    def reason(self, elapsed_time_ms):
        pass

    def act(self, elapsed_time_ms):
        for message in self.messages:
            self._process_message(message)
        self.messages = [ ]

    def _process_message(self, message):
        self.world.set_sequence(message)
