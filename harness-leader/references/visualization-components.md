# Visualization Components for Multi-Agent Collaboration
## Real-Time Monitoring Interface Components

*Based on "Leader能力可视化面板 + harness-leader技能完善" project成果 (2026-03-25)*

## Overview

This document provides detailed specifications for visualization components that enable real-time monitoring of multi-agent collaboration systems. These components are designed to integrate with AI-Monitor and provide comprehensive visibility into agent status, task progress, communication, and performance.

## Component Architecture

### Four-Panel Layout Design
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 实时团队状态面板 (Agent Status Dashboard)                               │
├─────────────────────────────────────────────────────────────────────────┤
│ 智能体卡片网格 (3x2)                                                    │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                  │
│ │Agent1│ │Agent2│ │Agent3│ │Agent4│ │Agent5│ │Agent6│                  │
│ │运行中│ │空闲  │ │错误  │ │运行中│ │空闲  │ │运行中│                  │
│ │75%   │ │-     │ │!     │ │42%   │ │-     │ │89%   │                  │
│ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘                  │
├─────────────────────────────────────────────────────────────────────────┤
│ 任务进度看板 (Task Progress Board)                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ 甘特图 + 任务卡片列表                                                    │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 时间线: [===任务A===] [==任务B==] [========任务C========]           │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ 任务列表:                                                               │
│ 1. ✅ 任务A (完成)    2. 🔄 任务B (进行中 65%)  3. ⏳ 任务C (待开始)    │
├─────────────────────────────────────────────────────────────────────────┤
│ 通信日志面板 (Communication Logs)                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ 实时消息流 + 过滤器                                                     │
│ [19:45] Agent1 → Agent2: "任务数据已准备"                              │
│ [19:46] Agent2 → Agent3: "请求协助处理..."                             │
│ [19:47] System: "任务B进度更新至65%"                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ 性能监控仪表盘 (Performance Dashboard)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ Token消耗趋势图 + 负载均衡图 + 健康度指标                               │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐                                    │
│ │ 趋势图  │ │ 负载图  │ │ 健康度  │                                    │
│ │ Token   │ │ 各Agent │ │ 85%     │                                    │
│ │ 消耗    │ │ 负载    │ │         │                                    │
│ └─────────┘ └─────────┘ └─────────┘                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. AgentCard.vue - 智能体卡片组件

#### Features
- Real-time status indicator (running, idle, error, starting, stopping)
- Role-based color coding and icons
- Progress bar for current task
- Performance metrics (CPU, memory, token usage)
- Capability tags display
- Click interaction for details

#### Implementation
```vue
<template>
  <div class="agent-card" :class="cardClasses" @click="$emit('click', agent)">
    <div class="flex items-start gap-3">
      <!-- Agent Avatar with Status Indicator -->
      <div class="relative">
        <div class="avatar" :class="avatarClasses">
          <component :is="roleIcon" :class="iconColor" />
        </div>
        <div class="status-indicator" :class="statusIndicatorClasses" />
      </div>
      
      <!-- Agent Information -->
      <div class="flex-1">
        <div class="flex items-center gap-2">
          <span class="agent-name">{{ agent.name }}</span>
          <span class="role-badge" :class="roleBadgeClasses">
            {{ agent.role }}
          </span>
        </div>
        
        <!-- Current Task -->
        <div v-if="agent.currentTask" class="task-info">
          <div class="task-label">Current Task</div>
          <div class="task-name">{{ agent.currentTask }}</div>
        </div>
        
        <!-- Progress Bar -->
        <div v-if="agent.taskProgress > 0" class="progress-section">
          <div class="progress-header">
            <span>Progress</span>
            <span>{{ agent.taskProgress }}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: agent.taskProgress + '%' }" 
                 :class="progressBarClasses" />
          </div>
        </div>
        
        <!-- Performance Stats -->
        <div class="stats-grid">
          <div class="stat-item">
            <CpuIcon />
            <span>{{ agent.cpuUsage }}% CPU</span>
          </div>
          <div class="stat-item">
            <MemoryIcon />
            <span>{{ agent.memoryUsage }}% RAM</span>
          </div>
          <div class="stat-item">
            <BrainIcon />
            <span>{{ formatTokens(agent.tokensUsed) }}</span>
          </div>
          <div class="stat-item">
            <ClockIcon />
            <span>{{ formatUptime(agent.uptimeSeconds) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Capabilities -->
    <div v-if="agent.capabilities.length > 0" class="capabilities-section">
      <div class="capabilities-label">Capabilities</div>
      <div class="capabilities-tags">
        <span v-for="cap in agent.capabilities.slice(0, 3)" :key="cap.name"
              class="capability-tag" :class="capabilityClasses(cap.level)">
          {{ cap.name }}
        </span>
        <span v-if="agent.capabilities.length > 3" class="more-tag">
          +{{ agent.capabilities.length - 3 }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Cpu, MemoryStick, Brain, Clock, Users, Code, Palette, FileText, Calendar, Bug, Server, Crown } from 'lucide-vue-next'
import type { HarnessAgent, AgentRole, AgentStatus } from '../../types/harness-leader'

// Props and emits
const props = defineProps<{
  agent: HarnessAgent
}>()

defineEmits<{
  click: [agent: HarnessAgent]
}>()

// Role icons mapping
const roleIcons = {
  'leader': Crown,
  'frontend-dev': Code,
  'backend-dev': Server,
  'designer': Palette,
  'product-manager': FileText,
  'project-manager': Calendar,
  'tester': Bug,
  'devops': Server
}

const roleIcon = computed(() => roleIcons[props.agent.role] || Users)

// Status-based styling
const cardClasses = computed(() => {
  switch (props.agent.status) {
    case 'running': return 'status-running'
    case 'error': return 'status-error'
    case 'starting': return 'status-starting'
    case 'stopping': return 'status-stopping'
    default: return 'status-idle'
  }
})

// ... additional computed properties for styling
</script>

<style scoped>
.agent-card {
  @apply p-4 rounded-xl transition-all duration-300 hover:scale-[1.02] cursor-pointer backdrop-blur-sm;
}

.status-running {
  @apply bg-gray-900/50 border border-green-500/20;
}

.status-error {
  @apply bg-red-500/10 border border-red-500/30;
}

/* ... additional styles */
</style>
```

