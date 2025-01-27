# FlowAI Markdown Prompt Template

Use this template to structure prompts for AI models to generate content in FlowAI's markdown format.

## Template

```markdown
Convert the following input into a hierarchical markdown structure following these rules:

1. Each object must be on a single line starting with # symbols for hierarchy level
2. Object format: # [@Type::UUID] **field1**: value **field2**: value
3. Types and fields allowed:
   - Client: name, context, objectives
   - Programme: name, description
   - Session: title, context, objectives, inputs, outputs, participants, design_principles, deliverables
   - Sequence: title, objective, input_text, output_text, order
   - BreakOut: title, description, objective
4. Use "new" as UUID for new objects: [@Type::new]
5. Hierarchy must follow: Client → Programme → Session → Sequence → BreakOut
6. Each value must be on a single line (no newlines)

INPUT CONTEXT:
{Describe the scenario, client, program details etc.}

EXAMPLE OUTPUT:
```markdown
# [@Client::new] **name**: ACME Corp **context**: Global tech company **objectives**: Improve team collaboration
## [@Programme::new] **name**: Team Building 2025 **description**: Comprehensive team building program
### [@Session::new] **title**: Kick-off Meeting **context**: Remote team **objectives**: Set collaboration framework
#### [@Sequence::new] **title**: Ice Breaker **objective**: Team introduction **order**: 1
##### [@BreakOut::new] **title**: Two Truths One Lie **description**: Fun team activity
```

YOUR TASK:
Convert this input into FlowAI markdown format, maintaining all relationships and hierarchy:

{Insert the actual content to be converted}

Remember:
- Keep all content for each object on a single line
- Remove any newlines from field values
- Maintain proper hierarchy with #, ##, ###, etc.
- Include all relevant fields for each object type
- Use [@Type::new] for all new objects
```

## Usage Example

### Input Example
```
Create a training program for ACME Corporation focused on leadership development. 
The client is a global technology company with 5000 employees.
Their objective is to develop the next generation of leaders.

The program should include sessions on communication, strategic thinking, and team management.
Each session should have practical exercises and group activities.
```

### Expected Output
```markdown
# [@Client::new] **name**: ACME Corporation **context**: Global technology company with 5000 employees **objectives**: Develop next generation of leaders
## [@Programme::new] **name**: Leadership Development Program **description**: Comprehensive leadership training focusing on communication, strategy, and management
### [@Session::new] **title**: Effective Communication **context**: Leadership fundamentals **objectives**: Master leadership communication **inputs**: Communication basics **outputs**: Communication strategy
#### [@Sequence::new] **title**: Active Listening **objective**: Develop active listening skills **order**: 1
##### [@BreakOut::new] **title**: Role Play Exercise **description**: Practice active listening scenarios
```