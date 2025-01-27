# Markdown Format Documentation

## Overview
The API accepts and exports hierarchical data in a specific markdown format that preserves relationships between objects.

## Basic Format
```markdown
# [@Type::UUID] **field1**: value1 **field2**: value2
```

Each line represents one object with:
- Hierarchy indicated by number of `#` characters
- Object type and UUID in `[@Type::UUID]` format 
- Fields as `**fieldname**: value` pairs

## Example
```markdown
# [@Client::550e8400-e29b-41d4-a716-446655440000] **name**: ACME Corp **context**: Global company
## [@Programme::663e8400-e29b-41d4-a716-446655440123] **name**: Sales Training
### [@Session::774e8400-e29b-41d4-a716-446655440456] **title**: Introduction
```

## Available Fields

### Client
- name
- context  
- objectives

### Programme
- name
- description

### Session
- title
- context
- objectives
- inputs
- outputs
- participants
- design_principles
- deliverables

### Sequence  
- title
- objective
- input_text
- output_text
- order

### BreakOut
- title
- description
- objective

## Usage Notes
1. Content must be on a single line per object
2. Use `[@Type::new]` for creating new objects
3. Use actual UUID for updating existing objects
4. Hierarchical relationships are maintained by heading levels
5. Field values cannot contain newlines (they will be automatically stripped)
6. The order of objects follows the hierarchy: Client → Programme → Session → Sequence → BreakOut