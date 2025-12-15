from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime
from typing import Optional, Dict, List
import time
import os

app = Flask(__name__)

# ==================== CONFIGURATION ====================
# Try multiple ways to get the API key
API_KEY = os.environ.get('TRACKING_API_KEY') or os.environ.get('17TRACK_API_KEY') or os.getenv('TRACKING_API_KEY')

BASE_URL = "https://api.17track.net"

print("=" * 60)
print("BoxBounty Web App Starting")
print("=" * 60)
if API_KEY:
    print(f"✓ API Key found: {API_KEY[:10]}...")
else:
    print("✗ WARNING: No API key found!")
    print("Set environment variable: TRACKING_API_KEY=your_key")
print("=" * 60)

# ==================== API CLIENT ====================
class TrackingAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # IMPORTANT: The header name must be exactly '17token' (lowercase)
        self.headers = {
            '17token': api_key,
            'Content-Type': 'application/json'
        }

    def register_tracking(self, tracking_number: str, carrier_code: Optional[str] = None) -> Dict:
        """Register a tracking number with 17Track"""
        url = f"{BASE_URL}/track/v2.4/register"

        data = [{
            "number": tracking_number.strip().upper()
        }]

        if carrier_code:
            data[0]["carrier"] = carrier_code

        try:
            print(f"[DEBUG] Registering: {tracking_number}")
            print(f"[DEBUG] URL: {url}")
            print(f"[DEBUG] Headers: {{'17token': '{self.api_key[:10]}...', 'Content-Type': 'application/json'}}")
            print(f"[DEBUG] Data: {json.dumps(data)}")
            
            response = requests.post(url, headers=self.headers, json=data, timeout=15)
            
            print(f"[DEBUG] Response Status: {response.status_code}")
            print(f"[DEBUG] Response Body: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': result.get('code') == 0,
                'message': result.get('data', {}).get('message', ''),
                'data': result
            }
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] HTTP Error: {e}")
            print(f"[ERROR] Response: {e.response.text if hasattr(e, 'response') else 'No response'}")
            return {'success': False, 'message': f'API Error: {str(e)}', 'data': None}
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error: {e}")
            return {'success': False, 'message': f'Network error: {str(e)}', 'data': None}
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return {'success': False, 'message': str(e), 'data': None}

    def get_tracking_info(self, tracking_number: str) -> Dict:
        """Get tracking information for a package"""
        url = f"{BASE_URL}/track/v2.4/gettrackinfo"

        data = [{
            "number": tracking_number.strip().upper()
        }]

        try:
            print(f"[DEBUG] Getting tracking info for: {tracking_number}")
            response = requests.post(url, headers=self.headers, json=data, timeout=15)
            
            print(f"[DEBUG] Tracking Response Status: {response.status_code}")
            print(f"[DEBUG] Tracking Response: {response.text[:500]}...")  # First 500 chars
            
            response.raise_for_status()
            result = response.json()

            if result.get('code') == 0:
                accepted = result.get('data', {}).get('accepted', [])
                rejected = result.get('data', {}).get('rejected', [])
                not_found = result.get('data', {}).get('not_found', [])

                print(f"[DEBUG] Accepted: {len(accepted)}, Rejected: {len(rejected)}, Not Found: {len(not_found)}")

                if accepted and len(accepted) > 0:
                    return {'success': True, 'data': accepted[0], 'message': 'Found'}
                elif rejected:
                    return {'success': False, 'data': None, 'message': 'Tracking number rejected'}
                elif not_found:
                    return {'success': False, 'data': None,
                            'message': 'Tracking number not found. It may take 24-48 hours for new shipments to appear.'}
                else:
                    return {'success': False, 'data': None, 'message': 'No tracking data available yet'}
            else:
                error_msg = result.get('message', 'Unknown API error')
                return {'success': False, 'data': None, 'message': f'API Error: {error_msg}'}

        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] HTTP Error: {e}")
            return {'success': False, 'data': None, 'message': f'API Error: {str(e)}'}
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error: {e}")
            return {'success': False, 'data': None, 'message': f'Network error: {str(e)}'}
        except Exception as e:
            print(f"[ERROR] Tracking error: {e}")
            return {'success': False, 'data': None, 'message': str(e)}


