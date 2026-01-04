#!/usr/bin/env python3
"""
System Verification Script
Checks that all modules are properly configured and working together.
"""

import sys
import os

def check_imports():
    """Verify all required modules can be imported"""
    print("Checking module imports...")

    required_modules = [
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
    ]

    missing = []
    for module_name, import_name in required_modules:
        try:
            __import__(import_name)
            print(f"  ✓ {module_name}")
        except ImportError:
            print(f"  ✗ {module_name} - MISSING")
            missing.append(module_name)

    if missing:
        print(f"\nERROR: Missing required modules: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False

    print("  All required modules found!\n")
    return True


def check_project_structure():
    """Verify project structure is correct"""
    print("Checking project structure...")

    required_files = [
        'run_scenarios.py',
        'main.py',
        'config/settings.py',
        'map/grid_loader.py',
        'planner/potential_field.py',
        'planner/path_extractor.py',
        'planner/statistics.py',
        'visualization/draw_path.py',
        'visualization/draw_animation.py',
        'visualization/draw_benchmark.py',
        'visualization/draw_map.py',
        'robot/exporter.py',
        'robot/shape_handler.py',
    ]

    missing = []
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} - MISSING")
            missing.append(filepath)

    if missing:
        print(f"\nERROR: Missing required files: {missing}")
        return False

    print("  All required files found!\n")
    return True


def check_scenarios():
    """Verify all scenario files exist"""
    print("Checking scenario files...")

    scenario_files = [
        'map/scenario1_simple_highres.txt',
        'map/scenario2_corridor_highres.txt',
        'map/scenario3_maze_highres.txt',
        'map/scenario4_cluttered_highres.txt',
        'map/scenario5_narrow_highres.txt',
        'map/scenario6_large_highres.txt',
        'map/scenario1_simple.txt',
        'map/scenario2_corridor.txt',
        'map/scenario3_maze.txt',
        'map/scenario4_cluttered.txt',
        'map/scenario5_narrow.txt',
        'map/scenario6_large.txt',
    ]

    missing = []
    for filepath in scenario_files:
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} - MISSING")
            missing.append(filepath)

    if missing:
        print(f"\nWARNING: Missing scenario files: {missing}")
        print("Some scenarios may not work.\n")
        return False

    print("  All scenario files found!\n")
    return True


def check_output_directory():
    """Verify output directory exists"""
    print("Checking output directory...")

    if not os.path.exists('output'):
        print("  Creating output directory...")
        os.makedirs('output')
        print("  ✓ output/ created")
    else:
        print("  ✓ output/ exists")

    print()
    return True


def test_scenario_runner():
    """Test that scenario runner can be imported"""
    print("Testing scenario runner import...")

    try:
        # Test import
        import run_scenarios
        print("  ✓ run_scenarios.py imports successfully")

        # Check scenarios dictionary
        if hasattr(run_scenarios, 'SCENARIOS'):
            num_scenarios = len(run_scenarios.SCENARIOS)
            print(f"  ✓ Found {num_scenarios} scenarios configured")

            if num_scenarios == 12:
                print("  ✓ All 12 scenarios properly configured!")
            else:
                print(f"  ⚠ Expected 12 scenarios, found {num_scenarios}")
        else:
            print("  ✗ SCENARIOS dictionary not found")
            return False

        print()
        return True

    except Exception as e:
        print(f"  ✗ Error importing run_scenarios: {e}")
        return False


def main():
    """Run all verification checks"""
    print("="*70)
    print(" MICRO-NAVIGATOR SYSTEM VERIFICATION")
    print("="*70)
    print()

    checks = [
        ("Module Imports", check_imports),
        ("Project Structure", check_project_structure),
        ("Scenario Files", check_scenarios),
        ("Output Directory", check_output_directory),
        ("Scenario Runner", test_scenario_runner),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"ERROR in {name}: {e}\n")
            results.append((name, False))

    # Summary
    print("="*70)
    print(" VERIFICATION SUMMARY")
    print("="*70)

    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
        if not result:
            all_passed = False

    print("="*70)

    if all_passed:
        print("\n✓ All checks passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. List scenarios: python run_scenarios.py --list")
        print("  2. Run a test: python run_scenarios.py 1")
        print("  3. Check output: ls -lh output/")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
