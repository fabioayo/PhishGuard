import os
import requests

API_KEY = os.getenv("VT_API_KEY")

BASE_URL = "https://www.virustotal.com/api/v3/urls"

class VirusTotalScanner:
    
    def submit_url(self,url):
        
        headers={
            "x-apikey": API_KEY
        }
        
        data= {
            "url":url
        }
        
        response = requests.post(
            BASE_URL,
            headers=headers,
            data=data,
            timeout=15
            )
        
        response.raise_for_status()
        
        print ("VirusTotal status:", response.status_code)
        # print ("Status:", response.status_code)
        # print ("URL:", response.url)
        # print ("Headers:", response.headers)
        # print ("Body", response.text)
        
        return response.json()
    
    def get_analysis(self, analysis_id):
        
        headers={
            "x-apikey": API_KEY
        }
        
        response = requests.get((
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"),
            headers=headers, timeout=15
        )
        response.raise_for_status()
        return response.json()
    
    def parse_results(self, result):
        
        stats = result["data"]["attributes"]["stats"]
        
        return {
            "malicious" : stats["malicious"],
            "suspicious": stats["suspicious"],
            "harmless": stats["harmless"],
            "undetected": stats["undetected"]
        }
        
    def scan_url(self,url):
        submit = self.submit_url(url)
        analysis_id = submit["data"]["id"]
        result = self.get_analysis(analysis_id)
        return self.parse_results(result)
    
    



