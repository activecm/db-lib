---
description: |
    API documentation for modules: db_lib, merge_into_db, remove_from_db, unittest_db_lib.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `db_lib` {#id}

Test library for sqlite storage.




    
## Functions


    
### Function `add_to_db_dict` {#id}




>     def add_to_db_dict(
>         dbfiles: Union[str, list],
>         key_value_dict: dict
>     ) ‑> bool


Inside the given database, process multiple key/value lists/tuples.  For each value, add it to the existing list if not already there.

    
### Function `add_to_db_list` {#id}




>     def add_to_db_list(
>         dbfiles: Union[str, list],
>         key_str: str,
>         new_value: str
>     ) ‑> bool


Inside the given database, add the new_value to the list for key_str and write it back if changed.

    
### Function `add_to_db_list_large_value` {#id}




>     def add_to_db_list_large_value(
>         dbfiles: Union[str, list],
>         large_dbfiles: Union[str, list],
>         key_str: str,
>         new_value: str,
>         max_adds: int
>     ) ‑> bool


Inside the given database, add the new_value to the list for key_str and write it back if changed.

    
### Function `add_to_db_multiple_lists` {#id}




>     def add_to_db_multiple_lists(
>         dbfiles: Union[str, list],
>         key_value_list: list
>     ) ‑> bool


Inside the given database, process multiple key/value lists/tuples.  For each value, add it to the existing list if not already there.

    
### Function `buffer_delete_vals` {#id}




>     def buffer_delete_vals(
>         dbfiles: Union[str, list],
>         key_str: str,
>         delete_values: list,
>         max_dels: int
>     ) ‑> bool


Buffer up values that will eventually get removed from their respective databases.
You _must_ call this with buffer_delete_vals('', '', [], 0) to flush any remaining writes before shutting down.

    
### Function `buffer_merges` {#id}




>     def buffer_merges(
>         dbfiles: Union[str, list],
>         key_str: str,
>         new_values: list,
>         max_adds: int
>     ) ‑> bool


Buffer up writes that will eventually get merged into their respective databases.
You _must_ call this with buffer_merges('', '', [], 0) to flush any remaining writes before shutting down.

    
### Function `delete_key` {#id}




>     def delete_key(
>         dbfiles: Union[str, list],
>         key_str: str
>     ) ‑> bool


Delete row with key_str and associated object from database.

    
### Function `insert_key` {#id}




>     def insert_key(
>         dbfiles: Union[str, list],
>         key_str: str,
>         value_obj: Any
>     ) ‑> bool


Inserts key_str and its associated python object into database
serializing the object on the way in.

    
### Function `insert_key_large_value` {#id}




>     def insert_key_large_value(
>         dbfiles: Union[str, list],
>         large_dbfiles: Union[str, list],
>         key_str: str,
>         value_obj: Any
>     ) ‑> bool


Inserts key_str and its associates python object into database
serializing the object on the way in.

    
### Function `is_sha256_sum` {#id}




>     def is_sha256_sum(
>         possible_hash_string: str
>     ) ‑> bool


Check if the string is valid hex.  Not that it won't correctly handle strings starting with 0x.

    
### Function `remove_from_db_multiple_lists` {#id}




>     def remove_from_db_multiple_lists(
>         dbfiles: Union[str, list],
>         key_value_list: list
>     ) ‑> bool


Inside the given database, process multiple key/value lists/tuples.  For each value, remove it from the existing list if there.

    
### Function `select_all` {#id}




>     def select_all(
>         dbfiles: Union[str, list],
>         return_values: bool = True
>     ) ‑> list


Returns all entries from database.  Optional parameter return_values decides whether key, value or just key comes back in the list.

    
### Function `select_key` {#id}




>     def select_key(
>         dbfiles: Union[str, list],
>         key_str: str
>     )


Searches for key_str from database. If the key_str is found,
the obj is unserialized and returned as the original type of that value.

    
### Function `select_key_large_value` {#id}




>     def select_key_large_value(
>         dbfiles: Union[str, list],
>         large_dbfiles: Union[str, list],
>         key_str: str
>     )


Searches for key_str from database. If the key_str is found,
the obj is unserialized and returned as the original type of that value.

    
### Function `select_random` {#id}




>     def select_random(
>         dbfiles: Union[str, list]
>     ) ‑> tuple


Selects a random key,value tuple from from all databases (both
the sole read-write database at position 0 and the remaining
read-only databases.). The return value is a single key,value
tuple (unless all databases have no k,v pairs, in which case we
return ('', []) .

    
### Function `setup_db` {#id}




>     def setup_db(
>         dbfiles: Union[str, list]
>     ) ‑> bool


Create Sqlite3 DB with all required tables.

    
### Function `sha256_sum` {#id}




>     def sha256_sum(
>         raw_object
>     ) ‑> str


Creates a hex format sha256 hash/checksum of the given string/bytes object.

    
### Function `should_add` {#id}




>     def should_add(
>         dbfiles: Union[str, list],
>         key_str: str,
>         existing_list: list,
>         new_value: str
>     ) ‑> bool


Make a decision about whether we should add a new value to an existing list.




    
# Module `merge_into_db` {#id}

Import pipe-separated key-value pairs and merge into the database specified on the command line.







    
# Module `remove_from_db` {#id}

Import pipe-separated key-value pairs and remove the values (and key, if no more values) from the database specified on the command line.







    
# Module `unittest_db_lib` {#id}

Perform unit tests for the db_lib library.





    
## Classes


    
### Class `DbFunctionsTest` {#id}




>     class DbFunctionsTest(
>         methodName='runTest'
>     )


Tests for the db_lib library.

Create an instance of the class that will use the named test
method when executed. Raises a ValueError if the instance does
not have a method with the specified name.


    
#### Ancestors (in MRO)

* [unittest.case.TestCase](#unittest.case.TestCase)






    
#### Methods


    
##### Method `test001MakeDB` {#id}




>     def test001MakeDB(
>         self
>     )


Set up the base databases.

    
##### Method `test002DbExists` {#id}




>     def test002DbExists(
>         self
>     )


Check that it's on disk.

    
##### Method `test003AddKeys` {#id}




>     def test003AddKeys(
>         self
>     )


Add a few keys.

    
##### Method `test004CheckThere` {#id}




>     def test004CheckThere(
>         self
>     )


See that they are in there.

    
##### Method `test005AppendValue` {#id}




>     def test005AppendValue(
>         self
>     )


Add new items to a row value.

    
##### Method `test006AddLarge` {#id}




>     def test006AddLarge(
>         self
>     )


Make sure we can add large values across databases.

    
##### Method `test007BufferedMerges` {#id}




>     def test007BufferedMerges(
>         self
>     )


Test that buffering works correctly.

    
##### Method `test999Shutdown` {#id}




>     def test999Shutdown(
>         self
>     )


Remove test files.


-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
