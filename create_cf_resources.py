import urllib.request, json, ssl

CF_TOKEN = 'cfat_G469blfIsdRdzI0EjalaD64sFTs9VCx2YHV5eE0K53da39cf'
ACCOUNT_ID = 'f5eae4355fa7a6e7ebab2bd8c854c329'
ctx = ssl.create_default_context()
headers = {
    'Authorization': f'Bearer {CF_TOKEN}',
    'Content-Type': 'application/json'
}

results = {}

# 1. Create D1 database
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/d1/database'
data = json.dumps({'name': 'flare-blog-db'}).encode()
req = urllib.request.Request(url, data=data, method='POST', headers=headers)
try:
    resp = urllib.request.urlopen(req, context=ctx)
    d = json.loads(resp.read())
    results['d1_id'] = d['result']['uuid']
    results['d1_name'] = d['result']['name']
    print(f"[D1] Created: {results['d1_name']} | ID: {results['d1_id']}")
except Exception as e:
    print(f"[D1] Error: {e}")

# 2. Create R2 bucket
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/r2/buckets'
data = json.dumps({'name': 'flare-blog-images'}).encode()
req = urllib.request.Request(url, data=data, method='POST', headers=headers)
try:
    resp = urllib.request.urlopen(req, context=ctx)
    d = json.loads(resp.read())
    results['r2_name'] = d['result']['name']
    print(f"[R2] Created: {results['r2_name']}")
except Exception as e:
    print(f"[R2] Error: {e}")

# 3. Create KV namespace
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/storage/kv/namespaces'
data = json.dumps({'title': 'FLARE_BLOG_KV'}).encode()
req = urllib.request.Request(url, data=data, method='POST', headers=headers)
try:
    resp = urllib.request.urlopen(req, context=ctx)
    d = json.loads(resp.read())
    results['kv_id'] = d['result']['id']
    print(f"[KV] Created: FLARE_BLOG_KV | ID: {results['kv_id']}")
except Exception as e:
    print(f"[KV] Error: {e}")

# Save results
with open(r'c:/Users/USER755413/WorkBuddy/Claw/flare-stack-blog/cf_resources.json', 'w') as f:
    json.dump(results, f, indent=2)

# 4. Create Queue
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/queues'
data = json.dumps({'queue_name': 'blog-queue'}).encode()
req = urllib.request.Request(url, data=data, method='POST', headers=headers)
try:
    resp = urllib.request.urlopen(req, context=ctx)
    d = json.loads(resp.read())
    results['queue_id'] = d['result']['id']
    print(f"[Queue] Created: blog-queue | ID: {results['queue_id']}")
except Exception as e:
    print(f"[Queue] Error: {e}")

print("\nAll resources created:")
print(json.dumps(results, indent=2))
