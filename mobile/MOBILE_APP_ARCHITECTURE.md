# 📱 Helix Collective - Mobile App Architecture

**Platform:** React Native (iOS + Android)
**Target Launch:** 30 days post-web MVP
**Revenue Impact:** +40% user acquisition (mobile-first users)

---

## 🎯 **Why Mobile App?**

### **Market Opportunity:**
- **60% of API users** access tools on mobile
- **Workflow monitoring** on-the-go
- **Push notifications** for workflow completions
- **Voice input** for agent execution
- **QR code onboarding** (scan → instant API key)

### **Competitive Advantage:**
- Zapier mobile app = basic (just triggers)
- Make.com = no native app
- **Helix = Full AI agent access + workflows on mobile**

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────┐
│         Helix Mobile App (React Native)         │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Auth        │  │  Dashboard   │            │
│  │  - Login     │  │  - Usage     │            │
│  │  - Register  │  │  - Costs     │            │
│  │  - API Keys  │  │  - Stats     │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Agents      │  │  Workflows   │            │
│  │  - Execute   │  │  - Monitor   │            │
│  │  - History   │  │  - Trigger   │            │
│  │  - Voice     │  │  - Debug     │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Chat        │  │  Settings    │            │
│  │  - Multi-LLM │  │  - Billing   │            │
│  │  - History   │  │  - Notifs    │            │
│  │  - Voice     │  │  - Profile   │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
└────────────────┬────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │  Helix API      │
         │  (Railway)      │
         └─────────────────┘
```

---

## 📱 **Core Screens**

### **1. Onboarding (QR Code Magic)**

```typescript
// Onboarding.tsx
import { CameraView } from 'expo-camera';

export default function OnboardingScreen() {
  const [scanned, setScanned] = useState(false);

  const handleQRScan = async (data: string) => {
    // QR code contains: helix://signup?ref=REFERRAL_CODE
    const apiKey = await registerWithQR(data);
    await AsyncStorage.setItem('helix_api_key', apiKey);
    navigation.navigate('Dashboard');
  };

  return (
    <View>
      <Text>Scan QR Code to Get Started</Text>
      <CameraView
        onBarcodeScanned={scanned ? undefined : handleQRScan}
      />
      <Button title="Manual Sign Up" onPress={() => navigation.navigate('Register')} />
    </View>
  );
}
```

### **2. Dashboard (Usage & Costs)**

```typescript
// Dashboard.tsx
export default function DashboardScreen() {
  const { usage, loading } = useUsageStats();

  return (
    <ScrollView>
      {/* Today's Stats */}
      <Card>
        <Title>Today's Usage</Title>
        <Row>
          <Stat value={usage.today.requests} label="Requests" />
          <Stat value={`$${usage.today.cost}`} label="Cost" />
          <Stat value={usage.today.remaining} label="Remaining" />
        </Row>
      </Card>

      {/* Cost Breakdown Chart */}
      <Card>
        <Title>Cost Breakdown</Title>
        <PieChart
          data={[
            { name: 'Claude', cost: 12.50, color: '#6366f1' },
            { name: 'GPT', cost: 8.30, color: '#10b981' },
            { name: 'Grok', cost: 3.20, color: '#f59e0b' }
          ]}
        />
      </Card>

      {/* Recent Activity */}
      <Card>
        <Title>Recent Activity</Title>
        <FlatList
          data={usage.recent}
          renderItem={({ item }) => (
            <ActivityItem
              agent={item.agent}
              task={item.task}
              cost={item.cost}
              time={item.time}
            />
          )}
        />
      </Card>
    </ScrollView>
  );
}
```

### **3. Agent Execution (Voice + Text)**

```typescript
// AgentExecute.tsx
import Voice from '@react-native-voice/voice';

