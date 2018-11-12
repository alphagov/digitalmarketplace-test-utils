# Digital marketplace test utils changelog

Records breaking or otherwise significant changes from major version bumps.

## 2.0.0

PR: [#2](https://github.com/alphagov/digitalmarketplace-test-utils/pull/8)

Change fixtures.py api
  * Remove `valid_pdf`, `valid_jpg` and `valid_jpeg`
  * Replace with `valid_pdf_bytes`, `valid_jpeg_bytes` and `valid_jpg_bytes`

The old `BytesIO` objects were mutable file like objects, not suitable for reuse in tests.
New fixtures should be employed in the creation of a new file-like object per usage.

Old code:
```
client.post('/pdf-document-upload', data={'pdf-document': (valid_pdf, 'test.pdf')})
```

New code:
```
client.post('/pdf-document-upload', data={'pdf-document': (BytesIO(valid_pdf_bytes), 'test.pdf')})
```

## 1.0.0

PR: [#2](https://github.com/alphagov/digitalmarketplace-test-utils/pull/2)

Brought in standard login views for testing login-required views in frontend applications.
