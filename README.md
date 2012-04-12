This is the latest version of total-impact, the software that runs the service available at http://total-impact.org

This isn't the deployed version -- it is an in-progress port the old codebase at http://github.com/mhahnel/Total-Impact
This README will be updated when this is the deployed version.

# About total-impact

See [http://total-impact/about](http://total-impact/about).

# Install and run total-impact

## Get total-impact-core code

How to install for dev:

    pip install -e .

How to install:

    python setup.py install

How to run tests:

    nosetests -v test/
    nosetests -v -A "not slow" test/

How to run the api:

    cd total-impact-core
    python totalimpact/api.py
    then surf up http://127.0.0.1:5000/

## Install memcache 

    apt-get install memcached

## Install and run CouchDB

Total-impact needs a running instance of CouchDB.

To install on Ubuntu Linux:  

1. apt-get install couchdb
1. run `couchdb` to start Couch. Done. You can test the CouchDB install at <http://localhost:5984/_utils>

To install on OSX Snow Leopard:

1. Install [homebrew](http://mxcl.github.com/homebrew/).
1. Run `brew install -v couchdb` (The `-v` for "verbose" fixes a [weird bug](http://code418.com/blog/2012/02/22/couchdb-osx-lion-verbose/)). Install will take a while, as there are big dependencies.
1. Run `couchdb` to start Couch. Done. You can test the CouchDB install at <http://localhost:5984/_utils>


## Configure CouchDB for total-impact

Customized settings for connecting to CouchDB can be set in the config/totalimpact.conf.json file.

By default, total-impact will try to contact CouchDB at http://localhost:5984/ through an admin user called "test" with password "password". To configure CouchDB for this default just use the Futon admin client at <http://localhost:5984/_utils>. At the bottom-right, click "Add User," and add user called "test" with the password "password".

When total-impact starts, it will, if necessary, create the database and all necessary views 
(you can see the view definitions [in the config](https://github.com/total-impact/total-impact/blob/master/config/totalimpact.conf.json).

## total-impact-webapp

The total-impact web application has [its own GitHub repository](http://github.com/total-impact/total-impact-webapp).


## Writing Providers

Total Impact uses many different data sources to acquire its metrics, and each of these data sources is connected to via a Provider client library which lives in the TI application.

The provider super-class and the individual implementations can be found in the module

    totalimpact.providers
    
The super-class is at:

    totalimpact.providers.provider.Provider
    
Inside the provider module there are also a bunch of other useful things such as a ProviderFactory and a suite of errors that providers can use.

To create a new provider, the first thing to do is sub-class the Provider and insert stubs for the methods which Providers can support

    from totalimpact.providers.provider import Provider
    
    class MyWonderfulProvider(Provider):
        
        def __init__(self, config, app_config):
            super(MyWonderfulProvider, self).__init__(config, app_config)
        
        def provides_metrics(self): 
            return False
        
        def member_items(self, query_string, query_type): 
            raise NotImplementedError()
            
        def aliases(self, item): 
            raise NotImplementedError()
        
        def metrics(self, item):
            raise NotImplementedError()
        
        def biblio(self, item): 
            raise NotImplementedError()

See the API documentation for full details of each of these methods, but here is a brief summary:

* provides_metrics
  Does the provider offer to gather metrics from its data sources?  This is used to determine whether the provider will get its own thread to operate in, so is important to have in addition to the metrics() function
  
* member_items
  Takes an opaque string and query type from the front end and queries the data source for identifiers related to that query.  For example, you may query the data source for a username, and get back a list of the object identifiers for that user.  This is used to seed the construction of collections of objects.
  
* aliases
  Take an item, and acquire all of the aliases that the item could be identified by.  The data source would be queried using any existing identifiers associated with an item, and would acquire more synonymous identifiers.  These should then be attached to the item's alias object (see the Item API documentation)
  
* metrics
  Take an item, and using its internal aliases populate one or more MetricSnap objects and attach them to the item's metrics object (see the Item API documentation)
  
* biblio
  Take an item and using any of the internal data for querying the data source obtain bibliographic data and attach it to the item's biblio object.  (see the Item API documentation)

Each Provider that runs must be declared in the main TI configuration file, so before you can get yours to execute you must update

    config/totalimpact.conf.json
    
and include the classname of your provider and the route to the providers configuration file.  You add it to the "providers" config option, thus:

    "providers" : [
        {
            "class" : "totalimpact.providers.myprovider.MyWonderfulProvider",
            "config" : "totalimpact/providers/myprovider.conf.json"
        },
        ... other providers ...
    ],
    
When the TI application starts, all the providers will be loaded from configuration, and those which return True on provides_metrics() will be given their own worker thread, and will be passed items from the Queue to process the metrics for.  They will also be added to an aliasing worker thread which will pass them items for which to obtain aliases.  There is no need for individual providers to know about threading - they should operate as pure client libraries joining TI to the data source.

It is not possible to provide a generic recipe for constructing a provider, as each data source will have its own idioms and approaches.  Instead, we can describe the features that the super-class has to support the implementation, and the error handling which is implemented in the thread.

In particular, the super-class provides an http_get() method which providers SHOULD and are strongly RECOMMENDED to use when connecting out over HTTP to GET web services.  This provides a wrapped HTTP request which supports cacheing.  So in your provider implementation:

    metrics(self, item):
        url = self._make_url(item)
        response = self.http_get(url)
        ... do stuff with response ...

The returned response object is a "requests" HTTP response object

If errors are thrown by any part of the provider, they should be wrapped or expressed using one of the appropriate error classes:

* ProviderConfigurationError
  if the provider's supplied configuration is incorrect, this error may be thrown.  Extends the ProviderError class, and may take a human readable message and/or an inner exception
  
    raise ProviderConfigurationError("configuration did not parse")
    
* ProviderTimeout
  raised on the provider's behalf by the http_get() method, if the HTTP request times out
  
* ProviderHttpError
  raised on the provider's behalf by the http_get() method, if the HTTP response is technically incorrect
    
* ProviderClientError
  Should be raised when the client experiences an HTTP error which was its own fault.  Typically this is when HTTP status codes in the range 400-499 are returned, although exactly when this error is thrown is left to the discretion of the Provider implementation.  It MUST take a response object as an argument in the constructor, and may also take an error message and inner exception
  
    response = self.http_get(url)
    if response.status_code >= 400 and response.status_code < 500:
        raise ProviderClientError(response, "my fault!")

* ProviderServerError
  Should be raised when the client experiences an HTTP error which was the server's fault.  Typically this is when HTTP status codes in the range 500+ are returned, although exactly when this error is thrown is left to the discretion of the Provider implementation.  It MUST take a response object as an argument in the constructor, and may also take an error message and inner exception
  
    response = self.http_get(url)
    if response.status_code > 500:
        raise ProviderServerError(response, "server's fault!")
    
* ProviderContentMalformedError
  Should be raised when the client is unable to parse the document retrieved from the data source (e.g. malformed XML, JSON, etc).  Extends the ProviderError class, and may take a human readable message and/or an inner exception
  
    raise ProviderContentMalformedError("was not valid XML")

* ProviderValidationFailedError
  Should be raised when the client is unable to validate the successfully parsed document as the document it was expecting.  This could happen if, for example, the response from the data source has changed structure (e.g. new XML schema) without the provider being aware of the change.  Extends the ProviderError class, and may take a human readable message and/or an inner exception
  
    raise ProviderValidationFailedError("couldn't find the result element")

If a provider experiences an error, the supervising thread will consider the options and may re-try requests, in order to mitigate against errors like network blips or known weaknesses in data sources.  The Provider is responsible for providing the supervising thread the information it needs to make those decisions, which it does be declaring in its own configuration file the following block:

    "errors" : {
        "timeout" : { 
            "retries" : 0, "retry_delay" : 0, 
            "retry_type" : "linear", "delay_cap" : -1 },
        "http_error" : { 
            "retries" : 0, "retry_delay" : 0, 
            "retry_type" : "linear", "delay_cap" : -1 },
        "client_server_error" : { 
            "retries" : 0, "retry_delay" : 0, 
            "retry_type" : "linear", "delay_cap" : -1 },
        "rate_limit_reached" : { 
            "retries" : -1, "retry_delay" : 1, 
            "retry_type" : "incremental_back_off", "delay_cap" : 256 },
        "content_malformed" : { 
            "retries" : 0, "retry_delay" : 0, 
            "retry_type" : "linear", "delay_cap" : -1 },
        "validation_failed" : { 
            "retries" : 0, "retry_delay" : 0, 
            "retry_type" : "linear", "delay_cap" : -1}
    },

This is retrieved by the supervising thread during an exception, and used to make decisions as to the re-try strategy.  Each exception corresponds to one of the error keys (e.g. ProviderTimeout -> "timeout")

CONTINUE ...
