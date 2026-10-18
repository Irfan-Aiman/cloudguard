import boto3
import json
from datetime import datetime, timedelta, timezone

def scan_cloudtrail_activity(hours_back=24):
    # Initialize the CloudTrail client in your region
    client = boto3.client('cloudtrail', region_name='us-east-2')
    alerts = []

    start_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    print(f"Querying CloudTrail management events over the last {hours_back} hours...")

    try:
        # lookup_events queries the free 90-day event history
        response = client.lookup_events(
            StartTime=start_time,
            MaxResults=50
        )
        events = response.get('Events', [])

        for item in events:
            event_name = item.get('EventName')
            username = item.get('Username', 'Unknown')
            event_time = item.get('EventTime').strftime("%Y-%m-%d %H:%M:%S")

            # Parse the detailed raw JSON inside CloudTrailEvent
            raw_detail = json.loads(item.get('CloudTrailEvent', '{}'))
            source_ip = raw_detail.get('sourceIPAddress', 'Unknown')

            # --- Detection Rules ---

            # Rule 1: Tampering / Defense Evasion
            if event_name in ['StopLogging', 'DeleteTrail', 'UpdateTrail']:
                alerts.append({
                    "event_name": event_name,
                    "severity": "CRITICAL",
                    "actor": username,
                    "source_ip": source_ip,
                    "timestamp": event_time,
                    "threat": "Audit logging disruption detected (Defense Evasion)",
                    "recommendation": "Re-enable CloudTrail immediately and revoke caller credentials."
                })

            # Rule 2: Backdoor Accounts / Persistence
            elif event_name in ['CreateUser', 'CreateAccessKey']:
                alerts.append({
                    "event_name": event_name,
                    "severity": "HIGH",
                    "actor": username,
                    "source_ip": source_ip,
                    "timestamp": event_time,
                    "threat": "IAM credential generation detected (Potential Persistence)",
                    "recommendation": "Verify whether this identity creation was authorized."
                })

            # Rule 3: Firewall Changes
            elif event_name in ['AuthorizeSecurityGroupIngress', 'RevokeSecurityGroupIngress']:
                alerts.append({
                    "event_name": event_name,
                    "severity": "HIGH",
                    "actor": username,
                    "source_ip": source_ip,
                    "timestamp": event_time,
                    "threat": "Firewall ingress/egress rules modified directly",
                    "recommendation": "Inspect security group rules for unauthorized port openings (e.g. 0.0.0.0/0)."
                })

            # Rule 4: Console Login without MFA
            elif event_name == 'ConsoleLogin':
                mfa_used = raw_detail.get('additionalEventData', {}).get('MFAUsed')
                if mfa_used == "No":
                    alerts.append({
                        "event_name": event_name,
                        "severity": "MEDIUM",
                        "actor": username,
                        "source_ip": source_ip,
                        "timestamp": event_time,
                        "threat": "Console sign-in without MFA",
                        "recommendation": "Enforce MFA for all console-enabled IAM identities."
                    })

        return alerts

    except Exception as e:
        print(f"Error accessing CloudTrail: {e}")
        return []

if __name__ == "__main__":
    findings = scan_cloudtrail_activity(hours_back=12)
    print("\n--- CloudTrail Detection Results ---")
    print(json.dumps(findings, indent=2))