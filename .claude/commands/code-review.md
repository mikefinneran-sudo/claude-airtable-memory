---
description: Perform thorough code review
argument-hint: [file-path or @file]
allowed-tools: [Read, Grep]
---

Perform a comprehensive code review of:

$ARGUMENTS

## Review Focus Areas

1. **Bugs & Logic Errors**
   - Logical flaws
   - Edge case handling
   - Error handling completeness

2. **Security Issues**
   - Input validation
   - Authentication/authorization
   - Data exposure risks
   - Injection vulnerabilities

3. **Performance**
   - Algorithm efficiency
   - Memory usage
   - Database query optimization
   - Network calls

4. **Code Quality**
   - Readability and maintainability
   - Code duplication
   - Naming conventions
   - Comment quality

5. **Testing**
   - Test coverage gaps
   - Missing edge cases
   - Test quality

**Output**: Clear, actionable feedback with specific line numbers and code examples for improvements.
