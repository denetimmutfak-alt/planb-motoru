#!/usr/bin/env python3
"""
Health Check Script for Docker Containers
"""
import requests
import sys
import os

def check_health():
    try:
        # Core API health check
        response = requests.get(
            "http://localhost:8000/health", 
            timeout=5
        )
        
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("status") == "healthy":
                print("✅ Core API is healthy")
                return True
            else:
                print(f"❌ Core API unhealthy: {health_data}")
                return False
        else:
            print(f"❌ Core API returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)
