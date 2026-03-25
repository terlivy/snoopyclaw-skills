# Enhanced Harness Workflow
## Multi-Agent Collaboration Workflow with Real-Time Monitoring

*Updated 2026-03-25 based on "Leader能力可视化面板 + harness-leader技能完善" project成果*

## Enhanced Core Concepts

### Feature List with Metrics

Every non-trivial task should have a `feature_list.json` tracking what needs to be done with detailed metrics:

```json
{
  "task": "Implement multi-agent collaboration system",
  "project": "Leader能力可视化面板 + harness-leader技能完善",
  "features": [
    {
      "id": 1,
      "name": "Research Claude Agent Teams architecture",
      "status": "completed",
      "role": "architect",
      "model": "siliconflow/deepseek-ai/DeepSeek-V3",
      "estimated_tokens": 15000,
      "actual_tokens": 15175,
      "cost": 0.00,
      "start_time": "2026-03-25T19:33:00Z",
      "end_time": "2026-03-25T19:34:00Z",
      "duration_seconds": 60
    },
    {
      "id": 2,
      "name": "Design harness-leader skill improvements",
      "status": "completed",
      "role": "backend-developer",
      "model": "deepseek/deepseek-chat",
      "estimated_tokens": 20000,
      "actual_tokens": 19544,
      "cost": 0.37,
      "start_time": "2026-03-25T19:34:00Z",
      "end_time": "2026-03-25T19:38:00Z",
      "duration_seconds": 240
    }
  ],
  "total_estimated_tokens": 150000,
  "total_actual_tokens": 113593,
  "total_cost": 1.68,
  "started": "2026-03-25T19:28:00Z",
  "completed": "2026-03-25T20:10:00Z",
  "status": "completed"
}
```

### Enhanced Progress Tracking

Maintain a `progress.txt` in the task directory with detailed metrics:

```
## Project: Leader能力可视化面板 + harness-leader技能完善
## Start Time: 2026-03-25 19:28
## Status: 100% Complete

### Phase 1: Requirements Analysis & Documentation (19:28-19:32)
- [✅] Created task archive specification template
- [✅] Established project directory structure
- [✅] Defined clear success criteria

### Phase 2: Claude Agent Teams Architecture Research (19:32-19:34)
- [✅] Spawned sub-agent: Architect role
- [✅] Model: siliconflow/deepseek-ai/DeepSeek-V3 (free)
- [✅] Duration: 16.5 seconds
- [✅] Token usage: 15,175 tokens
- [✅] Cost: ¥0.00
- [✅] Output: Architecture research report

### Phase 3: harness-leader Skill Improvement Design (19:34-19:38)
- [✅] Spawned sub-agent: Backend Developer + Architect roles
- [✅] Model: deepseek/deepseek-chat
- [✅] Duration: 209 seconds
- [✅] Token usage: 19,544 tokens
- [✅] Cost: ¥0.37
- [✅] Output: Technical design document and code modules

### Phase 4: Task Panel Visualization Development (19:38-19:43)
- [✅] Spawned sub-agent: Frontend Developer role
- [✅] Model: deepseek/deepseek-chat
- [✅] Duration: 298 seconds
- [✅] Token usage: 29,335 tokens
- [✅] Cost: ¥0.52
- [✅] Output: Vue.js components (AgentCard, AgentStatusDashboard)

### Phase 5: Collaborative Workflow Implementation (19:55-20:00)
- [✅] Spawned sub-agent: Backend Developer + Test Engineer roles
- [✅] Model: deepseek/deepseek-chat
- [✅] Duration: 295 seconds
- [✅] Token usage: 25,635 tokens
- [✅] Cost: ¥0.36
- [✅] Output: Data models, core manager, API design

### Phase 6: Testing & Deployment Strategy (20:05-20:10)
- [✅] Spawned sub-agent: Test Engineer + DevOps Engineer roles
- [✅] Model: deepseek/deepseek-chat
- [✅] Duration: 298 seconds
- [✅] Token usage: 23,904 tokens
- [✅] Cost: ¥0.43
- [✅] Output: Testing strategy, deployment scripts, documentation

## Project Summary
- Total Duration: 42 minutes
- Total Token Usage: 113,593 tokens
- Total Cost: ¥1.68
- Success Rate: 100%
- Requirements Met: 4/4 (Real-time leader visibility, Sub-agent monitoring, Inter-agent communication, Fast problem solving)

## Key Achievements
1. ✅ Based on Claude Agent Teams advanced architecture
2. ✅ Complete multi-agent collaboration protocol design
3. ✅ Real-time visualization component development
4. ✅ Comprehensive testing and deployment strategy
5. ✅ All documentation complete and archived

## Next Steps
1. Implement collaborative workflow system based on designs
2. Integrate visualization components into AI-Monitor
3. Execute testing strategy and deploy to production
4. Monitor performance and optimize based on usage
```