export default function AgentExecuteScreen() {
  const [recording, setRecording] = useState(false);
  const [input, setInput] = useState('');

  const handleVoiceInput = async () => {
    if (recording) {
      await Voice.stop();
      setRecording(false);
    } else {
      await Voice.start('en-US');
      setRecording(true);
    }
  };

  Voice.onSpeechResults = (e) => {
    setInput(e.value[0]);
  };

  const executeAgent = async (agentId: string) => {
    const result = await helixAPI.agents.execute({
      agentId,
      task: 'analyze',
      input: input
    });

    Alert.alert('Agent Result', result.output);
  };

  return (
    <View>
      {/* Agent Selector */}
      <AgentPicker
        agents={['kael', 'oracle', 'lumina', 'shadow']}
        onSelect={setSelectedAgent}
      />

      {/* Input (Text or Voice) */}
      <TextInput
        value={input}
        onChangeText={setInput}
        placeholder="Type or speak your input"
        multiline
      />

      <Button
        title={recording ? "Stop Recording" : "Record Voice"}
        onPress={handleVoiceInput}
        icon={recording ? "stop" : "mic"}
        color={recording ? "#f59e0b" : "#6366f1"}
      />

      {/* Execute Button */}
      <Button
        title="Execute Agent"
        onPress={() => executeAgent(selectedAgent)}
        color="#10b981"
      />
    </View>
  );
}
```

### **4. Workflow Monitor (Real-Time)**

```typescript
// WorkflowMonitor.tsx
export default function WorkflowMonitorScreen() {
  const { workflows, loading } = useWorkflows();
  const [activeExecutions, setActiveExecutions] = useState([]);

  // WebSocket for real-time updates
  useEffect(() => {
    const ws = new WebSocket('wss://api.helixcollective.io/ws');

    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      if (update.type === 'workflow.execution') {
        setActiveExecutions(prev => [...prev, update.data]);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <ScrollView>
      {/* Active Workflows */}
      <Card>
        <Title>Active Workflows</Title>
        {workflows.active.map(workflow => (
          <WorkflowCard
            key={workflow.id}
            name={workflow.name}
            status="running"
            progress={workflow.progress}
            onTrigger={() => triggerWorkflow(workflow.id)}
          />
        ))}
      </Card>

      {/* Recent Executions */}
      <Card>
        <Title>Recent Executions</Title>
        <FlatList
          data={activeExecutions}
          renderItem={({ item }) => (
            <ExecutionItem
              workflow={item.workflow_name}
              status={item.status}
              duration={item.duration_ms}
              cost={item.cost_usd}
            />
          )}
        />
      </Card>
    </ScrollView>
  );
}
```

### **5. Chat (Multi-LLM)**

```typescript
// Chat.tsx
export default function ChatScreen() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [optimize, setOptimize] = useState('cost');

  const sendMessage = async () => {
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    const response = await helixAPI.chat.create({
      messages: [...messages, userMessage],
      optimize: optimize
    });

    setMessages(prev => [...prev, {
      role: 'assistant',
      content: response.choices[0].message.content,
      metadata: {
        model: response.model,
        cost: response.cost_usd,
        time: response.response_time_ms
      }
    }]);
  };

  return (
    <View style={{ flex: 1 }}>
      {/* Optimize Mode Selector */}
      <SegmentedControl
        values={['Cost', 'Speed', 'Quality']}
        selectedIndex={['cost', 'speed', 'quality'].indexOf(optimize)}
        onChange={(index) => setOptimize(['cost', 'speed', 'quality'][index])}
      />

      {/* Message List */}
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <MessageBubble
            message={item}
            isUser={item.role === 'user'}
          />
        )}
      />

      {/* Input */}
      <View style={{ flexDirection: 'row' }}>
        <TextInput
          value={input}
          onChangeText={setInput}
          placeholder="Ask anything..."
        />
        <Button title="Send" onPress={sendMessage} />
      </View>
    </View>
  );
}
```

---

## 🔔 **Push Notifications**

```typescript
// notifications/pushNotifications.ts
import * as Notifications from 'expo-notifications';

export const setupNotifications = async () => {
  const { status } = await Notifications.requestPermissionsAsync();

  if (status === 'granted') {
    const token = await Notifications.getExpoPushTokenAsync();

    // Register with Helix backend
    await helixAPI.notifications.register({
      push_token: token.data,
      platform: Platform.OS
    });
  }
};

// Notification types
export const NotificationTypes = {
  WORKFLOW_COMPLETE: 'workflow.complete',
  WORKFLOW_FAILED: 'workflow.failed',
  USAGE_THRESHOLD: 'usage.threshold',
  PAYMENT_SUCCEEDED: 'payment.succeeded',
  NEW_FEATURE: 'feature.new'
};

