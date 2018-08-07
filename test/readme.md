## Testing

Scripts for testing specific class:
* `partis_test.py` >> Partis class
* `iplist_test.py` >> iplist class

### Prerequisites

Add executable permissions

```
chmod +x partis_test.py
chmod +x iplist_test.py
```

Before running specify your Partis username and password:

```
export PARTIS_USERNAME=YOUR_USERNAME && export PARTIS_PASSWORD=YOUR_PASSWORD
```

### Run

From root folder:

```
./test/partis_test.py
./test/iplist_test.py
```