## Features
From network crawl free chinese proxy, verify and then establish the proxy pool. Currently only supports saving to MySQL database. Verify proxy validity and connection time in the proxy pool at regular intervals.


## Quick start
* clone repository
* Rename 'db.conf.example' to 'db.conf' and modify the corresponding field value
* python main.py &

### 'db.conf' Field Description
* host: database address, if local, fill in "localhost" directly; fill in server's ip if on the remote server.
* port: port number, the default is 3306, generally does not need to be changed
* user: database username
* password: database password
* dbname: the name of the stored database, need to be created in advance

## Scalable
* New proxy source
If you want to add a new free proxy source, write a new class directly in 'lib/proxy' and inherit the 'BasicSource'. Then introduced in lib/proxy/all_source.py.
* New database storage method
If you want to add a new database storage method, write a new class directly in 'lib/database', and inherit the 'database'. Then in 'lib/database/db_object.py' returns an instance mimicing 'mysql'.