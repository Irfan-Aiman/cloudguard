import pytest

def evaluate_cloudtrail_event(event_name):
    """Pure logic validator matching CloudGuard detection rules."""
    if event_name in ['StopLogging', 'DeleteTrail', 'UpdateTrail']:
        return "CRITICAL"
    elif event_name in ['CreateUser', 'CreateAccessKey', 'AuthorizeSecurityGroupIngress', 'RevokeSecurityGroupIngress']:
        return "HIGH"
    elif event_name == 'ConsoleLogin':
        return "MEDIUM"
    return "LOW"

def evaluate_s3_public_block(block_public_acls, block_public_policy):
    """Evaluates S3 bucket access configuration."""
    if not block_public_acls or not block_public_policy:
        return "HIGH"
    return "SECURE"

# --- Tests ---

def test_tampering_defense_evasion():
    assert evaluate_cloudtrail_event("StopLogging") == "CRITICAL"
    assert evaluate_cloudtrail_event("DeleteTrail") == "CRITICAL"

def test_credential_persistence():
    assert evaluate_cloudtrail_event("CreateUser") == "HIGH"
    assert evaluate_cloudtrail_event("CreateAccessKey") == "HIGH"

def test_firewall_ingress_modification():
    assert evaluate_cloudtrail_event("AuthorizeSecurityGroupIngress") == "HIGH"

def test_s3_vulnerable_configuration():
    assert evaluate_s3_public_block(False, True) == "HIGH"
    assert evaluate_s3_public_block(True, False) == "HIGH"
    assert evaluate_s3_public_block(False, False) == "HIGH"

def test_s3_secure_configuration():
    assert evaluate_s3_public_block(True, True) == "SECURE"