### 2. AgentStatusDashboard.vue - 团队状态面板

#### Features
- Grid layout of agent cards (responsive: 1-3 columns)
- Real-time connection status indicator
- Team statistics (total agents, active agents, system health)
- Status legend for quick reference
- Quick action buttons (refresh, add agent, view stats)

#### Key Sections
1. **Header**: Title, description, connection status
2. **Agent Grid**: Responsive grid of AgentCard components
3. **Statistics**: Real-time team metrics
4. **Legend**: Status color coding explanation
5. **Actions**: Control buttons for team management

### 3. TaskProgressBoard.vue - 任务进度看板

#### Features
- Gantt chart visualization of task timelines
- Task cards with detailed information
- Dependency relationship visualization
- Progress tracking and estimation
- Filtering and sorting capabilities

#### Data Model
```typescript
interface Task {
  id: string
  name: string
  description: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  priority: 'critical' | 'high' | 'medium' | 'low'
  progress: number  // 0-100
  assignedAgent: string | null
  estimatedDuration: number  // seconds
  actualDuration: number | null
  startTime: string | null
  endTime: string | null
  dependencies: string[]
  tokenCost: number
  createdAt: string
  updatedAt: string
}
```

### 4. CommunicationLogPanel.vue - 通信日志面板

#### Features
- Real-time message stream
- Message filtering by type, sender, receiver
- Search functionality
- Time-based grouping
- Message details on click

#### Message Types
1. **Task Updates**: Progress reports, status changes
2. **Help Requests**: Assistance requests between agents
3. **Data Sharing**: Data transfer notifications
4. **Status Reports**: Periodic status updates
5. **Error Messages**: Error notifications and debugging

### 5. PerformanceDashboard.vue - 性能监控仪表盘

#### Features
- Token usage trend chart
- Agent load distribution chart
- System health indicators
- Performance metrics over time
- Alert and warning notifications

#### Metrics Tracked
1. **Token Consumption**: Input/output tokens over time
2. **Agent Utilization**: Percentage of time agents are busy
3. **Task Completion Rate**: Success/failure statistics
4. **Response Times**: Average task completion time
5. **System Health**: Overall system status and errors

## Type Definitions

### Complete TypeScript Types
```typescript
// Agent-related types
type AgentRole = 'leader' | 'frontend-dev' | 'backend-dev' | 'designer' | 
                 'product-manager' | 'project-manager' | 'tester' | 'devops'

type AgentStatus = 'running' | 'idle' | 'error' | 'starting' | 'stopping'

interface AgentCapability {
  name: string
  level: 'expert' | 'proficient' | 'basic'
}

interface HarnessAgent {
  id: string
  name: string
  role: AgentRole
  status: AgentStatus
  capabilities: AgentCapability[]
  currentTask: string | null
  taskProgress: number
  tokensUsed: number
  tokensPerMinute: number
  lastActivity: string
  uptimeSeconds: number
  cpuUsage: number
  memoryUsage: number
}

// Task-related types
type TaskPriority = 'critical' | 'high' | 'medium' | 'low'

interface TaskDependency {
  taskId: string
  type: 'blocks' | 'depends_on' | 'related'
}

interface HarnessTask {
  id: string
  name: string
  description: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  priority: TaskPriority
  progress: number
  assignedAgent: string | null
  estimatedDuration: number
  actualDuration: number | null
  startTime: string | null
  endTime: string | null
  dependencies: TaskDependency[]
  subtasks: HarnessTask[]
  tokenCost: number
  createdAt: string
  updatedAt: string
}

// Communication types
type MessageType = 'task_update' | 'help_request' | 'data_share' | 
                   'status_report' | 'error'

interface CommunicationMessage {
  id: string
  timestamp: string
  sender: string
  receiver: string
  type: MessageType
  content: string
  metadata: Record<string, any>
  read: boolean
}

// Performance types
interface PerformanceMetrics {
  timestamp: string
  totalTokens: number
  tokensPerMinute: number
  taskCompletionRate: number
  averageTaskTime: number
  agentUtilization: number
  errorRate: number
  systemHealth: number
}

// Dashboard statistics
interface DashboardStats {
  totalAgents: number
  activeAgents: number
  totalTasks: number
  completedTasks: number
  totalTokens: number
  avgTaskTime: number
  systemHealth: number
}
```

