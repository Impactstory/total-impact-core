import redis, logging, json, datetime, os
from collections import defaultdict
import threading

from totalimpact.providers.provider import ProviderFactory


logger = logging.getLogger("ti.tiredis")

currently_updating_lock = threading.Lock()

def from_url(url, db=0):
    r = redis.from_url(url, db)
    return r

def clear_currently_updating_status(self):
    # delete currently updating things, to start fresh
    currently_updating_keys = myredis.keys("currently_updating:*")
    for key in currently_updating_keys:
        self.delete(key)

def set_currently_updating(self, tiid, value):
    key = "currently_updating:"+tiid 
    expire = 60*60*24  # for a day    
    self.set_value(key, value, expire)

def get_currently_updating(self, tiid):
    key = "currently_updating:"+tiid 
    return self.get_value(key)

def delete_currently_updating(self, tiid):
    key = "currently_updating:"+tiid 
    return self.delete(key)


def init_currently_updating_status(self, item_id, providers):
    logger.debug(u"set_all_providers for '{tiid}'.".format(
        tiid=item_id))
    now = datetime.datetime.utcnow().isoformat()
    currently_updating_status = {}
    for provider_name in providers:
        currently_updating_status[provider_name] = now + ": not started"
    with currently_updating_lock:
        self.set_currently_updating(item_id, currently_updating_status)


def set_provider_started(self, item_id, provider_name):
    now = datetime.datetime.utcnow().isoformat()
    with currently_updating_lock:
        currently_updating_status = self.get_currently_updating(item_id)
        if not currently_updating_status:
            currently_updating_status = {}
        currently_updating_status[provider_name] = now + ": started"
        self.set_currently_updating(item_id, currently_updating_status)
    logger.info(u"set_provider_started for %s %s" % (
        item_id, provider_name))


def set_provider_finished(self, item_id, provider_name):
    with currently_updating_lock:
        currently_updating_status = self.get_currently_updating(item_id)
        if provider_name in currently_updating_status:
            del currently_updating_status[provider_name]
        if currently_updating_status.keys():
            self.set_currently_updating(item_id, currently_updating_status)
        else:
            self.delete_currently_updating(item_id)

    logger.info(u"set_provider_finished for {tiid} {provider_name}.  Still finishing: {providers_left}".format(
        tiid=item_id, provider_name=provider_name, providers_left=currently_updating_status.keys()))

    return currently_updating_status


def get_providers_currently_updating(self, item_id):
    with currently_updating_lock:
        currently_updating_status = self.get_currently_updating(item_id)
    print "get_providers_currently_updating", currently_updating_status
    if not currently_updating_status:
        currently_updating_status = {}
    providers_currently_updating = [provider for provider in currently_updating_status if currently_updating_status[provider]]
    return providers_currently_updating


def get_num_providers_currently_updating(self, item_id):
    providers_currently_updating = self.get_providers_currently_updating(item_id)
    return len(providers_currently_updating)



def add_to_alias_queue(self, tiid, aliases_dict, aliases_already_run=[]):
    queue_string = json.dumps([tiid, aliases_dict, aliases_already_run])
    logger.debug(u"Adding to alias_queue: {tiid} /biblio_print {aliases_dict} {aliases_already_run}".format(
        tiid=tiid, aliases_dict=aliases_dict, aliases_already_run=aliases_already_run))
    self.lpush("aliasqueue", queue_string)

def set_value(self, key, value, time_to_expire):
    json_value = json.dumps(value)
    self.set(key, json_value)
    self.expire(key, time_to_expire)

def get_value(self, key):
    try:
        json_value = self.get(key)
        value = json.loads(json_value)
    except TypeError:
        value = None
    return value



def set_memberitems_status(self, memberitems_key, query_status):
    key = "memberitems:"+memberitems_key 
    expire = 60*60*24  # for a day    
    self.set_value(key, query_status, expire)

def get_memberitems_status(self, memberitems_key):
    key = "memberitems:"+memberitems_key 
    value = self.get_value(key)
    return value

def set_confidence_interval_table(self, size, level, table):
    key = "confidence_interval_table:{size},{level}".format(
        size=size, level=level)
    expire = 60*60*24*7  # for a week
    self.set_value(key, table, expire)

def get_confidence_interval_table(self, size, level):
    key = "confidence_interval_table:{size},{level}".format(
        size=size, level=level)
    value = self.get_value(key)
    return value

def set_reference_histogram_dict(self, genre, refset_name, year, table):
    key = "refset_histogram:{genre},{refset_name},{year}".format(
        genre=genre, refset_name=refset_name, year=year)
    expire = 60*60*24  # for a day    
    self.set_value(key, table, expire)

def get_reference_histogram_dict(self, genre, refset_name, year):
    key = "refset_histogram:{genre},{refset_name},{year}".format(
        genre=genre, refset_name=refset_name, year=year)
    value = self.get_value(key)
    return value

def set_reference_lookup_dict(self, genre, refset_name, year, table):
    key = "refset_lookup:{genre},{refset_name},{year}".format(
        genre=genre, refset_name=refset_name, year=year)
    expire = 60*60*24  # for a day    
    self.set_value(key, table, expire)

def get_reference_lookup_dict(self, genre, refset_name, year):
    key = "refset_lookup:{genre},{refset_name},{year}".format(
        genre=genre, refset_name=refset_name, year=year)
    value = self.get_value(key)
    return value




redis.Redis.set_value = set_value
redis.Redis.get_value = get_value
redis.Redis.set_currently_updating = set_currently_updating
redis.Redis.get_currently_updating = get_currently_updating
redis.Redis.delete_currently_updating = delete_currently_updating
redis.Redis.clear_currently_updating_status = clear_currently_updating_status
redis.Redis.init_currently_updating_status = init_currently_updating_status
redis.Redis.set_provider_started = set_provider_started
redis.Redis.set_provider_finished = set_provider_finished
redis.Redis.get_providers_currently_updating = get_providers_currently_updating
redis.Redis.get_num_providers_currently_updating = get_num_providers_currently_updating
redis.Redis.add_to_alias_queue = add_to_alias_queue
redis.Redis.set_memberitems_status = set_memberitems_status
redis.Redis.get_memberitems_status = get_memberitems_status
redis.Redis.set_confidence_interval_table = set_confidence_interval_table
redis.Redis.get_confidence_interval_table = get_confidence_interval_table
redis.Redis.set_reference_histogram_dict = set_reference_histogram_dict
redis.Redis.get_reference_histogram_dict = get_reference_histogram_dict
redis.Redis.set_reference_lookup_dict = set_reference_lookup_dict
redis.Redis.get_reference_lookup_dict = get_reference_lookup_dict


myredis = from_url(os.getenv("REDISTOGO_URL"))

myredis.clear_currently_updating_status()

# now add the things that are currently in aliasqueue
received = myredis.lrange(["aliasqueue"], 0, -1)
print "**** RECIEVED MESSAGES", received
for message_json in received:
    try:
        logger.debug(u"Read from redis, adding to currently_updating_status {message_json}".format(
            message_json=message_json[0:50]))        
        message = json.loads(message_json) 
        init_currently_updating_status(tiid, 
            ProviderFactory.providers_with_metrics(default_settings.PROVIDERS))
    except (TypeError, KeyError):
        logger.info(u"error processing redis message {message_json}".format(
            message_json=message_json))

