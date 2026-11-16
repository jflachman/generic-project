## Topic Summaries:

- Software Development
  - How do we do Vibe coding and spec driven development
  - Managing governance files – keep them short, move changelogs to other files
  - Can we automate secondary code reviews
  - Git commits, pull requests, keeping github up to date
  - How do we handle bugs/issues/feature request?
    - Use github issues or local files
  - LLM integrations
    - How do we make this LLM agnostic (use Agents.md vs Claude.md vs ???)
    - How do we use our pro/plus subscription rather than API tokens
    - Using free LLMs
  - How do we handle design interactions
    - Vibe code design -> spec
    - Questions during a prompts session that is working development
    - How do we insure LLM does not make decisions for us or assumptions.   is the right level of LLM design versus developer design
- AI Automation stack
  - How do we handle 
    - memory (obsidian, db, other)
    - agents (getbb, Hermes, paperclip, etc)
    - projects
    - LLMs
      - manage tokens and unexpected runaway agents
      - local LLMs – how can we use them – limited reasoning
      - How do we make it LLM agnostic
    - common skills repos

## Software Development Goals 

Tenats:
- Feed AI exactly what it needs and little extra.
- Provide facility for AI to keep detailed records in files that are not read often or ever. (Otherwise it will drift to do this on its own and clutter critical files with unecessary info)

1. Be able to handle a large project with sub-projects
   1. Sub-projects have their own git repo
2. Projects are comprised of 3 parts
   1. All the documents, prompts, work packages etc related to working with the AI to design and implement the projects
   2. All the governance files that define the product and insure it does not drift (architecture, ADRs, Specs, etc)
   3. All the Actual Code of the projects
3. In large complex projects should these three parts be separate?
   - For example, if you are going to share the code repo, should other have access to yuor design documents.  With the design documents they could re-implement your project from scratch relatively easily.  
   - If you share implementation and governance, do you want to share all your AI interactions and records
 4. How do we support multi AI development
    1. Agents.md
    2. Skills Files
 5. How do we handle related projects
    1. Enhancements - project A needs an enhancement from project B.  B should pick it up, complete the enhancement and notify A it is done so that A's related blocked work can proceed.
 6. Git integration
    1. How do we automate the git workflow - commit, push, PR, pull etc.
       1. Should different AIs support different parts.  i.e. AI A modifies code and commits.  B reviews the changes, pushes then, does the PR, pulls and refreshes main
    2. How do we handle github tokens so that the AI can make the changes
 7. Managing governance and state.  Claude likes to keep extensive records of changes.  It appends to design docs rather than updating, it add log information to frequently read files
    1. How do we keep critical files like AGENTS.md, STATE.md, TRACEABILITY.md stay clean and efficient.
    2. Do we create an equivalent log file for these and all governance files
    3. Do we direct that governance files are updated rather than appended and the change is kept in a separate change log file.
 8. Is there a way to manage critical files in a tree form (AGENTS.md, SKILLS, etc) with index files or summary files at the top of the tree and then branch to the appropriate detailed files
 9. Is there a way to create a DB for all the governance or SKILLS etc to make access very efficient.
 10. How do we do vibe coding and spec driven development in harmony