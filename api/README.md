# Startup Generator API

A web API and CLI for generating ridiculous startup company ideas.

## CLI

Run the application locally to generate startup ideas without all the frills:
```
> startup-generator-api run --set_1 tests/data/word_set_1.txt --set_2 tests/data/word_set_2.txt
```

After setting up the environment variables, start the debug server like so:
```
> startup-generator-api api
```

## Environment Variables

Set these environment variables:
- mongo_reader_uri=value
- mongo_writer_uri=value
- flask_secret_key=value
- admin_username=value
- admin_password=value
- serve_admin_from=\<s3, file, redirect\>
    - For `s3`, also set `redirect_s3_bucket_name=value`
    - For `file` also set `redirect_path=value` (default=static)
    - For `redirect` also set `redirect_url=value` (default=http://localhost:4200)
- login_disabled=\<True, False\> (optional, default=False)

## Development

Run linting and tests with:
```
tox
```
