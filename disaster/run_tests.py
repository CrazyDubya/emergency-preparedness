#!/usr/bin/env python3
"""
Test runner for Emergency Preparedness System

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py -v           # Verbose output
    python run_tests.py -k security  # Run only security tests
    python run_tests.py --coverage   # Run with coverage report
"""

import sys
import os
import unittest
import argparse
from pathlib import Path

# Add the project root and core to path (core holds emergency_drill_simulator, exceptions, etc.)
PROJECT_ROOT = Path(__file__).parent
CORE_DIR = PROJECT_ROOT / "core"
sys.path.insert(0, str(CORE_DIR))
sys.path.insert(0, str(PROJECT_ROOT))


def discover_tests(test_pattern: str = "test_*.py") -> unittest.TestSuite:
    """Discover all tests in the tests directory"""
    tests_dir = PROJECT_ROOT / "tests"

    if not tests_dir.exists():
        print(f"Warning: Tests directory not found at {tests_dir}")
        return unittest.TestSuite()

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(tests_dir),
        pattern=test_pattern,
        top_level_dir=str(PROJECT_ROOT)
    )

    return suite


def run_tests(verbosity: int = 2,
             pattern: str = None,
             failfast: bool = False) -> unittest.TestResult:
    """
    Run the test suite

    Args:
        verbosity: Output verbosity (0=quiet, 1=normal, 2=verbose)
        pattern: Only run tests matching this pattern
        failfast: Stop on first failure

    Returns:
        TestResult object
    """
    # Discover tests
    if pattern:
        test_pattern = f"test_*{pattern}*.py"
    else:
        test_pattern = "test_*.py"

    suite = discover_tests(test_pattern)

    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        failfast=failfast
    )

    print(f"\n{'='*70}")
    print("Emergency Preparedness System - Test Suite")
    print(f"{'='*70}\n")

    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*70}")
    print("Test Summary")
    print(f"{'='*70}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n[PASS] All tests passed!")
    else:
        print("\n[FAIL] Some tests failed.")

        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")

        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")

    return result


def run_with_coverage(verbosity: int = 2, pattern: str = None):
    """Run tests with coverage reporting"""
    try:
        import coverage
    except ImportError:
        print("Coverage not installed. Install with: pip install coverage")
        return run_tests(verbosity, pattern)

    # Start coverage
    cov = coverage.Coverage(
        source=[str(PROJECT_ROOT)],
        omit=[
            "*/tests/*",
            "*/__pycache__/*",
            "*/run_tests.py"
        ]
    )
    cov.start()

    # Run tests
    result = run_tests(verbosity, pattern)

    # Stop coverage and generate report
    cov.stop()
    cov.save()

    print(f"\n{'='*70}")
    print("Coverage Report")
    print(f"{'='*70}\n")

    cov.report()

    # Generate HTML report
    html_dir = PROJECT_ROOT / "htmlcov"
    cov.html_report(directory=str(html_dir))
    print(f"\nHTML coverage report: {html_dir / 'index.html'}")

    return result


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run Emergency Preparedness System tests"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=1,
        help="Increase output verbosity (use -vv for more)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output"
    )

    parser.add_argument(
        "-k", "--pattern",
        type=str,
        help="Only run tests matching pattern"
    )

    parser.add_argument(
        "-f", "--failfast",
        action="store_true",
        help="Stop on first failure"
    )

    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage reporting"
    )

    args = parser.parse_args()

    # Determine verbosity
    if args.quiet:
        verbosity = 0
    else:
        verbosity = min(args.verbose + 1, 3)

    # Run tests
    if args.coverage:
        result = run_with_coverage(verbosity, args.pattern)
    else:
        result = run_tests(verbosity, args.pattern, args.failfast)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
