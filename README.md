# DOIRequest

This is a [KBase](https://kbase.us) module generated by the [KBase Software Development Kit (SDK)](https://github.com/kbase/kb_sdk).

You will need to have the SDK installed to use this module. [Learn more about the SDK and how to use it](https://kbase.github.io/kb_sdk_docs/).

You can also learn more about the apps implemented in this module from its [catalog page](https://narrative.kbase.us/#catalog/modules/DOIRequest) or its [spec file]($module_name.spec).

## Actually...

This is a prototype service for creating requests for DOIs for static narratives. 

Although it works with kb-sdk and is compatible with the KBase service wizard app runner, it does not use most of the machinery. Rather it is a simple fastapi-based service.

## Usage

```shell
ORCID_SANDBOX_CLIENT_ID=<client id> ORCID_SANDBOX_CLIENT_SECRET=<client secret> docker compose up
```

It currently works with the ORCID sandbox, so the credentials used above must be obtained from an ORCID sandbox account.

## Development

### build image
```shell
docker compose build
```

### shell into image to inspect
```shell
docker compose run --entrypoint sh orcidlink
```  

### run it
```shell
docker compose up
```
