---
description: Analyze and optimize code performance
argument-hint: [file-path]
allowed-tools: [Read, Edit]
---

Analyze this code for performance optimization opportunities:

@$ARGUMENTS

## Optimization Analysis

1. **Algorithm Complexity**
   - Current time complexity (Big O)
   - Current space complexity
   - Optimization opportunities

2. **Memory Usage**
   - Memory allocation patterns
   - Potential memory leaks
   - Caching opportunities

3. **I/O Operations**
   - Database queries (N+1 problems, indexing)
   - Network calls (batching, caching)
   - File system operations

4. **Language-Specific Optimizations**
   - Built-in functions vs custom code
   - Data structure choices
   - Framework-specific patterns

5. **Recommendations**
   - Prioritized list of improvements
   - Expected performance gains
   - Code examples for top 3 optimizations
   - Trade-offs to consider

**Focus on**: High-impact, low-risk improvements first.
