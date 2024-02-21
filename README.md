# ele

_ele_ is an 'atomic' data structure pivotal to a dynamic, gradient-based and hyperparameter-focused NLP ecosystem. It facilitates the generation of emergent code, behavior, and content, along with domain-specific adaptations, genetic-functional-generational querying and prompting, and detailed logging of agentic activities, primarily for Large Language Models (LLMs) running on consumer grade hardware.

### element+procedural_text+logic:

`${{ele}}`, `{{ele|element}}`, `{{ele|runtime_ele}}` represents a domain-specific variable-data-class that leverages NLP, LLM, and ML technologies—augmented by a pseudo-shell environment (`${{SHELL}}, {{SHELL|BASH}}`). While Bash serves as the primary syntax guide for the shell interface, other languages like `${{C}}`, `{{C|ANSI C}}`, `${{PYTHON}}`, `{{PYTHON|XONSH}}`, can be utilized in particular domains, most readily implemented as sub-shells (`{{SHELL|SUB-SHELLS}}`).

### feb 24 update
Microsoft has released the amazing UFO (don't like the name, haha) framework which allows, using vision+language processing, an addressable interface for agentic interaction within Windows. ele will only instantiate such agents, any agents, within the runtime windows ${{SANDBOX}}, {{SANDBOX|WSB}}. This is a very exciting development and will be the focus of the next major release of ele.

### why?

Ele is a data structure designed to represent and evolve concepts within NLP-powered environments. Here's what makes it unique:

* **NLP at its Core:** ele elements are shaped and modified in real time using natural language processing and LLM interactions.
* **Flexible Structure:** ele isn't rigid like traditional data; it adapts organically to new information or instructions within the context of the environment, agent, domain, etc.
* **Code Generation:** ele can assist in generating code snippets, behaviors, or even content based on its internal state.
* **Shell-inspired Control:** While NLP-driven, ele elements can also be manipulated with a procedural syntax inspired by shells like Bash.

### ::ele pseudo-markup+procedural_text+logic:
```
"""
// Placeholders and Variables:   
{{key}}: A placeholder for a variable or input value that will be replaced with actual content when used.
${{key}}: A variable or input value that is instantiated or declared and is only required once per variable. It is not replaced with content but serves to declare variables.

// Modifiers:
~{{key}}: Indicates an approximate value or range for the specified key. 
+{{key}}: Appends or concatenates the value of key with another element.
={{key}}: Specifies that the generated content should have an exact match or value equal to key.
!{{key}}: Negates or excludes the value of key from the generated content.  
-{{key}}: Removes or subtracts the value of key from the generated content.
*{{key}}: Specifies that the generated content should repeat the specified property or attribute key times.  
>{{key}}, <{{key}}, <={{key}}, >={{key}}: Define length comparisons for generated content.

// Conditional Expressions:
?{{key1}}{{key2}}: Used for conditional expressions, where if the condition specified by key1 is met, the generated content will include key2.

// Keywords:   
ANY, ALWAYS, NEVER, WITH, AND, ONLY, NOT, UNIQUE: Keywords that modify or constrain the generated content based on specific conditions.

// Functions:
between({{key1}}, {{key2}}): Specifies a range for a certain attribute or property in the generated content.  
random({{key1}}, {{key2}}, ...): Specifies that the generated content should include one of the provided keys at random.
mixed({{key1}}, {{key2}}, ...): Specifies that the generated content should include a combination of the provided keys.
contains({{key}}): Indicates that the generated content must contain the specified key.
optimize({{key}}): Suggests that the generated content should optimize for a certain aspect represented by the key.
limit({{key}}, {{value}}): Sets a limit on the number of times the specified key can appear in the generated content.

// Function Arguments:
fn(-{{key}}): Represents a function fn that takes the value of key as an input and removes or subtracts it from the generated content. 
fn(*{{key}}): Represents a function fn that takes the value of key as an input and repeats a specific property or attribute key times.
fn(?{{key1}}:{{key2}}): Represents a function fn that takes the values of key1 and key2 as inputs and includes key2 in the generated content if the condition specified by key1 is met.
"""
