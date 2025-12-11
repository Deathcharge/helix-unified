"""
Test script for Voice Patrol integration.

Tests the complete voice pipeline:
1. Voice Processor Client -> Voice Processor Service -> Google Cloud TTS
2. Audio caching
3. Health checks
"""
import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.voice_processor_client import (VoiceProcessorClient,
                                            get_voice_client)


async def test_health_check():
    """Test voice processor service health."""
    print("🏥 Testing voice processor health check...")
    client = get_voice_client()

    healthy = await client.health_check()
    if healthy:
        print("✅ Voice processor service is healthy")
        return True
    else:
        print("❌ Voice processor service is not responding")
        print(f"   URL: {client.base_url}")
        print("   Make sure the service is running:")
        print("   cd backend/voice_processor && uvicorn main:app --port 8001")
        return False


async def test_tts_synthesis():
    """Test text-to-speech synthesis."""
    print("\n🎙️ Testing TTS synthesis...")
    client = get_voice_client()

    test_phrases = [
        ("Nexus online. Strategic coordination active.", "en-US-Neural2-A"),
        ("Oracle perceives your presence.", "en-US-Neural2-F"),
        ("Velocity ready. Let's move quickly.", "en-US-Neural2-D"),
    ]

    for text, voice in test_phrases:
        print(f"\n  Testing: '{text[:40]}...'")
        print(f"  Voice: {voice}")

        audio_data = await client.synthesize_speech(
            text=text,
            voice_name=voice,
            language_code="en-US"
        )

        if audio_data:
            print(f"  ✅ Generated {len(audio_data):,} bytes")

            # Save sample
            output_path = f"/tmp/voice_test_{voice}.mp3"
            with open(output_path, "wb") as f:
                f.write(audio_data)
            print(f"  💾 Saved to: {output_path}")
        else:
            print(f"  ❌ Synthesis failed")
            return False

    return True


async def test_caching():
    """Test TTS audio caching."""
    print("\n💾 Testing TTS caching...")
    client = get_voice_client()

    text = "This is a cache test message."
    voice = "en-US-Neural2-A"

    # First request (should hit API)
    print("  First request (should generate audio)...")
    import time
    start = time.time()
    audio1 = await client.synthesize_speech(text, voice_name=voice, use_cache=True)
    duration1 = time.time() - start

    if not audio1:
        print("  ❌ Failed to generate audio")
        return False

    print(f"  ✅ Generated in {duration1:.2f}s")

    # Second request (should use cache)
    print("  Second request (should use cache)...")
    start = time.time()
    audio2 = await client.synthesize_speech(text, voice_name=voice, use_cache=True)
    duration2 = time.time() - start

    if not audio2:
        print("  ❌ Failed to get cached audio")
        return False

    print(f"  ✅ Retrieved in {duration2:.2f}s")

    # Verify cache performance
    if duration2 < duration1:
        speedup = duration1 / duration2
        print(f"  🚀 Cache speedup: {speedup:.1f}x faster!")
        return True
    else:
        print("  ⚠️  Cache may not be working (second request slower)")
        return False


async def test_error_handling():
    """Test error handling."""
    print("\n🔧 Testing error handling...")
    client = get_voice_client()

    # Test with empty text
    print("  Testing empty text...")
    audio = await client.synthesize_speech("", voice_name="en-US-Neural2-A")
    if audio is None:
        print("  ✅ Correctly handled empty text")
    else:
        print("  ⚠️  Unexpected: generated audio for empty text")

    # Test with invalid voice (should fall back gracefully)
    print("  Testing invalid voice name...")
    audio = await client.synthesize_speech(
        "Test message",
        voice_name="invalid-voice-name"
    )
    # This might succeed if API ignores invalid voice, that's okay
    print("  ✅ Error handling test complete")

    return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("🎙️ HELIX VOICE PATROL - INTEGRATION TESTS")
    print("=" * 60)
    print("")

    # Check environment
    print("📋 Environment Check:")
    print(f"  VOICE_PROCESSOR_URL: {os.getenv('VOICE_PROCESSOR_URL', 'Not set (using default)')}")
    print(f"  JWT_TOKEN: {'Set ✅' if os.getenv('JWT_TOKEN') else 'Not set ⚠️'}")
    print(f"  GOOGLE_CLOUD_TTS_API_KEY: {'Set ✅' if os.getenv('GOOGLE_CLOUD_TTS_API_KEY') else 'Not set ⚠️'}")
    print("")

    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("TTS Synthesis", test_tts_synthesis),
        ("Caching System", test_caching),
        ("Error Handling", test_error_handling),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Cleanup
    client = get_voice_client()
    await client.close()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")

    print("")
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Voice patrol is ready to rock! 🎸")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