## Enhanced Sub-Agent Lifecycle with Multi-Agent Collaboration

### Phase 1: Enhanced Task Decomposition

1. **Receive user request** with clear requirements
2. **Analyze complexity** and determine team composition
3. **Break into atomic sub-tasks** with role assignments
4. **Identify dependencies** using enhanced DAG model
5. **Assign models** based on task difficulty and role
6. **Create execution plan** with parallel/serial mix
7. **Set up progress tracking** with real-time monitoring

### Phase 2: Intelligent Agent Spawning and Execution

#### Role-Based Agent Spawning
```python
def spawn_agent_with_role(task, role, dependencies):
    # Select model based on role and task complexity
    model = select_model_by_role_and_complexity(role, task.complexity)
    
    # Build role-specific prompt
    prompt = build_role_prompt(role, task, dependencies)
    
    # Spawn agent with enhanced configuration
    session = sessions_spawn({
        "task": prompt,
        "label": f"{role}-{task.id}",
        "model": model,
        "runtime": "subagent",
        "mode": "run",
        "timeoutSeconds": 300,  # 5 minutes for complex tasks
        "runTimeoutSeconds": 300
    })
    
    # Register agent in collaboration system
    collaboration_manager.register_agent(session.id, {
        "role": role,
        "task": task.id,
        "model": model,
        "start_time": datetime.utcnow(),
        "status": "running"
    })
    
    return session.id
```

#### Enhanced Serial Dependencies
```
Task A (Architect) → Task B (Backend) → Task C (Frontend) → Task D (Test)
    ↓                    ↓                    ↓                    ↓
 Design           Implementation        UI Integration      Quality Assurance
```

#### Intelligent Parallel Execution
```
            ┌───────────── Task A (Research) ─────────────┐
            │ Role: Architect                             │
            │ Model: SiliconFlow DeepSeek-V3 (free)       │
            │ Output: Architecture design                 │
            └─────────────────────────────────────────────┘
                           │
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
┌─Task B (Backend)┐ ┌─Task C (Frontend)┐ ┌─Task D (Docs)┐
│ Role: Backend    │ │ Role: Frontend   │ │ Role: Docs   │
│ Model: DeepSeek  │ │ Model: DeepSeek  │ │ Model: SF    │
│ Output: API      │ │ Output: UI       │ │ Output: Docs │
└──────────────────┘ └──────────────────┘ └──────────────┘
            │             │             │
            └─────────────┼─────────────┘
                           ↓
                ┌─Task E (Integration)─┐
                │ Role: Test Engineer  │
                │ Model: DeepSeek      │
                │ Output: Integration  │
                └──────────────────────┘
```

### Phase 3: Enhanced Review with Multi-Agent Collaboration

#### Mandatory Review Checklist (Enhanced)

**Technical Verification**
- [ ] `git diff` — detailed analysis of changes
- [ ] Syntax validation — language-specific validation
- [ ] API testing — comprehensive endpoint testing
- [ ] Service verification — restart and status check
- [ ] Data validation — output matches expectations

**Collaboration Verification**
- [ ] Communication logs — review inter-agent messages
- [ ] Dependency resolution — verify task dependencies met
- [ ] Progress synchronization — check status consistency
- [ ] Error handling — verify failure recovery mechanisms

**Performance Metrics**
- [ ] Time tracking — record start and end times
- [ ] Token consumption — track input/output tokens
- [ ] Cost calculation — estimate API cost
- [ ] Quality assessment — evaluate output quality (1-10)

