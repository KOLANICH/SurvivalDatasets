from .http import get as httpGet
import json

GH_API_BASE = "https://api.github.com/"
GH_RAW_BASE = "https://raw.githubusercontent.com/"

def gitHubSearchPath(repoName, path=None, ext=None):
    parts = ["repo:" + repoName]
    
    if path:
        parts.append("path:" + path)
    if ext:
        parts.append("ext:" + ext)
    
    return json.loads(httpGet(GH_API_BASE + "search/code", {"q": " ".join(parts)}))
