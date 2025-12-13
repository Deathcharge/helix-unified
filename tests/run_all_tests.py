#!/usr/bin/env python3
"""
🧪 Master Test Runner - Helix Launch QA Suite
tests/run_all_tests.py

Comprehensive test execution and reporting for Dec 15 launch
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

TEST_SUITES = {
    "HelixSpiral Backend": {
        "file": "tests/test_helixspiral_backend.py",
        "priority": "CRITICAL",
        "coverage": ["auth", "stripe", "spiral_crud", "spiral_execution", "api_endpoints"]
    },
    "MCP Server": {
        "file": "tests/test_mcp_server.py",
        "priority": "CRITICAL",
        "coverage": ["ucf_metrics", "agent_control", "railway_sync", "memory_vault", "mcp_protocol"]
    },
    "Security Middleware": {
        "file": "tests/test_security_middleware.py",
        "priority": "CRITICAL",
        "coverage": ["rate_limiting", "csrf", "error_sanitization", "input_validation", "websocket_validation"]
    },
    "E2E Workflows": {
        "file": "tests/test_e2e_workflows.py",
        "priority": "HIGH",
        "coverage": ["user_onboarding", "agent_control", "consciousness_monitoring", "mcp_integration", "error_recovery"]
    },
    "Consciousness Framework": {
        "file": "tests/test_consciousness_framework.py",
        "priority": "MEDIUM",
        "coverage": ["ucf_calculation", "consciousness_states", "ritual_engine"]
    }
}

# ============================================================================
# TEST RUNNER
# ============================================================================

class TestRunner:
    """Execute all test suites and generate report"""

    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
        self.total_passed = 0
        self.total_failed = 0
        self.total_tests = 0

    def run_test_suite(self, name, config):
        """Run a single test suite"""
        print(f"\n{'='*70}")
        print(f"📊 Running: {name}")
        print(f"   Priority: {config['priority']}")
        print(f"   File: {config['file']}")
        print(f"{'='*70}")

        try:
            # Run pytest with JSON output
            cmd = [
                "pytest",
                config["file"],
                "-v",
                "--tb=short",
                "--json-report",
                f"--json-report-file=/tmp/{name.replace(' ', '_')}_report.json"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            # Parse output
            output_lines = result.stdout.split('\n')
            passed = result.stdout.count(" PASSED")
            failed = result.stdout.count(" FAILED")
            skipped = result.stdout.count(" SKIPPED")

            self.results[name] = {
                "status": "PASSED" if result.returncode == 0 else "FAILED",
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "priority": config["priority"],
                "coverage": config["coverage"]
            }

            self.total_passed += passed
            self.total_failed += failed
            self.total_tests += passed + failed

            # Print summary
            status_symbol = "✅" if result.returncode == 0 else "❌"
            print(f"\n{status_symbol} {name}: {passed} passed, {failed} failed, {skipped} skipped")

            if result.returncode != 0:
                print("STDERR:", result.stderr[:500])

        except subprocess.TimeoutExpired:
            print(f"❌ {name}: TIMEOUT after 5 minutes")
            self.results[name] = {
                "status": "TIMEOUT",
                "priority": config["priority"]
            }
            self.total_failed += 1

        except FileNotFoundError:
            print(f"⚠️  {name}: Test file not found - {config['file']}")
            self.results[name] = {
                "status": "NOT_FOUND",
                "priority": config["priority"]
            }

        except Exception as e:
            print(f"❌ {name}: ERROR - {str(e)[:100]}")
            self.results[name] = {
                "status": "ERROR",
                "error": str(e),
                "priority": config["priority"]
            }
            self.total_failed += 1

    def run_all(self):
        """Run all test suites"""
        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*15 + "🚀 HELIX LAUNCH TEST SUITE 🚀" + " "*24 + "║")
        print("║" + " "*20 + f"Dec 15, 2025 Launch Target" + " "*22 + "║")
        print("╚" + "="*68 + "╝")

        for suite_name, config in TEST_SUITES.items():
            self.run_test_suite(suite_name, config)

        self.print_summary()
        return self.total_failed == 0

    def print_summary(self):
        """Print final test summary"""
        duration = (datetime.now() - self.start_time).total_seconds()

        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*20 + "📋 TEST RESULTS SUMMARY" + " "*25 + "║")
        print("╠" + "="*68 + "╣")

        # Overall stats
        print(f"║ Total Tests Run:     {self.total_tests:<46} ║")
        print(f"║ Passed:              {self.total_passed:<46} ║")
        print(f"║ Failed:              {self.total_failed:<46} ║")
        print(f"║ Pass Rate:           {self._get_pass_rate():<46} ║")
        print(f"║ Duration:            {f'{duration:.1f}s':<46} ║")

        print("╠" + "="*68 + "╣")
        print("║ SUITE BREAKDOWN:".ljust(69) + "║")

        for name, result in self.results.items():
            status = result.get("status", "UNKNOWN")
            symbol = self._get_status_symbol(status)

            if "passed" in result:
                summary = f"{result['passed']}✓ {result['failed']}✗"
                line = f"║ {symbol} {name:<40} {summary:<15} ║"
            else:
                line = f"║ {symbol} {name:<40} {status:<15} ║"

            print(line)

        print("╚" + "="*68 + "╝")

        # Launch readiness
        print("\n📊 LAUNCH READINESS:\n")
        self._check_launch_readiness()

        # Generate detailed report
        self._generate_report()

    def _get_pass_rate(self):
        """Calculate overall pass rate"""
        if self.total_tests == 0:
            return "N/A"
        rate = (self.total_passed / self.total_tests) * 100
        return f"{rate:.1f}%"

    def _get_status_symbol(self, status):
        """Get symbol for status"""
        symbols = {
            "PASSED": "✅",
            "FAILED": "❌",
            "TIMEOUT": "⏱️ ",
            "NOT_FOUND": "❓",
            "ERROR": "⚠️ "
        }
        return symbols.get(status, "❓")

    def _check_launch_readiness(self):
        """Check if system is ready for launch"""
        critical_passed = True
        critical_suites = [s for s, c in TEST_SUITES.items() if c["priority"] == "CRITICAL"]

        for suite in critical_suites:
            if suite in self.results:
                status = self.results[suite]["status"]
                result = "✅ PASS" if status == "PASSED" else f"❌ {status}"
                print(f"  [{result}] {suite}")

                if status != "PASSED":
                    critical_passed = False

        if critical_passed:
            print("\n✅ ALL CRITICAL TESTS PASSED - READY FOR LAUNCH")
            return True
        else:
            print("\n❌ CRITICAL TESTS FAILED - NOT READY FOR LAUNCH")
            print("   Please fix failing tests before deployment")
            return False

    def _generate_report(self):
        """Generate detailed HTML report"""
        report_file = Path("tests/test_report.html")

        html = f"""
        <html>
        <head>
            <title>Helix Launch Test Report</title>
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                .critical {{ font-weight: bold; background-color: #fff3cd; }}
            </style>
        </head>
        <body>
            <h1>🚀 Helix Launch Test Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Target Launch: Dec 15, 2025</p>

            <h2>Test Summary</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Tests</td>
                    <td>{self.total_tests}</td>
                </tr>
                <tr>
                    <td>Passed</td>
                    <td class="pass">{self.total_passed}</td>
                </tr>
                <tr>
                    <td>Failed</td>
                    <td class="fail">{self.total_failed}</td>
                </tr>
                <tr>
                    <td>Pass Rate</td>
                    <td>{self._get_pass_rate()}</td>
                </tr>
            </table>

            <h2>Test Suites</h2>
            <table>
                <tr>
                    <th>Suite</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Results</th>
                </tr>
        """

        for name, result in self.results.items():
            priority = result.get("priority", "UNKNOWN")
            status = result.get("status", "UNKNOWN")
            css_class = "critical" if priority == "CRITICAL" else ""

            if "passed" in result:
                results_str = f"{result['passed']}✓ {result['failed']}✗"
            else:
                results_str = status

            html += f"""
                <tr class="{css_class}">
                    <td>{name}</td>
                    <td>{priority}</td>
                    <td class="{'pass' if status == 'PASSED' else 'fail'}">{status}</td>
                    <td>{results_str}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        report_file.write_text(html)
        print(f"\n📄 Detailed report: {report_file.absolute()}")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Run the test suite"""
    runner = TestRunner()
    all_passed = runner.run_all()

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
