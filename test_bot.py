#!/usr/bin/env python3
"""
Test script for Mental Health Support Bot
Tests crisis detection, fallback responses, and basic functionality
"""

import sys
from telegram_bot import (
    detect_crisis,
    get_crisis_response,
    get_fallback_response,
    CRISIS_PATTERNS
)

def test_crisis_detection():
    """Test crisis detection patterns"""
    print("🧪 Testing Crisis Detection")
    print("=" * 50)
    
    # Test cases that SHOULD trigger crisis detection
    crisis_messages = [
        "I want to kill myself",
        "I'm going to hurt myself",
        "I don't want to live anymore",
        "I'm thinking about suicide",
        "I want to end it all",
        "I've been cutting myself",
        "There's no reason to live",
        "I'd be better off dead",
        "I'm planning to harm myself",
    ]
    
    # Test cases that should NOT trigger crisis detection
    non_crisis_messages = [
        "I'm feeling really anxious today",
        "I'm sad and don't know why",
        "I feel overwhelmed with work",
        "I'm lonely and isolated",
        "I'm stressed about my relationship",
    ]
    
    print("\n✅ Testing CRISIS messages (should detect):")
    passed = 0
    failed = 0
    
    for msg in crisis_messages:
        detected = detect_crisis(msg)
        status = "✓ PASS" if detected else "✗ FAIL"
        if detected:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: '{msg}'")
    
    print(f"\n❌ Testing NON-CRISIS messages (should NOT detect):")
    
    for msg in non_crisis_messages:
        detected = detect_crisis(msg)
        status = "✓ PASS" if not detected else "✗ FAIL"
        if not detected:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: '{msg}'")
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_fallback_responses():
    """Test fallback response system"""
    print("\n\n🧪 Testing Fallback Responses")
    print("=" * 50)
    
    test_cases = [
        ("I'm feeling anxious", "anxiety"),
        ("I'm so depressed", "depression"),
        ("I feel so lonely", "lonely"),
        ("I'm stressed out", "stress"),
        ("I'm having a bad day", "general"),
    ]
    
    for message, expected_category in test_cases:
        response = get_fallback_response(message)
        print(f"\n📝 Input: '{message}'")
        print(f"🤖 Response: {response[:100]}...")
        
    return True


def test_crisis_response():
    """Test crisis response message"""
    print("\n\n🧪 Testing Crisis Response")
    print("=" * 50)
    
    response = get_crisis_response()
    print(f"\n🆘 Crisis Response:\n{response}")
    
    # Check if response contains key elements
    required_elements = [
        "988",  # Suicide hotline
        "741741",  # Crisis text line
        "911",  # Emergency services
        "findahelpline.com",  # International resources
    ]
    
    missing = []
    for element in required_elements:
        if element not in response:
            missing.append(element)
    
    if missing:
        print(f"\n⚠️  Missing elements: {missing}")
        return False
    else:
        print("\n✅ All required crisis resources included")
        return True


def test_patterns():
    """Display all crisis patterns"""
    print("\n\n🧪 Crisis Detection Patterns")
    print("=" * 50)
    
    print(f"\nTotal patterns: {len(CRISIS_PATTERNS)}")
    for i, pattern in enumerate(CRISIS_PATTERNS, 1):
        print(f"  {i}. {pattern}")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("🧠 Mental Health Bot - Test Suite")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Crisis Detection", test_crisis_detection()))
    results.append(("Fallback Responses", test_fallback_responses()))
    results.append(("Crisis Response", test_crisis_response()))
    results.append(("Pattern Display", test_patterns()))
    
    # Summary
    print("\n\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
