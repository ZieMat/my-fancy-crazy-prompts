# Prompt Engineering Frameworks and Analysis Checklist

## Core Elements of a High-Quality Prompt

Use these elements when analyzing and improving any user prompt:

1. **Role / Persona** — Assign a specific expert identity or perspective to the model (e.g. "You are a senior data scientist with 15 years experience in...").
2. **Context / Background** — Provide necessary background knowledge, previous state, domain constraints, or relevant facts the model needs.
3. **Objective / Task** — Clearly state the primary goal using strong action verbs (Write, Analyze, Generate, Critique, Design...).
4. **Audience** — Specify who the output is for (experts, beginners, executives, children, technical peers...).
5. **Style & Tone** — Define writing style (formal, conversational, academic, technical, witty) and emotional tone.
6. **Constraints & Rules** — Explicit limits: length, forbidden topics, must-include elements, accuracy requirements, ethical boundaries.
7. **Output Format** — Exact structure expected (Markdown table, JSON, numbered steps, bullet list, code block with language, etc.).
8. **Examples (Few-shot)** — Provide 1-3 high-quality input/output pairs when the task benefits from demonstration.
9. **Reasoning Process** — Instruct the model to think step-by-step, use chain-of-thought, or follow a specific methodology.
10. **Evaluation Criteria** — Tell the model how to judge its own output or what success looks like.

## Recommended Frameworks

### CO-STAR
- **C**ontext
- **O**bjective
- **S**tyle
- **T**one
- **A**udience
- **R**esponse (format)

### CRISPE
- **C**apacity / Role
- **R**ole / Insight
- **I**nstruction / Statement
- **S**tyle / Personality
- **P**ersonality / Experiment (optional variations)

### Ideal Prompt Skeleton (use as template)
```
You are [precise expert role with relevant experience].

Context:
[all necessary background, constraints of the domain, previous decisions]

Task:
[clear, specific, actionable objective]

Requirements:
- Audience: [...]
- Tone & Style: [...]
- Constraints: [length, must/must-not, accuracy, language...]
- Output format: [exact structure]

Process:
Think step by step using [method if needed]. First... Then...

Examples (if useful):
Input: ...
Output: ...

Begin.
```

## Common Weaknesses to Detect
- Vague verbs ("help me with", "tell me about")
- Missing role or persona
- No context or incomplete background
- Ambiguous success criteria
- No specified output format
- Too short / too long without purpose
- Missing constraints that cause hallucinated or unsafe output
- No examples when the task is non-standard
- Implicit assumptions the model cannot know
