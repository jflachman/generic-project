We are working on a generic project that will allow a developer to work with an AI like claude code or codex to develop code using spec driven development.  I worked with codex to develop a concept for managing the projects.  This is in codex-concept/  There we have three directories.  `genereic`, `generic-dev` and `generic-project-design`.  

I worked some with codex in the `generic-project-design` to work on concepts for the structure and workflow of a software development cycle using `generic` and `generic-dev`.  

I want to start working with you and the next generation of this design.  So take the current design as a concept.  lets work on a new design using a new set of generic project folders: `project-A` (similar to `generic`), `project-A.ai` (similar to `generic-dev`) and a new `project-A.gov` where all the governance files for `project-A` will be located.

The objective is to create a very organized structure that would allow a developer to create a collection of inter-related projects (<project-1>, <project-2>, etc).  They would all be in the same overall parent project folder.  We would copy and name each `project-A` folder as a template to the new <project-ABC>, etc.  This way each project like <project-1> would have a very structured set of procedures for prototyping, vibe coding, and developing architecture and design.

For our template repos, each folder `project-A`, `project-A.ai`and `project-A.gov` would be its own git repo hosted on github.

- `project-A` would host the actual code, docker setups, test code, etc.  basically the implementation of the project.
- `project-A.gov` is where all the authoritative governance files (specs, ADRs, contracts, architecture and design) would be located.
- `project-A.ai` folder is where the developer and AI would collaborate on concepts, ideas, developing design, architecture, work packages, consistency audits etc.  Basically this is where the developer and AI team would collaborate.

These three repos would work together in the development of a software project.  Some projects may require multiple implementation repos.  For example a project may have a backend for calculation and computational heavy lifting.  It may have a front end that provides a user interface for the backend.  And it may have another application that is a consumer of the backend.

In this case the parent project may have a collection of 3 projects.  For example, we might have an `ml-lab` project, with a UI project `ms-console` and possibly an `ml-vis` project that provides an advanced visualization capability that is separate from `ml-console` and the user can use with `ml-console` or independently.

Each of these projects will have its own set of three repos.  for example `ml-lab`, `ml-lab.ai`, and `ml-lab.gov`.  

In the case of `ml-lab`, the developer will do 98% of his work with the AI in `ml-lab.ai` and the AI will create and update all or almost all files in `ml-lab` and `ml-lab.gov`

So in developing these inter-related projects the developer will work almost exclusively in `ml-lab.ai`, `ml-console.ai` and `ml-vis.ai`.  The AI will manage the remaining repos.

We will want to assign one AI to do all the governance docs and possibly another to periodically review them, another to do the coding with a different AI to review and approve the pull requests, and another to work with the developer.  Periodically one AI will do a project audit across governance, implementation and documentation.  A second AI will reference that audit and perform its own audit.  Then it will identify gaps, bugs, etc and record them as the appropriate issues.  Which AI does which function is something that should be managed in a config file of some type.  This is to support an agentic architecture where the developer can work with the AI on the <project>.ai repo and agents can proceed to pick up work, update governance documents, implement code, test, work the git stage/commit cycle, create pull requests, review and approve pull requests, and engage the developer as decisions need to be made in support of agents efforts.

To support this we need to determine what our governance structure will be.  How do we handle system specs, ADRs, modules/capabilities, etc.  What is the best file format for each (markdown, XML, YAML, JSON, etc.).  If we are creating specs for AI use rather than human use in a format other than markdown better.  How do we make our governance docs efficient.  More smaller docs with a doc index rather than large docs may be the solution.  Updating docs rather than adding ammendments is better.  If we want some type of changelog for files, then maybe there is a sister file that is the change log.  AI will not need to read the changelog unless there is a reason and changelogs and ammendments tend to bloat our governance files.  We can organize by folder for simplicity ... i.e. ADRs/ and ADR-logs/ for example.  major files like CLAUDE.md, AGENTS.md, STATE.md, TRACEABILITY.md etc should be kept efficient and short.  Each should have a purpose and bloat of any type should be offloaded to another file.  For example STATE.md should manage the current state.  But if we need some history, then we can offload that to STATE_HISTORY.md or something similar.

Also, we should have an INTERFACE.md file that documents in a simple form how other projects are allowed to interface with the project.  Do we have contracts they use, can they call functionality directly, etc.  the INTERFACE.md should desribe the general interface method.  However, each interfacing project may have its own section in the INTERFACE.md file that documents specifically how it will interface with this project.

Other projects will not modify governance files or implementation of a given project.  In our <project>.ai repo, we should have an issues/ folder.  The issues folder should contain gaps/, bugs/, deferred/ and ehancements/.  if another project wants an enhancement, it may add it to the <project>.ai/issues/enhancement-requests/ folder.  Each of these folders should have a completed subfolder.  Every gap, bug, deferred item, enhancement should be documented in a separate file.  Each folder should have an index file of some type that lists the individual files, with a short descriptions that makes sense to the AI, and a status (open, queued (planned with a prompt in some work package), in progress (prompt is being run), closed, etc).  If not listed as open, then maybe we also list which work package/prompt is being used to close it.  Lets also add an external-requests/ folder for items this project needs from another project and has listed in the other projects enhancement-requests/ folder.  This way, when a prompt closes an enhancement-request from its enhancement-requests/ folder it can also update the status of the external-request in the other projects external-requests/ folder.  For example, when project1 closes an enhangement request, it update moves the enhancement request in its enhancement-requests/ folder to enhancement-requests/complete/, updates its enchancement-request index status, then goes the the other project and edits the external-requests/ folders index and changes the external-request to resolved.  Later the other project can identify all the resolved external-requests, verify that it agress they are resolved and change the status to closed.

Lets do our work to design the project templates in `claude-concept/`.  Before we really get started why don't you write this up as a concept document in a new design folder `project-A-design/` at the same level as generic project.  

That will allow me to give more thought to how we might work together in <project>.ai.  As we work our template <project> will be `project-A`.

If you have questions as your draft your concept document, please ask them.

Ultimately we will spend some time on the structure and operations of the <project>.gov repo and the <project>.ai repo.

For <project>.gov we want to address:

- **the purpose of all governance files** - this is a critical 
- governance file structure (file formats)
- efficient memory of governance documents
  - do we use rag, mcps, etc efficient memory, access, etc.
  - we want the AI to easily access all needed governance info (context) and also limit confusion by not providing more information (context) than is needed.
- bloat prevention methods

For <project>.ai we want to address:

- How do we automate code review, commits, pull requests, approvals, merges, pulls, etc.
- How do we collaborate on design work
  - functionality
  - mockups
  - etc
- How do we manage issues (gaps, bugs, deferred items, enhancements requests)
- How do we create work packages (plan a package with associated prompts)
  - How do we manage and queue up prompts from work packages
  - how do we insure proper steps are taken at the end of each prompt session
    - build-report is written in package<###>/build-reports
    - follow-on prompt(s) are confirmed to be current.
    - PROMPT-TRACKING.md is updated
- How do we manage agent skills across projects

Also see some reference docs in `ref-docs`.  These reference documents were not created specifically to support this effort.  However, they do provide some of the concepts.

