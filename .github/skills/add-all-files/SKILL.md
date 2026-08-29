---
name: add-all-files
description: "Use when: you need to add all relevant files to a workspace, scaffold a project, or ensure a complete set of project artifacts exists before finishing a task."
---

Related skill: `agent-customization`. Use this workflow for project setup, workspace completion, and file creation tasks that need a complete, verifiable project structure.

# Add All Files

## Purpose

Use this skill when the user wants the workspace to contain the complete set of relevant files for a task, feature, or project. The goal is not to create random files, but to add every necessary artifact needed for the work to be coherent, usable, and easy to verify.

## Decision Flow

1. Identify the task type
   - New project or feature scaffold: create the full project structure.
   - Existing project: add missing files only, preserving current structure and conventions.
   - Documentation-heavy work: add the docs, config, and setup files required to make the project understandable.

2. Inventory the workspace
   - List the current files and directories.
   - Check whether this is a minimal repo, a starter scaffold, or a partially complete implementation.
   - Decide which files are required versus optional.

3. Determine the minimum complete set
   - Include the core files needed for the task to be runnable or reviewable.
   - Prefer standard project conventions over custom one-off layouts.
   - For code projects, include the main source, config, dependency manifest, and a basic entry point when appropriate.
   - For docs or prompt workflows, include the main guidance file plus any related assets.

4. Create or update files
   - Add missing files with sensible defaults.
   - Edit existing files only when necessary to preserve consistency.
   - Avoid creating placeholder or duplicate content that does not serve the project.

5. Validate the result
   - Confirm the final structure matches the intended scope.
   - Check for broken paths, missing imports, and malformed configuration.
   - Run the smallest relevant validation command or syntax check when possible.

## Standard Workflow

### 1. Inspect the starting point
- Read the repo root and any existing docs.
- Note whether the project is empty, partial, or already established.
- Identify the user goal and the minimal file set required to satisfy it.

### 2. Decide scope
- If the project is empty, add the foundational files and a sensible starter layout.
- If the project already exists, add only the missing files and keep the current conventions.
- If the user asks for a complete implementation, include tests, configuration, docs, and entry points when relevant.

### 3. Add files in a logical order
- Start with the root context: README, config, and package/dependency files.
- Then add the primary implementation files.
- Then add supporting assets such as tests, docs, or environment files.
- Finish with any cleanup or final verification tasks.

### 4. Use a completion checklist
Before concluding, ensure all of the following are true:
- The file set is complete for the requested task.
- Existing files were not unnecessarily overwritten.
- The structure is consistent and easy to navigate.
- Any required configuration is present and valid.
- The project can be started, tested, or reviewed without obvious blockers.

## Quality Bar

A task is complete when:
- all relevant files are present;
- the workspace is internally consistent;
- there are no obvious omissions or broken references;
- the result is ready for the next stage of use, review, or execution.

## Example prompts

- "Add all the files needed for a Python CLI project with README, requirements, and app entry point."
- "Add the missing files for this repo while preserving the existing structure."
- "Create a complete starter project structure for a Streamlit app and include the key configuration files."
- "Review the workspace and add all necessary files to make this project runnable."

## Related customizations

- Create a project-specific instruction file for repo conventions.
- Add a prompt for scaffolding a new feature or app.
- Create a custom agent if this workflow needs stricter tool limits or multi-stage validation.
