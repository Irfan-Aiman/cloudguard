# CloudGuard: AWS Security Posture & Activity Monitoring Platform

CloudGuard is a lightweight Cloud Security Posture Management (CSPM) and threat detection tool designed to identify misconfigurations across core AWS services and monitor suspicious management activity using AWS CloudTrail.

## Architecture

\`\`\`text
                         AWS ACCOUNT
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
            IAM               S3              EC2
             │                │         (Security Groups)
             └────────────────┼────────────────┘
                              │
                              ▼
                         CloudTrail
                              │
                              ▼
                     Python Engine (Boto3)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
       Posture Scanner               Activity Monitor
       - S3 Public Blocks            - Unauthorized Ingress
       - Encryption & Versioning     - Defense Evasion
              │                               │
              └───────────────┬───────────────┘
                              ▼
                 Streamlit Security Console
\`\`\`

## Key Capabilities

1. **Posture Assessment (CSPM Engine)**
   - **S3 Storage:** Scans buckets for missing public access blocks, disabled server-side encryption, and versioning protection.
   - **Network Exposure:** Identifies security groups allowing open inbound traffic (`0.0.0.0/0`) on sensitive administrative ports (SSH 22, RDP 3389).

2. **Runtime Activity Detection**
   - **Defense Evasion:** Identifies attempts to disable or alter audit trails (`StopLogging`, `DeleteTrail`).
   - **Identity Persistence:** Detects privileged IAM identity and credential generation (`CreateUser`, `CreateAccessKey`).
   - **Network Tampering:** Flags real-time firewall ingress modifications (`AuthorizeSecurityGroupIngress`).

## Risk Model

| Severity | Definition | Example Findings |
|---|---|---|
| **CRITICAL** | Direct exposure or audit blinding | Trail logging disabled, public bucket containing sensitive assets |
| **HIGH** | Significant attack surface expansion | Unrestricted ingress on administrative ports, IAM persistence actions |
| **MEDIUM** | Missing baseline security controls | Bucket default encryption disabled, console login without MFA |
| **LOW** | Operational hygiene risks | Bucket versioning disabled |

## Installation & Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/<your-username>/cloudguard.git
   cd cloudguard
   \`\`\`

2. Create a virtual environment and install dependencies:
   \`\`\`bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   \`\`\`

3. Configure AWS CLI credentials:
   \`\`\`bash
   aws configure
   # Set default region to us-east-2
   \`\`\`

4. Run the automated test suite:
   \`\`\`bash
   pytest -v
   \`\`\`

5. Launch the security dashboard:
   \`\`\`bash
   streamlit run dashboard/app.py
   \`\`\`

## Security Design

- **Least Privilege:** The scanner executes using dedicated read-only identities (`SecurityAudit` permissions) and requires no administrative write access.
- **Credential Safety:** Uses AWS credential provider chains via Boto3; zero static secrets or tokens are stored in the codebase.
\`\`\`