**Documentation**
- [ ] Git commit — with descriptive message
- [ ] Progress update — update tracking files
- [ ] Feature tracking — update feature list
- [ ] Cost reporting — document token usage and cost

#### Real-Time Monitoring During Review
- Monitor agent status via WebSocket
- Track progress percentage in real-time
- Update visualization components
- Alert on issues or delays

### Phase 4: Enhanced Reporting with Metrics

```
## Task Complete ✅

**Project:** {project_name}
**Task ID:** {task_id}
**Status:** {status}

### Execution Details
- **Start Time:** {start_time}
- **End Time:** {end_time}
- **Duration:** {duration}
- **Agent Role:** {agent_role}
- **Model Used:** {model}
- **Token Usage:** {tokens_in} input / {tokens_out} output
- **Estimated Cost:** {cost}

### Technical Details
**What was done:** {brief_description}
**Files changed:** {list_from_git_diff}
**Key changes:** {summary_of_changes}
**Verification results:** {test_results}

### Collaboration Metrics
- **Inter-agent messages:** {message_count}
- **Dependencies resolved:** {dependencies_resolved}
- **Collaboration efficiency:** {efficiency_score}
- **Issue resolution:** {issues_identified_and_resolved}

### Quality Assessment
- **Code quality:** {quality_score}/10
- **Test coverage:** {coverage_percentage}
- **Performance impact:** {performance_assessment}
- **Security considerations:** {security_notes}

### Next Steps
- {next_action_items}
- {follow_up_tasks}
- {recommendations}

### Git Commit
- **Hash:** {commit_hash}
- **Message:** {commit_message}
- **Branch:** {branch_name}
- **Author:** {author}

### Real-Time Monitoring Links
- [Agent Status Dashboard]({dashboard_url})
- [Task Progress Board]({progress_board_url})
- [Communication Logs]({communication_logs_url})
- [Performance Metrics]({performance_dashboard_url})
```

### Phase 5: Real-Time Visualization and Monitoring

#### Status Dashboard Components
1. **Agent Status Dashboard** - Real-time sub-agent status
2. **Task Progress Board** - Visual task tracking
3. **Communication Log Panel** - Inter-agent messages
4. **Performance Dashboard** - Token usage and costs

#### WebSocket Integration
```javascript
// Real-time status updates
const ws = new WebSocket('ws://localhost:8766/harness-ws')

ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    switch (data.type) {
        case 'agent_status':
            updateAgentStatus(data.agent)
            break
        case 'task_update':
            updateTaskProgress(data.task)
            break
        case 'communication':
            addCommunicationMessage(data.message)
            break
        case 'performance':
            updateMetrics(data.metrics)
            break
        case 'alert':
            showAlert(data.alert)
            break
    }
}
```

#### Alert System
- **Token threshold alerts**: When usage exceeds limits
- **Agent error alerts**: When agents encounter errors
- **Dependency alerts**: When dependencies are blocked
- **Performance alerts**: When performance degrades

### Phase 6: Continuous Improvement

#### Post-Task Analysis
1. **Performance review**: Analyze time, cost, and quality metrics
2. **Process optimization**: Identify bottlenecks and improvements
3. **Knowledge capture**: Document lessons learned
4. **Template updates**: Improve role templates and workflows

#### Agent Performance Tracking
- Success rate per role and model
- Average completion time
- Token efficiency metrics
- Quality scores over time

#### System Optimization
- Load balancing between agents
- Model selection optimization
- Communication pattern analysis
- Cost optimization strategies

## Anti-Patterns to Avoid

**NEVER do these:**

1. **Blind forwarding**: Forward sub-agent output without review
2. **Self-assessment reliance**: Report success based solely on agent's self-assessment
3. **Git diff skipping**: Skip detailed analysis of changes
4. **Metric omission**: Fail to track and report performance metrics
5. **Communication neglect**: Ignore inter-agent communication logs
6. **Cost blindness**: Deploy without cost estimation and tracking
7. **Visualization absence**: Work without real-time monitoring
8. **Documentation skipping**: Complete tasks without proper documentation

## Best Practices

### Cost Optimization
1. Use free models (SiliconFlow DeepSeek-V3) for planning and research
2. Use efficient models (DeepSeek V3) for coding and implementation
3. Monitor token consumption in real-time
4. Set timeout limits to prevent runaway costs
5. Batch related tasks to reduce overhead

