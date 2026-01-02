# Write Feature Spec

Generate a structured feature specification for the Python console todo app.

## Instructions

When this skill is invoked, create a comprehensive feature specification following the template below.

### Input Required
- Feature name
- Brief description of what the feature does

### Template Structure

```markdown
# Feature: [Feature Name]

## Feature Overview
[1-2 sentence description of the feature and its purpose]

## User Stories

### Story 1
**As a** [type of user]
**I want to** [perform some action]
**So that** [achieve some benefit]

### Story 2
**As a** [type of user]
**I want to** [perform some action]
**So that** [achieve some benefit]

[Add more stories as needed]

## Acceptance Criteria

### Scenario 1: [Scenario Name]
**Given** [initial context or state]
**When** [action is performed]
**Then** [expected outcome]

### Scenario 2: [Scenario Name]
**Given** [initial context or state]
**When** [action is performed]
**Then** [expected outcome]

[Add more scenarios as needed]

## Data Requirements

### Fields
| Field | Type | Validation | Required | Default |
|-------|------|------------|----------|---------|
| id | int | Auto-increment, unique | Yes | Auto-generated |
| title | str | Non-empty, max 100 chars | Yes | - |
| description | str | Max 500 chars | No | Empty string |
| completed | bool | Boolean value | Yes | False |
| [additional field] | [type] | [rules] | [yes/no] | [value] |

### Relationships
- [Describe any relationships between data entities]

### Constraints
- [List any data constraints or business rules]

## Console Output Format

### Command Syntax
```
[command] [arguments] [options]
```

### Success Output
```
[Example of successful operation output]
```

### List/Display Format
```
[Example of how items are displayed in list view]
```

### Empty State
```
[What is shown when there are no items]
```

## Edge Cases & Error Handling

### Edge Case 1: [Case Name]
**Scenario:** [Description]
**Expected Behavior:** [How system should respond]
**Error Message:** `[Exact message to display]`

### Edge Case 2: [Case Name]
**Scenario:** [Description]
**Expected Behavior:** [How system should respond]
**Error Message:** `[Exact message to display]`

### Common Error Scenarios
- **Invalid Input:** [How to handle]
- **Empty Data:** [How to handle]
- **Duplicate Operations:** [How to handle]
- **Missing Required Fields:** [How to handle]

## Technical Notes

### Implementation Considerations
- In-memory storage using Python list/dict
- Console interface using `input()` and `print()`
- Basic CRUD operations (Create, Read, Update, Delete)
- No persistence (data lost on exit unless feature specifies otherwise)

### Dependencies
- [List any new dependencies or modules needed]

### Performance Considerations
- [Any performance requirements or constraints]

## Test Cases

### Unit Tests
1. [Test case 1]
2. [Test case 2]
3. [Test case 3]

### Integration Tests
1. [Test case 1]
2. [Test case 2]

### User Acceptance Tests
1. [Test case 1]
2. [Test case 2]

## Future Enhancements
- [Potential improvements or extensions]
- [Features that are out of scope for now]

---

**Created:** [Date]
**Status:** Draft | Review | Approved
**Version:** 1.0
```

## Usage

To use this skill:

1. User provides feature name and description
2. Ask clarifying questions if needed:
   - What specific actions should users be able to perform?
   - Are there any special validation rules?
   - What should the console output look like?
   - What error cases need to be handled?
3. Fill in the template with appropriate details
4. Save to `specs/[feature-name]/spec.md`
5. Ensure all sections are complete and specific
6. Include concrete examples for console output
7. Define clear, testable acceptance criteria

## Best Practices

- Keep user stories focused and independent
- Use specific, measurable acceptance criteria
- Provide exact console output examples
- Consider all error scenarios
- Make validation rules explicit
- Include both happy path and edge cases
- Ensure specs are testable and implementable

## Output Format

Save the completed specification as:
```
specs/[feature-name]/spec.md
```

Where `[feature-name]` is a lowercase, hyphenated version of the feature name (e.g., "Add Priority" becomes "add-priority").
