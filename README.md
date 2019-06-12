# Install Usage Guide

## Setup Python

```pip install -r requirements.txt```

## Create a Excel document from a practiscore.com event 

Navigate to your practiscore.com dashboard and select an event. Notice the 'GUID' in the URL. Copy that id and use it call `ppull.py`


Example:

```python ppull.py --event_id 5a66061e-c876-4f47-be69-87bc4a07e04c --filename "Green Valley ICORE June 2019" --debug```
