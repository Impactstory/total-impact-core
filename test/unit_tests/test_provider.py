import requests, os, unittest, time, threading, json, memcache, sys, traceback
from test.utils import slow

from totalimpact.providers.provider import Provider, ProviderFactory
from totalimpact.providers.provider import ProviderError, ProviderTimeout, ProviderServerError
from totalimpact.providers.provider import ProviderClientError, ProviderHttpError, ProviderContentMalformedError
from totalimpact.providers.provider import ProviderConfigurationError, ProviderValidationFailedError
from totalimpact.config import Configuration, StringConfiguration
from totalimpact.cache import Cache
from totalimpact import api

CWD, _ = os.path.split(__file__)

def successful_get(url, headers=None, timeout=None):
    return url
def timeout_get(url, headers=None, timeout=None):
    raise requests.exceptions.Timeout()
def error_get(url, headers=None, timeout=None):
    raise requests.exceptions.RequestException()

def mock_get_cache_entry(self, url):
    return None
def mock_set_cache_entry_null(self, url, data):
    pass

class InterruptableSleepThread(threading.Thread):
    def run(self):
        provider = Provider(None)
        provider._interruptable_sleep(0.5)
    
    def _interruptable_sleep(self, snooze, duration):
        time.sleep(0.5)

class InterruptableSleepThread2(threading.Thread):
    def __init__(self, method, *args):
        super(InterruptableSleepThread2, self).__init__()
        self.method = method
        self.args = args
        self.failed = False
        self.exception = None
        
    def run(self):
        try:
            self.method(*self.args)
        except Exception as e:
            self.failed = True
            self.exception = e
    
    def _interruptable_sleep(self, snooze, duration):
        time.sleep(snooze)

ERROR_CONF = json.loads('''
{
    "timeout" : { "retries" : 3, "retry_delay" : 0.1, "retry_type" : "linear", "delay_cap" : -1 },
    "http_error" : { "retries" : 3, "retry_delay" : 0.1, "retry_type" : "linear", "delay_cap" : -1 },
    
    "client_server_error" : { },
    "rate_limit_reached" : { "retries" : -1, "retry_delay" : 1, "retry_type" : "incremental_back_off", "delay_cap" : 256 },
    "content_malformed" : { "retries" : 0, "retry_delay" : 0, "retry_type" : "linear", "delay_cap" : -1 },
    "validation_failed" : { },
    
    "no_retries" : { "retries": 0 },
    "none_retries" : {},
    "one_retry" : { "retries" : 1 },
    "delay_2" : { "retries" : 2, "retry_delay" : 2 },
    "example_timeout" : { "retries" : 3, "retry_delay" : 1, "retry_type" : "linear", "delay_cap" : -1 }
}
''')

BASE_PROVIDER_CONF = StringConfiguration('''
{
    "cache" : {
        "max_cache_duration" : 86400
    }
}
''')


class Test_Provider(unittest.TestCase):

    def setUp(self):
        self.old_http_get = requests.get
        self.old_get_cache_entry = Cache.get_cache_entry
        self.old_set_cache_entry = Cache.set_cache_entry
        
        Cache.get_cache_entry = mock_get_cache_entry
        Cache.set_cache_entry = mock_set_cache_entry_null
        
        # FIXME: this belongs in a cache testing class, rather than here
        # in this unit we'll just mock out the cache
        #
        # Clear memcache so we have an empty cache for testing
        #mc = memcache.Client(['127.0.0.1:11211'])
        #mc.flush_all()
        
        # Create a base config which provides necessary settings
        # which all providers should at least implement
        self.base_provider_config = BASE_PROVIDER_CONF
        self.provider_configs = api.app.config["PROVIDERS"]
    
    def tearDown(self):
        requests.get = self.old_http_get
        Cache.get_cache_entry = self.old_get_cache_entry
        Cache.set_cache_entry = self.old_set_cache_entry
        
        # FIXME: this belongs in a cache testing class, rather than here
        # in this unit we'll just mock out the cache
        #
        # Clear memcache in case we have stored anything
        #mc = memcache.Client(['127.0.0.1:11211'])
        #mc.flush_all()

    def test_01_init(self):
        # since the provider is really abstract, this doen't
        # make much sense, but we do it anyway
        provider = Provider(None)

    def test_02_interface(self):
        # check that the interface is defined, and has appropriate
        # defaults/NotImplementedErrors
        provider = Provider(None)
        
        self.assertRaises(NotImplementedError, provider.member_items, None, None)
        self.assertRaises(NotImplementedError, provider.aliases, None)
        self.assertRaises(NotImplementedError, provider.metrics, None)
        self.assertRaises(NotImplementedError, provider.biblio, None)
        
    def test_03_error(self):
        # FIXME: will need to test this when the error handling is written
        pass
        
    # FIXME: we will also need tests to cover the cacheing when that
    # has been implemented
    
    def test_08_get_provider(self):
        pconf = None
        print self.provider_configs
        for provider_name, v in self.provider_configs.iteritems():
            if v["class"].endswith("wikipedia.Wikipedia"):
                pconf = v
                break
        provider = ProviderFactory.get_provider(pconf)
        assert provider.provider_name == "wikipedia"
        
    def test_09_get_providers(self):
        providers = ProviderFactory.get_providers(self.provider_configs)
        assert len(providers) == len(self.provider_configs)

    def test_18_exceptions_type(self):
        pcoe = ProviderConfigurationError()
        pt = ProviderTimeout()
        phe = ProviderHttpError()
        pcle = ProviderClientError(None)
        pse = ProviderServerError(None)
        pcme = ProviderContentMalformedError()
        pvfe = ProviderValidationFailedError()
        
        assert isinstance(pcoe, ProviderError)
        assert isinstance(pt, ProviderError)
        assert isinstance(phe, ProviderError)
        assert isinstance(pcle, ProviderError)
        assert isinstance(pse, ProviderError)
        assert isinstance(pcme, ProviderError)
        assert isinstance(pvfe, ProviderError)
    
        
