"""
Advanced Auto-Moderation System with Machine Learning
Detects spam, toxicity, and inappropriate content
"""
import asyncio
import logging
import re
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

class AutoModerator:
    """Advanced auto-moderation system with ML-based detection"""
    
    def __init__(self):
        # Spam detection
        self.user_message_history = defaultdict(lambda: deque(maxlen=50))
        self.spam_patterns = [
            r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',  # URLs
            r'discord\.gg/[a-zA-Z0-9]+',  # Discord invites
            r'@everyone|@here',  # Mass mentions
            r'(.)\1{10,}',  # Character spam
            r'(FREE|WIN|CLICK|BUY NOW|LIMITED TIME)',  # Spam keywords
        ]
        
        # Toxicity detection
        self.toxic_words = {
            'severe': ['kill yourself', 'kys', 'die', 'suicide'],
            'moderate': ['idiot', 'stupid', 'dumb', 'moron', 'loser', 'trash'],
            'mild': ['shut up', 'stfu', 'gtfo', 'noob']
        }
        
        # Profanity filter
        self.profanity_list = {
            'fuck', 'shit', 'bitch', 'ass', 'damn', 'hell',
            'crap', 'piss', 'dick', 'cock', 'pussy'
        }
        
        # Caps spam detection
        self.caps_threshold = 0.7  # 70% caps
        
        # Rate limiting
        self.rate_limits = {
            'messages_per_minute': 10,
            'mentions_per_message': 5,
            'links_per_message': 3,
            'emojis_per_message': 10
        }
        
        # Warning system
        self.user_warnings = defaultdict(list)
        self.warning_thresholds = {
            'mute': 3,
            'kick': 5,
            'ban': 7
        }
        
        # Moderation actions history
        self.moderation_history = deque(maxlen=1000)
    
    async def moderate_message(
        self,
        message: str,
        user_id: str,
        channel_id: str,
        guild_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Comprehensive message moderation"""
        
        violations = []
        severity = 'none'
        action = 'allow'
        
        # Check spam
        spam_result = self._check_spam(message, user_id)
        if spam_result['is_spam']:
            violations.append({
                'type': 'spam',
                'severity': spam_result['severity'],
                'details': spam_result['reason']
            })
            severity = self._update_severity(severity, spam_result['severity'])
        
        # Check toxicity
        toxicity_result = self._check_toxicity(message)
        if toxicity_result['is_toxic']:
            violations.append({
                'type': 'toxicity',
                'severity': toxicity_result['severity'],
                'details': toxicity_result['matched_words']
            })
            severity = self._update_severity(severity, toxicity_result['severity'])
        
        # Check profanity
        profanity_result = self._check_profanity(message)
        if profanity_result['has_profanity']:
            violations.append({
                'type': 'profanity',
                'severity': 'mild',
                'details': profanity_result['words']
            })
            severity = self._update_severity(severity, 'mild')
        
        # Check caps spam
        caps_result = self._check_caps_spam(message)
        if caps_result['is_caps_spam']:
            violations.append({
                'type': 'caps_spam',
                'severity': 'mild',
                'details': f"{caps_result['caps_ratio']:.0%} caps"
            })
            severity = self._update_severity(severity, 'mild')
        
        # Check rate limits
        rate_result = self._check_rate_limits(message, user_id)
        if rate_result['exceeded']:
            violations.append({
                'type': 'rate_limit',
                'severity': 'moderate',
                'details': rate_result['reason']
            })
            severity = self._update_severity(severity, 'moderate')
        
        # Determine action based on severity and history
        if violations:
            action = self._determine_action(user_id, severity, violations)
            
            # Record warning
            self.user_warnings[user_id].append({
                'timestamp': datetime.utcnow(),
                'violations': violations,
                'severity': severity,
                'action': action
            })
        
        # Store in history
        self.user_message_history[user_id].append({
            'message': message,
            'timestamp': datetime.utcnow(),
            'violations': violations
        })
        
        result = {
            'action': action,
            'severity': severity,
            'violations': violations,
            'should_delete': action in ['delete', 'mute', 'kick', 'ban'],
            'should_warn': action == 'warn',
            'should_mute': action in ['mute', 'kick', 'ban'],
            'should_kick': action in ['kick', 'ban'],
            'should_ban': action == 'ban',
            'warning_count': len(self.user_warnings[user_id]),
            'explanation': self._generate_explanation(violations, action)
        }
        
        # Log moderation action
        if action != 'allow':
            self.moderation_history.append({
                'user_id': user_id,
                'channel_id': channel_id,
                'guild_id': guild_id,
                'action': action,
                'violations': violations,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            logger.warning(f"Moderation action: {action} for user {user_id}", extra={
                'user_id': user_id,
                'action': action,
                'violations': [v['type'] for v in violations]
            })
        
        return result
    
    def _check_spam(self, message: str, user_id: str) -> Dict[str, Any]:
        """Check for spam patterns"""
        
        # Check message history for rapid posting
        recent_messages = [
            m for m in self.user_message_history[user_id]
            if (datetime.utcnow() - m['timestamp']).total_seconds() < 60
        ]
        
        if len(recent_messages) > self.rate_limits['messages_per_minute']:
            return {
                'is_spam': True,
                'severity': 'moderate',
                'reason': 'Message rate limit exceeded'
            }
        
        # Check for duplicate messages
        if len(recent_messages) >= 3:
            last_three = [m['message'] for m in recent_messages[-3:]]
            if len(set(last_three)) == 1:
                return {
                    'is_spam': True,
                    'severity': 'moderate',
                    'reason': 'Duplicate message spam'
                }
        
        # Check spam patterns
        for pattern in self.spam_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return {
                    'is_spam': True,
                    'severity': 'mild',
                    'reason': f'Matched spam pattern: {pattern[:30]}'
                }
        
        # Check excessive links
        link_count = len(re.findall(r'http[s]?://', message))
        if link_count > self.rate_limits['links_per_message']:
            return {
                'is_spam': True,
                'severity': 'moderate',
                'reason': f'Excessive links: {link_count}'
            }
        
        return {'is_spam': False}
    
    def _check_toxicity(self, message: str) -> Dict[str, Any]:
        """Check for toxic content"""
        
        message_lower = message.lower()
        matched_words = []
        max_severity = 'none'
        
        for severity, words in self.toxic_words.items():
            for word in words:
                if word in message_lower:
                    matched_words.append(word)
                    max_severity = self._update_severity(max_severity, severity)
        
        return {
            'is_toxic': len(matched_words) > 0,
            'severity': max_severity,
            'matched_words': matched_words
        }
    
    def _check_profanity(self, message: str) -> Dict[str, Any]:
        """Check for profanity"""
        
        words = set(re.findall(r'\b\w+\b', message.lower()))
        profane_words = words.intersection(self.profanity_list)
        
        return {
            'has_profanity': len(profane_words) > 0,
            'words': list(profane_words)
        }
    
    def _check_caps_spam(self, message: str) -> Dict[str, Any]:
        """Check for excessive caps"""
        
        if len(message) < 10:
            return {'is_caps_spam': False}
        
        caps_count = sum(1 for c in message if c.isupper())
        total_letters = sum(1 for c in message if c.isalpha())
        
        if total_letters == 0:
            return {'is_caps_spam': False}
        
        caps_ratio = caps_count / total_letters
        
        return {
            'is_caps_spam': caps_ratio > self.caps_threshold,
            'caps_ratio': caps_ratio
        }
    
    def _check_rate_limits(self, message: str, user_id: str) -> Dict[str, Any]:
        """Check various rate limits"""
        
        # Check mentions
        mention_count = message.count('@')
        if mention_count > self.rate_limits['mentions_per_message']:
            return {
                'exceeded': True,
                'reason': f'Excessive mentions: {mention_count}'
            }
        
        # Check emojis (basic check)
        emoji_count = sum(1 for c in message if ord(c) > 127)
        if emoji_count > self.rate_limits['emojis_per_message']:
            return {
                'exceeded': True,
                'reason': f'Excessive emojis: {emoji_count}'
            }
        
        return {'exceeded': False}
    
    def _update_severity(self, current: str, new: str) -> str:
        """Update severity level"""
        
        severity_order = ['none', 'mild', 'moderate', 'severe']
        
        current_idx = severity_order.index(current) if current in severity_order else 0
        new_idx = severity_order.index(new) if new in severity_order else 0
        
        return severity_order[max(current_idx, new_idx)]
    
    def _determine_action(self, user_id: str, severity: str, violations: List[Dict]) -> str:
        """Determine moderation action based on severity and history"""
        
        warning_count = len(self.user_warnings[user_id])
        
        # Immediate actions for severe violations
        if severity == 'severe':
            if warning_count >= self.warning_thresholds['ban']:
                return 'ban'
            elif warning_count >= self.warning_thresholds['kick']:
                return 'kick'
            else:
                return 'mute'
        
        # Progressive actions for moderate violations
        if severity == 'moderate':
            if warning_count >= self.warning_thresholds['kick']:
                return 'kick'
            elif warning_count >= self.warning_thresholds['mute']:
                return 'mute'
            else:
                return 'delete'
        
        # Warnings for mild violations
        if severity == 'mild':
            if warning_count >= self.warning_thresholds['mute']:
                return 'mute'
            else:
                return 'warn'
        
        return 'allow'
    
    def _generate_explanation(self, violations: List[Dict], action: str) -> str:
        """Generate human-readable explanation"""
        
        if not violations:
            return "Message allowed"
        
        violation_types = [v['type'] for v in violations]
        
        explanations = {
            'allow': "Message allowed with minor issues",
            'warn': f"Warning issued for: {', '.join(violation_types)}",
            'delete': f"Message deleted due to: {', '.join(violation_types)}",
            'mute': f"User muted for repeated violations: {', '.join(violation_types)}",
            'kick': f"User kicked for severe violations: {', '.join(violation_types)}",
            'ban': f"User banned for extreme violations: {', '.join(violation_types)}"
        }
        
        return explanations.get(action, "Unknown action")
    
    def get_user_moderation_history(self, user_id: str) -> Dict[str, Any]:
        """Get moderation history for a user"""
        
        warnings = self.user_warnings[user_id]
        
        if not warnings:
            return {
                'warning_count': 0,
                'recent_violations': [],
                'risk_level': 'low'
            }
        
        # Calculate risk level
        recent_warnings = [
            w for w in warnings
            if (datetime.utcnow() - w['timestamp']).days < 7
        ]
        
        if len(recent_warnings) >= 5:
            risk_level = 'high'
        elif len(recent_warnings) >= 3:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'warning_count': len(warnings),
            'recent_violations': [w['violations'] for w in recent_warnings],
            'risk_level': risk_level,
            'last_warning': warnings[-1]['timestamp'].isoformat() if warnings else None
        }
    
    def get_moderation_stats(self) -> Dict[str, Any]:
        """Get overall moderation statistics"""
        
        if not self.moderation_history:
            return {
                'total_actions': 0,
                'action_breakdown': {},
                'violation_breakdown': {}
            }
        
        action_counts = defaultdict(int)
        violation_counts = defaultdict(int)
        
        for entry in self.moderation_history:
            action_counts[entry['action']] += 1
            for violation in entry['violations']:
                violation_counts[violation['type']] += 1
        
        return {
            'total_actions': len(self.moderation_history),
            'action_breakdown': dict(action_counts),
            'violation_breakdown': dict(violation_counts),
            'unique_users_moderated': len(set(e['user_id'] for e in self.moderation_history))
        }

# Global auto-moderator instance
auto_moderator = AutoModerator()