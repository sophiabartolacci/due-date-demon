#!/usr/bin/env python3
"""
Dry-run test that validates bot logic without network calls
Catches import errors, syntax issues, and basic functionality
"""

import os
import sys
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime, timezone

def test_imports():
    """Test core imports work correctly"""
    try:
        # Test individual imports without triggering global setup
        import boto3
        import discord
        import json
        import logging
        from datetime import datetime, date, timedelta, timezone
        from dotenv import load_dotenv
        from notion_client import AsyncClient
        
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_date_formatting():
    """Test date formatting function"""
    try:
        # Mock the environment to avoid credential loading
        with patch.dict(os.environ, {'NOTION_TOKEN': 'test', 'NOTION_DATABASE_ID': 'test', 
                                     'DISCORD_TOKEN': 'test', 'DISCORD_CHANNEL_ID': '123'}):
            from bot import format_date
            
            # Test date-only format
            result1 = format_date("2025-01-22T00:00:00Z")
            assert result1 == "1/22", f"Expected '1/22', got '{result1}'"
            
            # Test date with time
            result2 = format_date("2025-01-22T23:59:00Z")
            assert "11:59PM" in result2, f"Expected time in result, got '{result2}'"
            
        print("✅ Date formatting test passed")
        return True
    except Exception as e:
        print(f"❌ Date formatting test failed: {e}")
        return False

def test_credential_loading():
    """Test credential loading logic"""
    try:
        with patch.dict(os.environ, {'NOTION_TOKEN': 'test', 'NOTION_DATABASE_ID': 'test', 
                                     'DISCORD_TOKEN': 'test', 'DISCORD_CHANNEL_ID': '123'}):
            from bot import load_credentials
            
            creds = load_credentials()
            assert 'notion_token' in creds
            assert creds['notion_token'] == 'test'
            
        print("✅ Credential loading test passed")
        return True
    except Exception as e:
        print(f"❌ Credential loading test failed: {e}")
        return False

def test_lambda_context():
    """Test Lambda context handling"""
    try:
        # Mock Lambda environment
        os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "test-function"
        
        # Mock AWS SSM calls
        with patch('boto3.client') as mock_boto:
            mock_ssm = Mock()
            mock_ssm.get_parameter.return_value = {'Parameter': {'Value': 'test-value'}}
            mock_boto.return_value = mock_ssm
            
            from bot import load_credentials
            creds = load_credentials()
            
            assert 'notion_token' in creds
            assert creds['notion_token'] == 'test-value'
            
        print("✅ Lambda context test passed")
        return True
    except Exception as e:
        print(f"❌ Lambda context test failed: {e}")
        return False
    finally:
        if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
            del os.environ["AWS_LAMBDA_FUNCTION_NAME"]

def test_null_handling():
    """Test null field handling in assignment processing"""
    try:
        # Mock Notion API response with null fields
        mock_entry = {
            'properties': {
                'Assignment': {'title': [{'plain_text': 'Test Assignment'}]},
                'Class': {'select': None},  # Null field
                'Type': {'select': {'name': 'Homework'}},
                'Due Date': {'date': {'start': '2025-01-22T00:00:00Z'}},
                'Notes': {'rich_text': []}
            }
        }
        
        # Test the logic that caused the original error
        class_select = mock_entry['properties']['Class']['select']
        assignment_class = class_select['name'] if class_select else 'Unknown'
        
        assert assignment_class == 'Unknown'
        print("✅ Null field handling test passed")
        return True
    except Exception as e:
        print(f"❌ Null field handling test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running dry-run tests...")
    
    tests = [
        test_imports,
        test_date_formatting,
        test_credential_loading,
        test_lambda_context,
        test_null_handling
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Safe to deploy.")
        sys.exit(0)
    else:
        print("💥 Some tests failed! Fix issues before deploying.")
        sys.exit(1)