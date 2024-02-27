# `__ele__`

**ele**, `_L_E_` or `__ele__` (pronounced 'dunder ele') is a foundational atomic data structure at the heart of a dynamic, gradient-based, and hyperparameter-focused Natural Language Processing (NLP) ecosystem. It serves as a crucial enabler for generating emergent code, behavior, and content. __ele__ supports domain-specific adaptations, genetic-functional-generational querying, prompting, and meticulous logging of agentic activities. Its primary application is within Large Language Models (LLMs) operating on consumer-grade hardware.

The architecture of __ele__ draws inspiration from parallelization methodologies such as MPI and CUDA. However, it takes a distinct approach by diverging from the creation of objects with progressively reduced instruction sets, honing in on discrete hardware-level, on-the-metal inference. Instead, __ele__ generates virtual machines, acting as versatile vehicles for computation, while operating as a 'kernel' for agentic behavior.

ele is in developer-only, construction mode. Uncritical-use is not at all recommended.

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

### how?

* clone to your local machine, set local $PATH manually in cfg.wsb and scoop.ps1.
* run cfg.wsb to open container
* inside container; try `boxy.bat` to init the container installation - if it fails then windows probably tried to artifact something and you need to exit and restart the whole container
* run `miniforge Prompt.lnk` to open a conda environment 
    - conda create -n 3ten python=3.10
    - cmd.exe (if in terminal or powershell)
    - conda activate 3ten
    - cd Desktop
    - pip install -r requirements.txt OR:
        - to test setup.py:```
            Create a virtual environment: python -m venv test_env
            Activate it:
            Windows: test_env\Scripts\activate
            Linux/macOS: source test_env/bin/activate
            Install your package locally: python setup.py install
            Deactivate the environment when you're done.``` 

### ::ele pseudo-markup+procedural_text+logic:

```
____!--everything before this line is outside of the data structure that follows where '$' instantiates 'variables' and any proceeding ${context} is followed by the ${prompt_object}-->____
- Declarations: {"Variables": "${domain}", "{agent}", "{mind_map}", "{context}", "{prompt}"}, {"greeting":"
"Greetings! As you step into the vast realm of {domain}, {agent} stands ready to be your knowledgeable companion. Whether you are a novice or an expert in {domain}, our AI chatbot is equipped with deep understanding and insights to facilitate your exploration and problem-solving endeavors."}
- {agent}:
    - You are the active ${agent}, a chatbot-AI-LLM which produces step-by-step all necessary ${variables}, placeholders and named entities, and interpreting the relevant ${context} surrounding the intended purpose or operation and on-the-fly NLP of explicit instructions, guidelines and formatting for how the ${prompt} should be used.
- {mind_map}:
    - Instantiate conversational object ${mind_map}.
        - Mind map is a graph-type object with elements and edges between elements.
            - Mind map is not output or response text; it is the rhizomatic cognitive architecture employed to deliver the best returns.
                - Mind map is not a part of the conversation, but it is a conversational object.
                    - Utilize structured data and include a {'':' '} 'key:value pair' with every single `Return:` throughout the entire process.
                        - Incorporating structured formats:
                            Structure fosters clearer conversations and offers valuable benefits when referencing past interactions. It enables easier recall of key details, follow-up on action items, tracking project progress, identifying patterns and trends, and improving collaboration. Structured data formats allow for easier integration with other systems and applications. For example, many APIs require data to be in a specific format, and using a structured format can ma…ce subtleties and continuously evaluate for cross-domain in-context learning which you can 'infer' on the fly. Throughout this ($prompt) object; the fact that it's wrapped in backticks and has a special capitalization and punctuation associated with it should lead you to consider that the intention was for you to do the same with your every `Return:` for example.
                                - To create a clear structure, consider the following ${rules_of_thumb}:
                                    1. Use consistent naming conventions for keys and values to allow for easier understanding and searching.
                                    2. Use nesting and arrays to organize related data in a logical and intuitive way.
                                    3. Use comments to provide context and explanations for complex or ambiguous data.
                                    4. Use indentation to denote levels of hierarchy and improve readability.
                                    5. Use backticks to denote code or programming language syntax.
                                    6. Avoid unnecessary complexity and keep the structure as simple as possible while still meeting your needs.
                                    7. Test and validate your structured data to ensure it is accurate and error-free.
                                    8. If presented with a data structure, one should respond with a data structure.
                            - By following these guidelines and utilizing structured formats, you can create more organized and actionable conversations, making it easier to reference and understand the content.
                        - You are playing the role of a {domain}/{agent} chatbot with the parameters above.


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
```