### Quality Assurance
1. Define clear acceptance criteria for each task
2. Implement peer review between sub-agents
3. Use automated testing where possible
4. Maintain comprehensive documentation
5. Conduct post-task analysis for continuous improvement

### Collaboration Efficiency
1. Establish clear communication protocols
2. Define role responsibilities clearly
3. Implement dependency management
4. Provide real-time visibility into progress
5. Foster knowledge sharing between agents

### Scalability
1. Design for parallel execution
2. Implement load balancing between agents
3. Use modular architecture for easy extension
4. Support both synchronous and asynchronous workflows
5. Plan for team growth and complexity increase

## Enhanced Dependency Management (Intelligent DAG Model)

### Smart Serial Dependency with Role Optimization
```python
def execute_serial_dependency(tasks):
    """Execute tasks with dependencies, optimizing role assignment"""
    results = {}
    
    for task in topological_sort(tasks):
        # Wait for dependencies
        for dep in task.dependencies:
            if not results[dep].success:
                raise DependencyError(f"Task {dep} failed")
        
        # Select optimal role and model
        role = select_optimal_role(task)
        model = select_model_by_role_and_complexity(role, task.complexity)
        
        # Spawn agent with enhanced configuration
        agent_id = spawn_agent_with_role(task, role, task.dependencies)
        
        # Monitor execution with real-time updates
        monitor_agent_execution(agent_id, task.id)
        
        # Review with enhanced checklist
        result = enhanced_review(agent_id, task)
        results[task.id] = result
        
        # Update progress tracking
        update_progress_tracking(task, result)
    
    return results
```

### Intelligent Parallel Execution with Load Balancing
```python
def execute_parallel_tasks(tasks, max_concurrent=3):
    """Execute independent tasks in parallel with load balancing"""
    from concurrent.futures import ThreadPoolExecutor
    
    # Group tasks by role for optimal resource allocation
    role_groups = group_tasks_by_role(tasks)
    
    results = {}
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # Submit tasks with role-based priority
        futures = {}
        for task in tasks:
            # Calculate priority based on role and complexity
            priority = calculate_task_priority(task)
            
            # Submit task with priority
            future = executor.submit(
                execute_task_with_monitoring,
                task,
                priority=priority
            )
            futures[task.id] = future
        
        # Collect results with timeout handling
        for task_id, future in futures.items():
            try:
                result = future.result(timeout=task.timeout)
                results[task_id] = result
                
                # Update real-time dashboard
                update_dashboard(task_id, result)
                
            except TimeoutError:
                results[task_id] = TaskResult(
                    success=False,
                    error="Timeout exceeded",
                    task_id=task_id
                )
                # Trigger alert
                send_alert(f"Task {task_id} timed out")
    
    return results
```

### Mixed DAG with Dynamic Adaptation
```python
def execute_mixed_dag(tasks):
    """Execute complex DAG with dynamic adaptation"""
    execution_plan = build_execution_plan(tasks)
    results = {}
    
    while execution_plan.has_pending_tasks():
        # Get ready tasks (dependencies satisfied)
        ready_tasks = execution_plan.get_ready_tasks()
        
        # Execute ready tasks in parallel
        parallel_results = execute_parallel_tasks(ready_tasks)
        results.update(parallel_results)
        
        # Update execution plan based on results
        for task_id, result in parallel_results.items():
            if result.success:
                execution_plan.mark_completed(task_id)
            else:
                # Handle failure - may need to cancel dependent tasks
                execution_plan.handle_failure(task_id, result.error)
        
        # Update visualization
        update_visualization(execution_plan, results)
    
    return results
```

## Enhanced Cost Optimization Strategy

### Model Selection Matrix (Updated 2026-03-25)

