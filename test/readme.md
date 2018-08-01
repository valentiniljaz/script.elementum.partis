## Testing

You can test only the Partis class without using the whole Kodi stack.

### Prerequisites

Add executable permissions to `run.py`

```
chmod +x run.py
```

Before running specify your Partis username and password:

```
export PARTIS_USERNAME=YOUR_USERNAME && export PARTIS_PASSWORD=YOUR_PASSWORD
```

### Run

From root folder:

```
./test/run.py
```