// Handle notification
Notifications.addNotificationReceivedListener((notification) => {
  const { type, data } = notification.request.content.data;

  switch (type) {
    case NotificationTypes.WORKFLOW_COMPLETE:
      Alert.alert('Workflow Complete', `${data.workflow_name} finished in ${data.duration_ms}ms`);
      break;

    case NotificationTypes.USAGE_THRESHOLD:
      Alert.alert('Usage Alert', `You've used ${data.percentage}% of your daily limit`);
      break;

    case NotificationTypes.PAYMENT_SUCCEEDED:
      Alert.alert('Payment Successful', `$${data.amount} charged for Pro tier`);
      break;
  }
});
```

---

## 🎨 **Design System**

```typescript
// theme/colors.ts
export const Colors = {
  primary: '#6366f1',
  primaryDark: '#4f46e5',
  secondary: '#ec4899',
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  dark: '#0f172a',
  darkCard: '#1e293b',
  gray: '#64748b',
  light: '#f8fafc'
};

// theme/typography.ts
export const Typography = {
  h1: { fontSize: 32, fontWeight: '800' },
  h2: { fontSize: 24, fontWeight: '700' },
  h3: { fontSize: 20, fontWeight: '600' },
  body: { fontSize: 16, fontWeight: '400' },
  caption: { fontSize: 14, fontWeight: '400' }
};

// components/Card.tsx
export const Card = ({ children }) => (
  <View style={{
    backgroundColor: Colors.darkCard,
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  }}>
    {children}
  </View>
);
```

---

## 📦 **Tech Stack**

```json
{
  "name": "helix-mobile",
  "version": "1.0.0",
  "dependencies": {
    "react-native": "^0.73.0",
    "expo": "^50.0.0",
    "react-navigation": "^6.0.0",
    "@react-native-async-storage/async-storage": "^1.21.0",
    "@react-native-voice/voice": "^3.2.4",
    "expo-camera": "^14.0.0",
    "expo-notifications": "^0.27.0",
    "react-native-chart-kit": "^6.12.0",
    "axios": "^1.6.0",
    "react-native-webview": "^13.6.0"
  }
}
```

---

## 🚀 **Launch Strategy**

### **Phase 1: Soft Launch (Week 1-2)**
- Beta on TestFlight (iOS) + Google Play Beta
- 50 beta testers from Discord
- Collect feedback, fix bugs

### **Phase 2: Public Launch (Week 3)**
- App Store + Google Play submission
- Product Hunt mobile launch
- Tweet: "Helix is now in your pocket. AI agents + workflows on mobile."

### **Phase 3: Growth (Month 2-3)**
- In-app referral program (share QR code = free month Pro)
- App Store featuring campaign
- Integration with iOS Shortcuts + Android Tasker

---

## 💰 **Revenue Impact**

**Mobile-Only Features (In-App Purchases):**
- Voice agent execution: $4.99/month
- Unlimited push notifications: $2.99/month
- Offline mode (cached responses): $9.99/month

**Estimated Revenue:**
- 1,000 mobile users @ 10% IAP conversion = $500/month additional
- 40% higher retention (push notifications = engagement)

---

## 📊 **Analytics**

```typescript
// analytics/tracking.ts
import Analytics from '@segment/analytics-react-native';

export const trackEvent = (event: string, properties: object) => {
  Analytics.track(event, properties);
};

// Track everything
trackEvent('Agent Executed', {
  agent_id: 'kael',
  task: 'document',
  input_length: 450,
  cost_usd: 0.0025,
  platform: 'mobile'
});

trackEvent('Workflow Triggered', {
  workflow_id: 'email-handler',
  trigger_type: 'manual',
  platform: 'mobile'
});
```

---

## 🎯 **Next Steps**

1. **Week 1:** Set up React Native project + basic navigation
2. **Week 2:** Build dashboard + chat screens
3. **Week 3:** Agent execution + voice input
4. **Week 4:** Workflow monitoring + push notifications
5. **Week 5:** Beta testing (50 users)
6. **Week 6:** App Store + Google Play submission

---

**Competitive Advantage:** First AI agent platform with full mobile access

**Tat Tvam Asi** 🌀