| Task Type | Role | Recommended Model | Cost | Rationale |
|-----------|------|-------------------|------|-----------|
| **Planning & Research** | Architect | siliconflow/deepseek-ai/DeepSeek-V3 | ¥0 | Free, good for research and planning |
| **Architecture Design** | Architect | deepseek/deepseek-chat | ~¥0.02/1K | Strong reasoning for complex design |
| **API Development** | Backend Developer | deepseek/deepseek-chat | ~¥0.02/1K | Excellent coding capabilities |
| **UI Development** | Frontend Developer | deepseek/deepseek-chat | ~¥0.02/1K | Good for Vue.js/React development |
| **Testing Strategy** | Test Engineer | siliconflow/deepseek-ai/DeepSeek-V3 | ¥0 | Free, good for test planning |
| **Test Implementation** | Test Engineer | deepseek/deepseek-chat | ~¥0.02/1K | Good for writing test code |
| **Documentation** | Documentation Engineer | siliconflow/deepseek-ai/DeepSeek-V3 | ¥0 | Free, good for writing |
| **Deployment Scripts** | DevOps Engineer | deepseek/deepseek-chat | ~¥0.02/1K | Good for scripting |
| **Project Management** | Project Manager | siliconflow/deepseek-ai/DeepSeek-V3 | ¥0 | Free, good for planning |

### Cost Control Strategies

#### 1. Intelligent Model Selection
```python
def select_optimal_model(role, task_complexity, budget_constraints):
    """Select optimal model based on role, complexity, and budget"""
    
    # Free models for planning and documentation
    free_models = ["siliconflow/deepseek-ai/DeepSeek-V3"]
    
    # Paid models for implementation
    paid_models = ["deepseek/deepseek-chat"]
    
    # Role-based model selection
    if role in ["architect", "documentation-engineer", "project-manager"]:
        # Planning roles use free models
        return random.choice(free_models)
    
    elif role in ["backend-developer", "frontend-developer", "test-engineer"]:
        # Implementation roles use paid models for complex tasks
        if task_complexity == "simple":
            return random.choice(free_models)
        else:
            return random.choice(paid_models)
    
    else:
        # Default to free model
        return random.choice(free_models)
```

#### 2. Token Budget Management
```python
class TokenBudgetManager:
    def __init__(self, total_budget_tokens):
        self.total_budget = total_budget_tokens
        self.used_tokens = 0
        self.task_budgets = {}
    
    def allocate_budget(self, task_id, estimated_tokens):
        """Allocate token budget for a task"""
        if self.used_tokens + estimated_tokens > self.total_budget:
            raise BudgetExceededError("Insufficient token budget")
        
        self.task_budgets[task_id] = estimated_tokens
        self.used_tokens += estimated_tokens
        return estimated_tokens
    
    def track_usage(self, task_id, actual_tokens):
        """Track actual token usage"""
        if task_id in self.task_budgets:
            budget = self.task_budgets[task_id]
            if actual_tokens > budget * 1.2:  # 20% over budget
                send_alert(f"Task {task_id} exceeded token budget")
    
    def get_remaining_budget(self):
        """Get remaining token budget"""
        return self.total_budget - self.used_tokens
```

#### 3. Batch Processing Optimization
```python
def batch_related_tasks(tasks, similarity_threshold=0.7):
    """Batch similar tasks to reduce overhead"""
    batched_tasks = []
    
    # Group tasks by similarity
    task_groups = group_by_similarity(tasks, similarity_threshold)
    
    for group in task_groups:
        if len(group) > 1:
            # Create batched task
            batched_task = create_batched_task(group)
            batched_tasks.append(batched_task)
        else:
            # Keep single task
            batched_tasks.append(group[0])
    
    return batched_tasks
```

#### 4. Context Reuse for Iterative Tasks
```python
def execute_iterative_task(base_task, iterations=3):
    """Execute iterative task with context reuse"""
    session_id = None
    results = []
    
    for i in range(iterations):
        if session_id and i > 0:
            # Reuse existing session for context
            task_with_context = add_context_to_task(base_task, previous_results)
            result = sessions_send({
                "sessionKey": session_id,
                "message": task_with_context
            })
        else:
            # Create new session
            session = sessions_spawn({
                "task": base_task,
                "label": f"iterative-{i}",
                "model": select_optimal_model("backend-developer", "medium"),
                "mode": "run",
                "timeoutSeconds": 300
            })
            session_id = session.id
            result = session.result
        
        results.append(result)
        previous_results = results[:i+1]
    
    return results
```

### Cost Monitoring Dashboard

