# xproxy.io middleware rotator

## usage

Add this 2 middlewares
```python
SPIDER_MIDDLEWARES = {
    "rotate_proxy_middleware.middleware.RotateProxyMiddleware": 1,
}
```

```python
DOWNLOADER_MIDDLEWARES = {
    "rotate_proxy_middleware.middleware.RandomProxy": 1,
}
```

set proxy list:
```python
PROXY_LIST = ["http://192.168.1.162:4001", "http://192.168.1.162:4002"],
```

set proxy rotate endpoint:
```python
RESTART_URL = "http://192.168.1.162/api/v1/rotate_ip/proxy/",
```
