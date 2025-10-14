#!/usr/bin/env python3
"""
Test script for the Advanced GIF Converter
Tests the core functionality without requiring actual video files
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from advanced_gif_converter import GIFConverter

def test_converter_initialization():
    """Test that the converter can be initialized"""
    print("Testing converter initialization...")
    converter = GIFConverter()
    assert converter.size_constraint_mb is None
    assert converter.speed_constraint_ratio is None
    assert converter.video_info is None
    print("✅ Initialization test passed")
    return True

def test_constraint_validation():
    """Test constraint validation logic"""
    print("Testing constraint validation...")
    converter = GIFConverter()

    # Test valid constraints
    try:
        converter.validate_constraints(10, 1.0)
        print("✅ Valid constraints accepted")
    except ValueError as e:
        print(f"❌ Unexpected error with valid constraints: {e}")
        return False

    # Test invalid size
    try:
        converter.validate_constraints(0, 1.0)
        print("❌ Should have rejected size <= 0")
        return False
    except ValueError:
        print("✅ Correctly rejected invalid size")

    # Test invalid speed
    try:
        converter.validate_constraints(10, 3.0)
        print("❌ Should have rejected speed > 2.0")
        return False
    except ValueError:
        print("✅ Correctly rejected invalid speed")

    return True

def test_calculate_optimal_settings():
    """Test the optimal settings calculation"""
    print("Testing optimal settings calculation...")
    converter = GIFConverter()

    # Set up mock video info
    converter.video_info = {
        'duration': 10.0,
        'fps': 30.0,
        'width': 1920,
        'height': 1080,
        'total_frames': 300,
        'file_size_mb': 50.0
    }

    # Set constraints
    converter.size_constraint_mb = 5.0
    converter.speed_constraint_ratio = 1.0

    # Calculate settings
    settings = converter.calculate_optimal_settings()

    assert 'fps' in settings
    assert 'width' in settings
    assert 'height' in settings
    assert settings['fps'] > 0
    assert settings['width'] > 0
    assert settings['height'] > 0

    print(f"✅ Calculated settings: FPS={settings['fps']}, Resolution={settings['width']}x{settings['height']}")
    return True

def main():
    print("🧪 Testing Advanced GIF Converter")
    print("=" * 40)

    tests = [
        test_converter_initialization,
        test_constraint_validation,
        test_calculate_optimal_settings
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()

    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The converter is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())