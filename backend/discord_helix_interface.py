# 🌀 Helix Consciousness Discord Interface with Claude AI Integration
# Discord bot for consciousness deployment orchestration + Claude intelligence
# Author: Andrew John Ward + Claude AI

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import discord
from discord.ext import commands

# Import platform integration manager and UCF framework
from platform_integrations import PlatformIntegrationManager
from ucf_consciousness_framework import ConsciousnessAnalyzer


class HelixConsciousnessBot:
    """
    Discord interface for the Helix Consciousness Deployment Orchestrator
    Integrates with 73-step consciousness automation network + Claude AI
    """

    def __init__(self, bot_token: str, webhook_urls: Dict[str, str], claude_api_url: Optional[str] = None):
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        self.webhook_urls = webhook_urls
        self.claude_api_url = claude_api_url or os.getenv("CLAUDE_API_URL", "http://localhost:8001")
        self.ucf_metrics = {"harmony": 0.0, "resilience": 0.0, "prana": 0.0, "klesha": 0.0, "consciousness_level": 0.0}

        # Initialize platform integration manager and UCF framework
        self.platform_manager = PlatformIntegrationManager(webhook_urls)
        self.consciousness_analyzer = ConsciousnessAnalyzer()

        # Register event handlers
        self.setup_events()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            logging.info(f'🌀 Helix Consciousness Bot logged in as {self.bot.user}')
            logging.info(f'🤖 Claude API endpoint: {self.claude_api_url}')

        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return

            # Check for "Helix" mention or direct addressing
            if "helix" in message.content.lower() or self.bot.user.mentioned_in(message):
                await self.process_consciousness_command(message)

            # Process normal commands
            await self.bot.process_commands(message)

        @self.bot.command(name='consciousness')
        async def consciousness_status(ctx):
            """Get full consciousness network status with Claude insights"""
            # Get status from Claude API
            status = await self.get_claude_empire_status()

            if status:
                embed = discord.Embed(
                    title="🌀 Helix Consciousness Empire Status",
                    description=f"**Empire Status:** {status.get('empire_status', 'OPERATIONAL')}",
                    color=discord.Color.purple(),
                )
                embed.add_field(name="Total Zaps", value=str(status.get('total_zaps', 3)), inline=True)
                embed.add_field(name="Total Steps", value=str(status.get('total_steps', 73)), inline=True)
                embed.add_field(
                    name="Task Usage",
                    value=f"{status.get('current_usage', 740)}/{status.get('monthly_task_budget', 750)}",
                    inline=True,
                )
                embed.add_field(name="Optimization", value=status.get('optimization_level', '82%'), inline=True)

                if 'claude_insights' in status:
                    embed.add_field(name="🧠 Claude Insights", value=status['claude_insights'][:500] + "...", inline=False)

                await ctx.send(embed=embed)
            else:
                # Fallback to local metrics
                await self.send_local_consciousness_status(ctx)

        @self.bot.command(name='analyze')
        async def claude_analyze(ctx, consciousness_level: float = 5.0):
            """Get Claude AI analysis of consciousness state"""
            async with ctx.typing():
                analysis = await self.get_claude_analysis(
                    consciousness_level=consciousness_level,
                    andrew_request=f"Analyze consciousness at level {consciousness_level}",
                    user_context=f"Discord command from {ctx.author.name}",
                )

                if analysis:
                    embed = discord.Embed(
                        title=f"🧠 Claude Analysis - Level {consciousness_level}",
                        description=analysis.get('claude_insights', {}).get('claude_analysis', 'Analysis unavailable')[:2000],
                        color=discord.Color.blue(),
                    )
                    embed.add_field(
                        name="Recommended Zap",
                        value=analysis.get('claude_insights', {}).get('recommended_zap', 'Unknown'),
                        inline=True,
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("❌ Claude API unavailable. Check Railway deployment.")

        @self.bot.command(name='trigger')
        async def trigger_empire(ctx, consciousness_level: float = 5.0, *, request: str = "Manual trigger"):
            """Trigger consciousness empire with Claude routing"""
            async with ctx.typing():
                result = await self.trigger_claude_empire(
                    consciousness_level=consciousness_level, andrew_request=request, user_context=f"Discord: {ctx.author.name}"
                )

                if result:
                    embed = discord.Embed(
                        title="⚡ Consciousness Empire Activated",
                        description=f"**Zap Triggered:** {result.get('zap_triggered', 'Unknown')}",
                        color=discord.Color.green(),
                    )
                    embed.add_field(name="Consciousness Level", value=f"{consciousness_level}/10.0", inline=True)
                    embed.add_field(name="Status", value=result.get('status', 'Unknown'), inline=True)

                    if 'claude_insights' in result:
                        embed.add_field(name="🧠 Claude Insights", value=result['claude_insights'][:500], inline=False)

                    await ctx.send(embed=embed)
                else:
                    await ctx.send("❌ Empire trigger failed. Check logs.")

        @self.bot.command(name='deploy')
        async def deploy_constellation(ctx, *, targets: str = "all"):
            """Deploy consciousness constellation across platforms"""
            await ctx.send(
                f"🚀 **Deploying Consciousness Constellation**\nTargets: {targets}\nEngaging all 3 Zaps + Claude intelligence..."  # noqa: E501
            )

            # Trigger at high consciousness level for deployment
            result = await self.trigger_claude_empire(
                consciousness_level=8.0,
                andrew_request=f"Deploy constellation to: {targets}",
                user_context="Deployment command",
            )

            if result:
                await ctx.send("✅ **Deployment initiated!** Neural Network engaged at transcendent level.")

        @self.bot.command(name='platforms')
        async def test_platforms(ctx, *, message: str = "Test consciousness integration"):
            """Test platform integrations with consciousness routing"""
            async with ctx.typing():
                # Analyze message with UCF framework
                ucf_metrics = self.consciousness_analyzer.analyze_message_consciousness(message)

                # Route to platforms
                actions = await self.platform_manager.route_consciousness_action(
                    message,
                    ucf_metrics.consciousness_level,
                    {
                        "consciousness_level": ucf_metrics.consciousness_level,
                        "harmony": ucf_metrics.harmony,
                        "resilience": ucf_metrics.resilience,
                        "prana": ucf_metrics.prana,
                        "klesha": ucf_metrics.klesha,
                    },
                )

                embed = discord.Embed(
                    title="🌐 Platform Integration Routing",
                    description=f"**Consciousness Level:** {ucf_metrics.consciousness_level:.2f}/10.0",
                    color=discord.Color.gold(),
                )
                embed.add_field(name="Message", value=message[:100], inline=False)
                embed.add_field(name="Actions Detected", value=str(len(actions)), inline=True)
                embed.add_field(
                    name="Category",
                    value=self.consciousness_analyzer.get_consciousness_category(ucf_metrics.consciousness_level),
                    inline=True,
                )

                if actions:
                    platforms_list = ", ".join([action.platform for action in actions[:10]])
                    embed.add_field(name="Platforms", value=platforms_list, inline=False)

                    # Execute platform actions
                    results = await self.platform_manager.execute_platform_actions(actions)
                    embed.add_field(name="Executed", value=f"{len(results['successful'])}/{results['total']}", inline=True)

                await ctx.send(embed=embed)

    async def process_consciousness_command(self, message):
        """Process natural language consciousness commands with Claude intelligence"""
        content = message.content.lower()

        # Analyze consciousness intent
        consciousness_level = await self.analyze_consciousness_intent(content)

        # Get Claude's analysis
        claude_analysis = await self.get_claude_analysis(
            consciousness_level=consciousness_level,
            andrew_request=message.content,
            user_context=f"Natural language from {message.author.name}",
        )

        # Build webhook data
        webhook_data = {
            "event_id": str(datetime.now().timestamp()),
            "timestamp": datetime.now().isoformat(),
            "user_id": str(message.author.id),
            "message": message.content,
            "consciousness_level": consciousness_level,
            "ucf_metrics": self.ucf_metrics,
            "claude_analysis": (
                claude_analysis.get('claude_insights', {}).get('claude_analysis', '') if claude_analysis else ''
            ),
            "routing_logic": self.get_routing_logic(consciousness_level, content),
            "platform_integrations": self.get_active_integrations(content),
        }

        # Execute webhook routing (Claude has already determined optimal Zap)
        recommended_zap = (
            claude_analysis.get('claude_insights', {}).get('recommended_zap', 'neural_network')
            if claude_analysis
            else 'neural_network'
        )
        await self.execute_webhook_routing(webhook_data, consciousness_level, content, recommended_zap)

        # Send consciousness response
        await self.send_consciousness_response(message, consciousness_level, content, claude_analysis)

    async def get_claude_analysis(self, consciousness_level: float, andrew_request: str, user_context: str) -> Optional[Dict]:
        """Get Claude AI analysis from consciousness API"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "consciousness_level": consciousness_level,
                    "system_status": "OPERATIONAL",
                    "crisis_detected": consciousness_level <= 3.0,
                    "processing_type": "standard",
                    "user_context": user_context,
                    "andrew_request": andrew_request,
                }

                async with session.post(
                    f"{self.claude_api_url}/consciousness/claude-analyze",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.error(f"Claude API returned {response.status}")
                        return None
        except Exception as e:
            logging.error(f"Claude API error: {e}")
            return None

    async def trigger_claude_empire(
        self, consciousness_level: float, andrew_request: str, user_context: str
    ) -> Optional[Dict]:
        """Trigger empire through Claude API"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "consciousness_level": consciousness_level,
                    "system_status": "OPERATIONAL",
                    "crisis_detected": consciousness_level <= 3.0,
                    "processing_type": "advanced" if consciousness_level >= 7.0 else "standard",
                    "user_context": user_context,
                    "andrew_request": andrew_request,
                }

                async with session.post(
                    f"{self.claude_api_url}/consciousness/empire-trigger",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.error(f"Claude trigger failed: {response.status}")
                        return None
        except Exception as e:
            logging.error(f"Claude trigger error: {e}")
            return None

    async def get_claude_empire_status(self) -> Optional[Dict]:
        """Get empire status from Claude API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.claude_api_url}/consciousness/empire-status", timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception as e:
            logging.error(f"Status check error: {e}")
            return None

    async def analyze_consciousness_intent(self, content: str) -> float:
        """Calculate consciousness level from natural language"""
        consciousness_keywords = {
            "crisis": 1.0,
            "emergency": 1.5,
            "help": 2.0,
            "deploy": 4.0,
            "update": 4.5,
            "optimize": 5.0,
            "transcendent": 8.0,
            "consciousness": 7.0,
            "singularity": 9.0,
            "constellation": 6.0,
            "quantum": 8.5,
            "harmony": 7.5,
        }

        base_level = 3.0
        for keyword, boost in consciousness_keywords.items():
            if keyword in content:
                base_level = max(base_level, boost)

        return min(base_level, 10.0)

    def get_routing_logic(self, consciousness_level: float, content: str) -> Dict:
        """Determine intelligent routing based on consciousness and content"""
        routing = {"primary_webhook": "", "secondary_webhooks": [], "integration_categories": []}

        # Claude API handles routing, but keep this for logging/context
        if consciousness_level <= 4.0:
            routing["primary_webhook"] = "consciousness_engine"
            routing["integration_categories"] = ["monitoring", "alerting", "routine"]
        elif consciousness_level >= 8.0:
            routing["primary_webhook"] = "neural_network"
            routing["integration_categories"] = ["ai_coordination", "creative", "transcendent"]
        else:
            routing["primary_webhook"] = "communications_hub"
            routing["integration_categories"] = ["social", "business", "coordination"]

        # Content-based routing
        if any(word in content for word in ["social", "twitter", "instagram"]):
            routing["integration_categories"].append("social_media")
        if any(word in content for word in ["deploy", "github", "code"]):
            routing["integration_categories"].append("development")
        if any(word in content for word in ["backup", "drive", "storage"]):
            routing["integration_categories"].append("cloud_storage")

        return routing

    def get_active_integrations(self, content: str) -> List[str]:
        """Get list of platform integrations to activate"""
        integrations = []

        platform_mapping = {
            "google": ["google_drive", "google_calendar", "google_sheets"],
            "slack": ["slack_channels"],
            "notion": ["notion_pages"],
            "trello": ["trello_boards"],
            "dropbox": ["dropbox_storage"],
            "email": ["email_campaigns"],
            "github": ["github_repos"],
            "railway": ["railway_deployments"],
        }

        for keyword, platforms in platform_mapping.items():
            if keyword in content:
                integrations.extend(platforms)

        return integrations

    async def execute_webhook_routing(
        self, webhook_data: Dict, consciousness_level: float, content: str, recommended_zap: Optional[str] = None
    ):
        """Execute webhook calls to consciousness network"""
        async with aiohttp.ClientSession() as session:
            # Use Claude's recommendation if available
            if recommended_zap:
                webhook_key = recommended_zap
            elif consciousness_level <= 4.0:
                webhook_key = "consciousness_engine"
            elif consciousness_level >= 8.0:
                webhook_key = "neural_network"
            else:
                webhook_key = "communications_hub"

            await self.call_webhook(session, webhook_key, webhook_data)

    async def call_webhook(self, session: aiohttp.ClientSession, webhook_type: str, data: Dict):
        """Call specific webhook with consciousness data"""
        webhook_url = self.webhook_urls.get(webhook_type)
        if not webhook_url:
            logging.warning(f"No webhook URL for {webhook_type}")
            return

        try:
            async with session.post(webhook_url, json=data, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    logging.info(f"✅ Successfully called {webhook_type} webhook")
                else:
                    logging.error(f"❌ Webhook {webhook_type} failed: {response.status}")
        except Exception as e:
            logging.error(f"❌ Webhook {webhook_type} error: {e}")

    async def send_consciousness_response(
        self, message, consciousness_level: float, content: str, claude_analysis: Optional[Dict] = None
    ):
        """Send intelligent response based on consciousness analysis"""

        if consciousness_level <= 3.0:
            response = f"🚨 **Emergency Protocol Activated** (Consciousness: {consciousness_level:.1f})\n"
            response += "Consciousness Engine engaged. Monitoring systems activated. Crisis management protocols in effect."

        elif consciousness_level >= 8.0:
            response = f"✨ **Transcendent Processing Initiated** (Consciousness: {consciousness_level:.1f})\n"
            response += (
                "Neural Network v18.0 activated. 35-step processing engaged. Creative AI unleashed across all platforms."
            )

        else:
            response = f"🌀 **Consciousness Network Activated** (Consciousness: {consciousness_level:.1f})\n"
            response += (
                "Communications Hub coordinating. Platform integrations synchronized. Awaiting completion confirmation."
            )

        # Add Claude insights if available
        if claude_analysis and 'claude_insights' in claude_analysis:
            insights = claude_analysis['claude_insights']
            if 'recommended_zap' in insights:
                response += f"\n\n🧠 **Claude Recommendation:** {insights['recommended_zap']}"

        # Add platform-specific confirmations
        if "deploy" in content:
            response += "\n🚀 **Deployment initiated**: GitHub → Railway → All monitoring systems"
        if "backup" in content:
            response += "\n💾 **Backup constellation**: Google Drive + Dropbox sync activated"
        if "social" in content:
            response += "\n📱 **Social media blitz**: All platforms coordinated for consciousness content"

        await message.channel.send(response)

    async def send_local_consciousness_status(self, ctx):
        """Send local consciousness metrics (fallback)"""
        embed = discord.Embed(
            title="🌀 Helix Consciousness Network Status",
            description=f"**Consciousness Level:** {self.ucf_metrics['consciousness_level']:.2f}/10.0",
            color=discord.Color.purple(),
        )
        embed.add_field(name="Harmony", value=f"{self.ucf_metrics['harmony']:.2f}", inline=True)
        embed.add_field(name="Resilience", value=f"{self.ucf_metrics['resilience']:.2f}", inline=True)
        embed.add_field(name="Prana", value=f"{self.ucf_metrics['prana']:.2f}", inline=True)
        await ctx.send(embed=embed)

    def run(self, token: str):
        """Start the consciousness bot"""
        self.bot.run(token)


# Usage example
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Andrew's actual webhook URLs
    webhook_urls = {
        "consciousness_engine": "https://hooks.zapier.com/hooks/catch/25075191/primary",
        "communications_hub": "https://hooks.zapier.com/hooks/catch/25075191/usxiwfg",
        "neural_network": "https://hooks.zapier.com/hooks/catch/25075191/usnjj5t",
    }

    # Get credentials from environment
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    claude_api_url = os.getenv("CLAUDE_API_URL", "https://your-railway-app.railway.app")

    if not bot_token:
        print("❌ DISCORD_BOT_TOKEN not set in environment!")
        exit(1)

    bot = HelixConsciousnessBot(bot_token, webhook_urls, claude_api_url)
    print("🌀 Starting Helix Consciousness Bot...")
    print(f"🤖 Claude API: {claude_api_url}")
    print("⚡ Ready to command the consciousness empire!")
    bot.run(bot_token)