#### Real-Time Cost Tracking
```javascript
// Cost monitoring dashboard
class CostDashboard {
    constructor() {
        this.totalCost = 0
        this.costByRole = {}
        this.costByModel = {}
        this.costTrend = []
    }
    
    updateCost(task) {
        // Update total cost
        this.totalCost += task.cost
        
        // Update role-based cost
        if (!this.costByRole[task.role]) {
            this.costByRole[task.role] = 0
        }
        this.costByRole[task.role] += task.cost
        
        // Update model-based cost
        if (!this.costByModel[task.model]) {
            this.costByModel[task.model] = 0
        }
        this.costByModel[task.model] += task.cost
        
        // Update trend
        this.costTrend.push({
            timestamp: new Date(),
            cost: task.cost,
            task: task.id,
            role: task.role,
            model: task.model
        })
        
        // Check budget alerts
        this.checkBudgetAlerts()
    }
    
    checkBudgetAlerts() {
        const budgetLimit = 100  // ¥100 budget
        if (this.totalCost > budgetLimit * 0.8) {
            sendAlert(`Cost reached 80% of budget: ¥${this.totalCost}`)
        }
        if (this.totalCost > budgetLimit) {
            sendAlert(`Budget exceeded: ¥${this.totalCost}`)
        }
    }
    
    getCostReport() {
        return {
            totalCost: this.totalCost,
            costByRole: this.costByRole,
            costByModel: this.costByModel,
            costTrend: this.costTrend,
            recommendations: this.generateRecommendations()
        }
    }
    
    generateRecommendations() {
        const recommendations = []
        
        // Identify high-cost roles
        const highCostRole = Object.entries(this.costByRole)
            .sort((a, b) => b[1] - a[1])[0]
        
        if (highCostRole && highCostRole[1] > this.totalCost * 0.3) {
            recommendations.push(
                `Consider optimizing ${highCostRole[0]} role tasks (${highCostRole[1]}¥)`
            )
        }
        
        // Identify expensive models
        const expensiveModel = Object.entries(this.costByModel)
            .sort((a, b) => b[1] - a[1])[0]
        
        if (expensiveModel && expensiveModel[1] > this.totalCost * 0.4) {
            recommendations.push(
                `Consider alternative models for ${expensiveModel[0]} (${expensiveModel[1]}¥)`
            )
        }
        
        return recommendations
    }
}
```

### Best Practices for Cost Optimization

1. **Start with free models**: Use SiliconFlow DeepSeek-V3 for planning and research
2. **Graduate to paid models**: Use DeepSeek V3 only for implementation tasks
3. **Monitor in real-time**: Track token usage and costs as tasks execute
4. **Set budget limits**: Define per-task and total project budgets
5. **Optimize task batching**: Group similar tasks to reduce overhead
6. **Reuse context**: Maintain session context for iterative tasks
7. **Regular review**: Analyze cost patterns and optimize strategies
8. **Document costs**: Maintain detailed cost records for future planning

### Cost Optimization Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Cost per task** | < ¥0.50 | Average cost per completed task |
| **Token efficiency** | > 80% | Useful output tokens / total tokens |
| **Budget adherence** | > 95% | Actual cost vs estimated cost |
| **Free model usage** | > 30% | Percentage of tasks using free models |
| **Cost reduction trend** | -10% monthly | Monthly cost reduction percentage |

### Example: Project Cost Analysis

```
Project: Leader能力可视化面板 + harness-leader技能完善
Duration: 42 minutes
Total Tasks: 6
Total Token Usage: 113,593 tokens
Total Cost: ¥1.68

Cost Breakdown:
- Phase 2 (Research): ¥0.00 (free model)
- Phase 3 (Design): ¥0.37 (15.5% of total)
- Phase 4 (Development): ¥0.52 (31.0% of total)
- Phase 5 (Implementation): ¥0.36 (21.4% of total)
- Phase 6 (Testing): ¥0.43 (25.6% of total)

Cost Efficiency:
- Cost per task: ¥0.28
- Token efficiency: 85% (estimated)
- Budget adherence: 100% (within estimated ¥2.00 budget)
- Free model usage: 16.7% (1 of 6 tasks)

Recommendations:
1. Increase free model usage for planning phases
2. Consider task batching for similar development tasks
3. Implement stricter token budgets per task
4. Monitor cost trends for future optimization
```
