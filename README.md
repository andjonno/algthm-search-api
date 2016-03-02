Search API
---------

Search API for Algthm - Query Processor, Query Log, Autosuggest Engine. 
Queries are sent to this api in exchange for results. All queries originate from the [algthm-web](https://github.com/andjonno/algthm-web) component. 

ElasticSearch sources data from the 'Honey' that algthm async produces. It then structures it's own index from this data allowing us to 
query our index through elasticsearch query syntax and leveraging its many capabilities.