## Integration with AI-Monitor

### 1. Extend AI-Monitor Types
Add harness-leader specific types to existing AI-Monitor type definitions.

### 2. Create Component Directory Structure
```
ai-monitor/frontend/src/components/harness-leader/
├── AgentStatusDashboard.vue
├── TaskProgressBoard.vue
├── CommunicationLogPanel.vue
├── PerformanceDashboard.vue
├── AgentCard.vue
├── GanttChart.vue
├── MessageStream.vue
└── index.ts
```

### 3. Update AI-Monitor Navigation
Add harness-leader dashboard to AI-Monitor navigation menu.

### 4. Integrate WebSocket Events
Extend existing WebSocket connection to handle harness-leader events.

## WebSocket Integration

### Event Types
```typescript
type HarnessEventType = 'agent_status' | 'task_update' | 'communication' | 'performance'

interface HarnessEvent {
  type: HarnessEventType
  data: any
  timestamp: string
}
```

### Event Handling
```javascript
// WebSocket connection setup
const ws = new WebSocket('ws://localhost:8766/harness-ws')

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  if (data.type === 'harness') {
    const harnessEvent = data as HarnessEvent
    
    switch (harnessEvent.type) {
      case 'agent_status':
        updateAgentStatus(harnessEvent.data)
        break
      case 'task_update':
        updateTaskProgress(harnessEvent.data)
        break
      case 'communication':
        addCommunicationMessage(harnessEvent.data)
        break
      case 'performance':
        updatePerformanceMetrics(harnessEvent.data)
        break
    }
  }
}
```

## Styling Guidelines

### Color Scheme
- **Primary**: Indigo (#6366f1) for active elements
- **Success**: Green (#10b981) for completed/running
- **Warning**: Yellow (#f59e0b) for warnings
- **Error**: Red (#ef4444) for errors
- **Neutral**: Gray (#6b7280) for idle/inactive

### Typography
- **Headings**: Inter, 16-24px, weight 600-700
- **Body**: Inter, 14-16px, weight 400
- **Monospace**: JetBrains Mono, 13px, for code/logs

### Spacing
- **Base unit**: 4px
- **Card padding**: 16px (4 * 4)
- **Grid gap**: 12px (3 * 4)
- **Section margin**: 24px (6 * 4)

### Responsive Design
- **Mobile**: 1 column, simplified views
- **Tablet**: 2 columns, basic features
- **Desktop**: 3-4 columns, full features

## Implementation Roadmap

### Phase 1: Core Components (1 week)
1. Implement AgentCard component
2. Create AgentStatusDashboard
3. Set up basic WebSocket integration
4. Integrate with AI-Monitor navigation

### Phase 2: Task Management (1 week)
1. Implement TaskProgressBoard
2. Add Gantt chart visualization
3. Create task dependency visualization
4. Implement task filtering and sorting

### Phase 3: Communication (1 week)
1. Implement CommunicationLogPanel
2. Add real-time message streaming
3. Create message filtering and search
4. Implement notification system

### Phase 4: Performance Monitoring (1 week)
1. Implement PerformanceDashboard
2. Add charts and graphs
3. Create alert system
4. Implement historical data viewing

### Phase 5: Optimization (1 week)
1. Performance optimization
2. Responsive design improvements
3. Accessibility enhancements
4. Documentation completion

## Best Practices

### Performance Optimization
1. **Virtual scrolling** for large lists
2. **Debounced updates** for frequent changes
3. **Cached computations** for expensive operations
4. **Lazy loading** for non-critical components

### Accessibility
1. **Keyboard navigation** support
2. **Screen reader** compatibility
3. **Color contrast** compliance
4. **Focus management** for interactive elements

### Maintainability
1. **Modular component** structure
2. **Comprehensive documentation**
3. **Type safety** with TypeScript
4. **Unit testing** for critical components

## Conclusion

These visualization components provide comprehensive real-time monitoring for multi-agent collaboration systems. By implementing these components, you can achieve full visibility into agent status, task progress, communication patterns, and system performance, enabling efficient management and optimization of multi-agent workflows.

*Based on implementation from "Leader能力可视化面板 + harness-leader技能完善" project (2026-03-