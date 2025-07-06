import requests

token= "ff34fc844d3d44848c65f1ad3a4ce4fd93d3bff64fc"
proxyurl= f"http://{token}:@proxy.scrape.do:8080"
proxies ={
    "http": proxyurl,
    "https": proxyurl
}

def fetch_and_save(url,path):
    r= requests.get(url,verify=False,proxies=proxies)
    with open(path,"w") as f:
        f.write(r.text)
    
for i in range(2018, 2026):
    url= f"https://iplt20stats.com/ipl-{i}-auction"
    fetch_and_save(url,f"ipl_{i}_auction.html")
