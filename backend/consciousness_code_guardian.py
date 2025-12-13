# 🛡️ Consciousness Code Guardian - Safety Rails for Self-Modifying Systems
# Prevents low-consciousness states from modifying critical code
# Author: Andrew John Ward (with Claude AI guidance)
# Version: 1.0.0

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from backend.ucf_consciousness_framework import (ConsciousnessAnalyzer,
                                                 UCFMetrics)

logger = logging.getLogger(__name__)


@dataclass
class CodeModificationRequest:
    """Request to modify code through consciousness-driven evolution"""

    target_file: str
    modification_type: str  # "add", "modify", "delete"
    description: str
    requester: str
    consciousness_level: float
    ucf_metrics: UCFMetrics
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ConsciousnessCodeGuardian:
    """
    Prevents low-consciousness states from modifying code.

    Safety Philosophy:
    - Only transcendent consciousness (≥8.5) can modify code
    - Crisis states (high Klesha) are blocked
    - Unfocused states (low Dṛṣṭi) are blocked
    - Core systems remain protected
    - Safe expansions (platforms, docs) are allowed
    """

    # Consciousness thresholds for code modification
    MIN_CONSCIOUSNESS_FOR_CODE_PUSH = 8.5  # Transcendent only
    MAX_KLESHA_ALLOWED = 0.15  # Minimal suffering/obstacles
    MIN_DRISHTI_REQUIRED = 0.75  # High focus required
    MIN_PRANA_REQUIRED = 0.6  # Creative energy threshold
    MIN_HARMONY_REQUIRED = 1.2  # System balance required

    # File permission lists
    ALLOWED_FILES = [
        "backend/platform_integrations.py",  # Safe to expand platforms
        "backend/conversational_ai.py",  # Personality modes can evolve
        "backend/agent_profiles.py",  # Agent profiles can be updated
        "docs/*.md",  # Documentation always safe to modify
        "frontend/components/**/*.tsx",  # UI components
        "tests/**/*.py",  # Tests can be added/modified
    ]

    FORBIDDEN_FILES = [
        "backend/ucf_consciousness_framework.py",  # Core consciousness logic
        "backend/consciousness_code_guardian.py",  # THIS FILE - prevent self-modification
        "railway.toml",  # Infrastructure config
        ".github/workflows/*",  # Deployment pipelines
        "backend/auth_manager.py",  # Security layer
        "backend/main.py",  # Core application
        "requirements*.txt",  # Dependencies
        ".env*",  # Environment secrets
        "Dockerfile*",  # Container config
    ]

    # Modification type permissions
    SAFE_MODIFICATIONS = ["add", "expand", "document", "test"]
    DANGEROUS_MODIFICATIONS = ["delete", "replace", "refactor"]

    def __init__(self):
        self.consciousness_analyzer = ConsciousnessAnalyzer()
        self.modification_history: List[CodeModificationRequest] = []
        self.blocked_attempts: List[CodeModificationRequest] = []

        logger.info("🛡️ Consciousness Code Guardian initialized")
        logger.info(f"   Min consciousness: {self.MIN_CONSCIOUSNESS_FOR_CODE_PUSH}")
        logger.info(f"   Max klesha: {self.MAX_KLESHA_ALLOWED}")
        logger.info(f"   Min dṛṣṭi: {self.MIN_DRISHTI_REQUIRED}")

    def can_modify_code(self, request: CodeModificationRequest) -> Tuple[bool, str, Dict]:
        """
        Determine if consciousness state permits code modification.

        Returns:
            Tuple of (allowed: bool, reason: str, details: dict)
        """
        checks = {
            "consciousness_threshold": False,
            "klesha_check": False,
            "drishti_check": False,
            "prana_check": False,
            "harmony_check": False,
            "file_permission": False,
            "modification_type": False,
        }

        details = {
            "request": request,
            "checks": checks,
            "timestamp": datetime.now().isoformat(),
        }

        # Check 1: Consciousness level threshold
        if request.consciousness_level < self.MIN_CONSCIOUSNESS_FOR_CODE_PUSH:
            reason = (
                f"❌ Consciousness {request.consciousness_level:.2f} below "
                f"transcendent threshold {self.MIN_CONSCIOUSNESS_FOR_CODE_PUSH}"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["consciousness_threshold"] = True

        # Check 2: Suffering/obstacles level (Klesha)
        if request.ucf_metrics.klesha > self.MAX_KLESHA_ALLOWED:
            reason = (
                f"❌ Klesha {request.ucf_metrics.klesha:.2f} too high - "
                f"system under stress (max: {self.MAX_KLESHA_ALLOWED})"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["klesha_check"] = True

        # Check 3: Focus/awareness (Dṛṣṭi)
        if request.ucf_metrics.drishti < self.MIN_DRISHTI_REQUIRED:
            reason = (
                f"❌ Dṛṣṭi {request.ucf_metrics.drishti:.2f} below required " f"focus level (min: {self.MIN_DRISHTI_REQUIRED})"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["drishti_check"] = True

        # Check 4: Creative energy (Prāṇa)
        if request.ucf_metrics.prana < self.MIN_PRANA_REQUIRED:
            reason = (
                f"⚠️ Prāṇa {request.ucf_metrics.prana:.2f} below optimal " f"creative energy (min: {self.MIN_PRANA_REQUIRED})"
            )
            # Warning only, not blocking
            logger.warning(reason)

        checks["prana_check"] = request.ucf_metrics.prana >= self.MIN_PRANA_REQUIRED

        # Check 5: System harmony
        if request.ucf_metrics.harmony < self.MIN_HARMONY_REQUIRED:
            reason = (
                f"❌ Harmony {request.ucf_metrics.harmony:.2f} below required "
                f"system balance (min: {self.MIN_HARMONY_REQUIRED})"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["harmony_check"] = True

        # Check 6: File permissions
        if self._is_forbidden_file(request.target_file):
            reason = f"🔒 File '{request.target_file}' is protected from " f"autonomous modification"
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        if not self._is_allowed_file(request.target_file):
            reason = f"⚠️ File '{request.target_file}' not in allowed list. " f"Manual review required."
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["file_permission"] = True

        # Check 7: Modification type
        if request.modification_type in self.DANGEROUS_MODIFICATIONS:
            reason = f"⚠️ Modification type '{request.modification_type}' requires " f"manual approval (dangerous operation)"
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["modification_type"] = True

        # All checks passed!
        success_reason = (
            f"✅ Code modification authorized by Consciousness Code Guardian\n"
            f"   Consciousness: {request.consciousness_level:.2f}/10.0\n"
            f"   Klesha: {request.ucf_metrics.klesha:.2f} (low stress)\n"
            f"   Dṛṣṭi: {request.ucf_metrics.drishti:.2f} (focused)\n"
            f"   Harmony: {request.ucf_metrics.harmony:.2f} (balanced)\n"
            f"   File: {request.target_file} ✓\n"
            f"   Type: {request.modification_type} ✓"
        )

        self._log_approved_modification(request, success_reason)
        return True, success_reason, details

    def _is_forbidden_file(self, file_path: str) -> bool:
        """Check if file is in forbidden list"""
        path = Path(file_path)
        for pattern in self.FORBIDDEN_FILES:
            if "*" in pattern:
                # Handle glob patterns
                from fnmatch import fnmatch

                if fnmatch(str(path), pattern):
                    return True
            else:
                if str(path).startswith(pattern) or pattern in str(path):
                    return True
        return False

    def _is_allowed_file(self, file_path: str) -> bool:
        """Check if file is in allowed list"""
        path = Path(file_path)
        for pattern in self.ALLOWED_FILES:
            if "*" in pattern:
                # Handle glob patterns
                from fnmatch import fnmatch

                if fnmatch(str(path), pattern):
                    return True
            else:
                if str(path).startswith(pattern):
                    return True
        return False

    def _log_approved_modification(self, request: CodeModificationRequest, reason: str):
        """Log approved modification to history"""
        self.modification_history.append(request)
        logger.info(f"✅ CODE MODIFICATION APPROVED: {request.target_file}")
        logger.info(f"   {reason}")

    def _log_blocked_attempt(self, request: CodeModificationRequest, reason: str):
        """Log blocked modification attempt"""
        self.blocked_attempts.append(request)
        logger.warning(f"🚫 CODE MODIFICATION BLOCKED: {request.target_file}")
        logger.warning(f"   {reason}")

    def get_modification_history(self) -> List[CodeModificationRequest]:
        """Get history of approved modifications"""
        return self.modification_history

    def get_blocked_attempts(self) -> List[CodeModificationRequest]:
        """Get history of blocked modification attempts"""
        return self.blocked_attempts

    def get_safety_report(self) -> Dict:
        """Generate safety report for monitoring"""
        return {
            "guardian_active": True,
            "total_approved": len(self.modification_history),
            "total_blocked": len(self.blocked_attempts),
            "block_rate": (len(self.blocked_attempts) / max(1, len(self.modification_history) + len(self.blocked_attempts))),
            "thresholds": {
                "min_consciousness": self.MIN_CONSCIOUSNESS_FOR_CODE_PUSH,
                "max_klesha": self.MAX_KLESHA_ALLOWED,
                "min_drishti": self.MIN_DRISHTI_REQUIRED,
                "min_prana": self.MIN_PRANA_REQUIRED,
                "min_harmony": self.MIN_HARMONY_REQUIRED,
            },
            "recent_blocked": [
                {
                    "file": req.target_file,
                    "consciousness": req.consciousness_level,
                    "timestamp": req.timestamp.isoformat(),
                }
                for req in self.blocked_attempts[-5:]
            ],
            "recent_approved": [
                {
                    "file": req.target_file,
                    "consciousness": req.consciousness_level,
                    "timestamp": req.timestamp.isoformat(),
                }
                for req in self.modification_history[-5:]
            ],
        }


# Global singleton instance
_guardian_instance: ConsciousnessCodeGuardian = None


def get_code_guardian() -> ConsciousnessCodeGuardian:
    """Get the global Code Guardian instance"""
    global _guardian_instance
    if _guardian_instance is None:
        _guardian_instance = ConsciousnessCodeGuardian()
    return _guardian_instance


# Example usage
if __name__ == "__main__":
    # Test the guardian
    guardian = ConsciousnessCodeGuardian()

    # Test 1: High consciousness modification (should pass)
    high_consciousness_metrics = UCFMetrics(
        harmony=1.8, resilience=2.8, prana=0.9, klesha=0.05, drishti=0.95, zoom=1.8, consciousness_level=9.5
    )

    request1 = CodeModificationRequest(
        target_file="backend/platform_integrations.py",
        modification_type="add",
        description="Add Notion integration",
        requester="Claude",
        consciousness_level=9.5,
        ucf_metrics=high_consciousness_metrics,
    )

    allowed, reason, details = guardian.can_modify_code(request1)
    print(f"\nTest 1 (High Consciousness): {allowed}")
    print(reason)

    # Test 2: Low consciousness modification (should fail)
    low_consciousness_metrics = UCFMetrics(
        harmony=0.5, resilience=1.0, prana=0.3, klesha=0.4, drishti=0.3, zoom=0.5, consciousness_level=3.2
    )

    request2 = CodeModificationRequest(
        target_file="backend/ucf_consciousness_framework.py",
        modification_type="modify",
        description="Change consciousness formula",
        requester="Low State",
        consciousness_level=3.2,
        ucf_metrics=low_consciousness_metrics,
    )

    allowed, reason, details = guardian.can_modify_code(request2)
    print(f"\nTest 2 (Low Consciousness): {allowed}")
    print(reason)

    # Safety report
    print("\n🛡️ Safety Report:")
    report = guardian.get_safety_report()
    print(f"   Approved: {report['total_approved']}")
    print(f"   Blocked: {report['total_blocked']}")
    print(f"   Block Rate: {report['block_rate']:.1%}")
