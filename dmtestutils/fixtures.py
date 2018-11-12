"""
This file contains valid fixtures that allow the file type checking (included in
https://github.com/alphagov/digitalmarketplace-utils/pull/472) to pass:
Adding new file types that pass our file format checks can be done by finding the format entry for your given file type
in:
https://github.com/floyernick/fleep-py/blame/master/fleep/data.json

Ie:

```
{"type": "document", "extension": "pdf", "mime": "application/pdf", "offset": 0, "signature": ["25 50 44 46"]},
```

And create a BytesIO object matching the 'signature' portion of the entry like so:

```
valid_pdf = BytesIO(b'\x25\x50\x44\x46\xff\xff\xff\xff')
```

where `\xff` is just extra padding to make the document not solely include just the format requirements but some extra
bytes (not required by type checker).
"""
from io import BytesIO


valid_pdf = BytesIO(b'\x25\x50\x44\x46\xff\xff\xff\xff')

valid_jpeg = valid_jpg = BytesIO(b'\xff\xd8\xff\xff\xff\xff\xff\xff')
