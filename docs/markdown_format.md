# Markdown Format Documentation

The API accepts and returns data in a specific markdown format that preserves hierarchical relationships between objects.

## Format Specification

Each object is represented by a single line in the following format:
```markdown
# [@Type::UUID] **field1**: value1 **field2**: value2 **field3**: value3
```

### Key Elements

1. **Hierarchy Levels**: Indicated by the number of `#` characters
   - `#` - Top level (typically Client)
   - `##` - Second level (typically Programme)
   - `###` - Third level (typically Session)
   - `####` - Fourth level (typically Sequence)
   - `#####` - Fifth level (typically BreakOut)

2. **Object Declaration**: `[@Type::UUID]`
   - Type: The model name (Client, Programme, Session, etc.)
   - UUID: Either:
     - `new` for creating new objects: `[@Type::new]`
     - An existing UUID: `[@Type::550e8400-e29b-41d4-a716-446655440000]`

3. **Fields**: `**fieldname**: value`
   - Each field is enclosed in double asterisks
   - Field value follows after a colon and space
   - Multiple fields are separated by spaces

## Available Fields per Type

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

## Example

```markdown
# [@Client::550e8400-e29b-41d4-a716-446655440000] **name**: ACME Corp **context**: Global company **objectives**: Improve sales
## [@Programme::663e8400-e29b-41d4-a716-446655440123] **name**: Sales Training **description**: Comprehensive sales program
### [@Session::774e8400-e29b-41d4-a716-446655440456] **title**: Introduction **context**: Sales basics
#### [@Sequence::885e8400-e29b-41d4-a716-446655440789] **title**: Opening **objective**: Learn greeting **order**: 1
##### [@BreakOut::996e8400-e29b-41d4-a716-446655440012] **title**: Role Play **description**: Practice greetings
```

## Usage Notes

1. All content for an object must be on a single line
2. Field values cannot contain newlines (they will be automatically stripped)
3. Hierarchical relationships are automatically maintained based on the heading levels
4. When creating new objects, use `new` as the UUID and the API will generate a proper UUID
5. When updating existing objects, use their actual UUID