# ==================== FLASK ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track_package():
    tracking_number = request.json.get('tracking_number', '').strip()
    
    if not tracking_number:
        return jsonify({'success': False, 'message': 'Please enter a tracking number'})
    
    if not API_KEY:
        return jsonify({
            'success': False,
            'message': 'API key not configured. Please set the TRACKING_API_KEY environment variable.'
        })
    
    print(f"\n{'='*60}")
    print(f"New tracking request: {tracking_number}")
    print(f"{'='*60}\n")
    
    # Initialize API
    api = TrackingAPI(API_KEY)
    
    # Register tracking number first
    reg_result = api.register_tracking(tracking_number)
    
    if not reg_result['success']:
        error_msg = reg_result['message']
        
        # Check if it's an auth error
        if '401' in error_msg or 'Unauthorized' in error_msg:
            error_msg = "API Authentication Failed. Please check your API key is correct."
        
        return jsonify({
            'success': False,
            'message': f"Failed to register: {error_msg}"
        })
    
    # Wait for the tracking system to process
    time.sleep(2)
    
    # Get tracking info - try up to 3 times
    tracking_result = None
    for attempt in range(3):
        print(f"[INFO] Attempt {attempt + 1} to get tracking info...")
        tracking_result = api.get_tracking_info(tracking_number)
        
        if tracking_result['success']:
            break
        
        if attempt < 2:
            time.sleep(2)
    
    if tracking_result['success']:
        # Format the data for the frontend
        tracking_data = tracking_result['data']
        track_info = tracking_data.get('track_info', {})
        
        # Extract carrier information
        tracking_providers = track_info.get('tracking', {}).get('providers', [])
        carrier_name = 'Unknown Carrier'
        service_type = ''
        
        if tracking_providers:
            provider_info = tracking_providers[0].get('provider', {})
            carrier_name = provider_info.get('name', 'Unknown Carrier')
            service_type = tracking_providers[0].get('service_type', '')
        
        # Extract status information
        latest_status = track_info.get('latest_status', {})
        status_text = latest_status.get('status', 'Unknown')
        sub_status = latest_status.get('sub_status', '')
        
        status_display = status_text
        if sub_status and sub_status != status_text:
            status_display = sub_status.replace('_', ' ').title()
        
        # Extract route information
        shipping_info = track_info.get('shipping_info', {})
        shipper_addr = shipping_info.get('shipper_address', {})
        recipient_addr = shipping_info.get('recipient_address', {})
        
        origin = shipper_addr.get('country', 'Unknown')
        destination = recipient_addr.get('country', 'Unknown')
        
        # Extract timeline events
        events = []
        if tracking_providers:
            events = tracking_providers[0].get('events', [])
        
        # Format events for display
        formatted_events = []
        for event in events:
            time_iso = event.get('time_iso', '')
            try:
                dt = datetime.fromisoformat(time_iso)
                formatted_time = dt.strftime("%B %d, %Y at %I:%M %p")
            except:
                formatted_time = time_iso or 'Unknown time'
            
            formatted_events.append({
                'time': formatted_time,
                'location': event.get('location', ''),
                'description': event.get('description', ''),
                'is_latest': False
            })
        
        # Mark the first event as latest
        if formatted_events:
            formatted_events[0]['is_latest'] = True
        
        # Get time metrics
        time_metrics = track_info.get('time_metrics', {})
        days_transit = time_metrics.get('days_of_transit', 0)
        
        # Get last update time
        latest_event = track_info.get('latest_event', {})
        last_update = ''
        time_iso = latest_event.get('time_iso', '')
        if time_iso:
            try:
                dt = datetime.fromisoformat(time_iso)
                last_update = dt.strftime("%B %d, %Y at %I:%M %p")
            except:
                pass
        
        print(f"[SUCCESS] Tracking data retrieved successfully")
        
        return jsonify({
            'success': True,
            'data': {
                'tracking_number': tracking_data.get('number', 'N/A'),
                'carrier_name': carrier_name,
                'service_type': service_type,
                'status': status_display,
                'origin': origin,
                'destination': destination,
                'days_transit': days_transit,
                'last_update': last_update,
                'events': formatted_events
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': tracking_result['message']
        })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'api_key_configured': bool(API_KEY)
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    if not API_KEY:
        print("\n" + "!"*60)
        print("WARNING: No API key found!")
        print("Set it with: export TRACKING_API_KEY=your_key_here")
        print("Or in Docker: -e TRACKING_API_KEY=your_key_here")
        print("!"*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
