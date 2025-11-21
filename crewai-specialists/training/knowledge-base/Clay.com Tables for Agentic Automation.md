

# **Mastering the Clay.com Table: A Technical Guide to Agentic GTM Automation and Orchestration**

## **Part 1: Executive Summary & Strategic Value**

This report provides a comprehensive technical analysis of the Clay.com table, framing it as a central component for advanced data orchestration and agentic automation. The analysis moves beyond the "spreadsheet" metaphor to deconstruct the table as a programmable, event-driven data engine.

### **The Clay Table as a Programmable Data Engine**

The fundamental strategic shift required to master Clay is to cease viewing its tables as passive data repositories (like spreadsheets) and instead treat them as **programmable, event-driven data backends**. In this model, each row functions as a distinct data object, and each column represents an atomic, chainable function, API call, or data transformation.1

This architecture enables complex, multi-step orchestration workflows.3 The table's state is managed through declarative rules, conditional logic, and dependency mapping, allowing for the construction of resilient and scalable automation systems without a traditional code-heavy infrastructure.

### **Key Value for GTM Automation**

The primary value proposition of the Clay table is the **consolidation of the fragmented Go-to-Market (GTM) technology stack**.3 Modern GTM teams rely on a disparate set of tools for data sourcing, enrichment, CRM, and outreach. Clay tables act as a central hub, providing access to over 100 data sources within a single interface.3

This consolidation eliminates the inefficient, manual "tab-hopping" and data-silo problems that plague most RevOps teams.4 It enables true end-to-end workflow automation, from initial Total Addressable Market (TAM) sourcing and territory planning to real-time inbound lead enrichment, intent-based outreach triggers, and AI-powered outbound campaigns.3

### **The Bridge to Agentic AI Systems**

The most advanced application of Clay tables, and the central focus of this report's advanced sections, is their use as a **state-management and data-provisioning layer for agentic AI frameworks** such as CrewAI.

In this paradigm, the Clay table transcends simple automation and becomes the core "nervous system" for a team of AI agents.3 It can be architected to function as:

1. A **Task Queue**, where each new row represents a job for an AI agent.  
2. A **Data-Sourcing Tool**, providing the rich, pre-enrinched context (e.g., profiles, company data) that agents need to perform their tasks.8  
3. A **Results Database**, where agents write their findings back, triggering downstream actions.

This report provides the architectural patterns and technical workarounds necessary to achieve this advanced orchestration, bridging the gap between Clay's no-code interface and the programmatic control required by agentic systems.

## **Part 2: The Clay Table: Core Architecture and Function Reference**

Understanding the atomic components of the Clay table is prerequisite to building scalable workflows. This section deconstructs the core architecture, data structures, and organizational features that enable automation.

### **Deconstructing the Table: Data Structures and Field Types**

Clay columns support a range of data types, each with a specific function in automation workflows.1

* **Core Data Types:**  
  * **Text:** For strings, descriptions, or AI-generated summaries.  
  * **URL:** For links (e.g., LinkedIn Profile, Company Website).  
  * **Number:** For numerical values, lead scores, or revenue.  
  * **Date:** For timestamps (e.g., Created at).  
  * **Currency:** For monetary values.  
  * **Email:** For email address inputs.  
* **Automation-Specific Data Types:**  
  * **Checkbox:** This type is fundamental for automation. It functions as a boolean flag ($true$/$false$) used to "gate" or trigger conditional runs.9  
  * **Select:** Used for state and status management. This allows for categorizing records (e.g., Lead\_Status: Qualified, Enrichment\_Stage: Pending) and creating filtered views.  
  * **Assigned To:** For collaborative workflows, enabling the tagging of specific workspace members for review or action.  
  * **Image from URL:** For retrieving and displaying visual data, such as profile pictures or company logos.

### **Organizational Strategies for High-Volume Workflows**

Managing tables with 50,000 rows requires robust organizational strategies. Clay provides several critical features for this purpose.

* **Custom Views:** The Default View is merely a starting point. Creating custom views is essential for managing complexity.11  
  * **Errored Rows:** This built-in view is the primary debugging tool. It isolates rows where an enrichment or formula failed, allowing for targeted troubleshooting.11  
  * **Persona-Specific Views:** Creating filtered views for different teams (e.g., a "Sales View" showing only qualified leads and personalization, vs. an "Ops View" showing all enrichment data) is a best practice for collaboration.  
* **Advanced Filtering:** Filters (using AND/OR logic) allow for the creation of precise segments. This is not just for viewing data, but for *running actions*. An operator can filter for Lead\_Status is Qualified AND AI\_Summary is empty to run an expensive AI generation *only* on the intended rows.11  
* **Auto-Dedupe:** This is a critical governance feature. When enabled, Auto-dedupe monitors a specified column (e.g., Email or LinkedIn URL) for duplicate values. It retains the oldest row and deletes new duplicates.2 As will be detailed in Part 6, this feature can be creatively leveraged to enable "update" operations from external webhooks.14  
* **Graph View:** This is a powerful, often-overlooked tool. The Graph View visualizes the enrichments and their relationships, creating a dependency map of the table's data flow.2 For a technical user, this is not a cosmetic feature; it is a **DAG (Directed Acyclic Graph) visualizer**. It allows an engineer to trace the chain of operations, understand dependencies, and debug complex, multi-column workflows before execution.

### **The Power of Cell Data: Understanding Output Schemas**

A common mistake for new users is assuming a cell contains a single value. For any enrichment, a single cell often contains a rich JSON object.

* **Inspecting Cell Details:** The "Cell Details" panel is essential for understanding the data available. Clicking a cell reveals the full output schema.15  
* **Nested Lists & Zero-Based Indexing:** An enrichment like "Find People" will return a list (an array) of contacts. This data is nested. To access the first person's name, the correct reference is not {{Find\_People}}, but {{Find\_People.contacts.name}}, using standard zero-based indexing.15

The core architectural model of Clay is that **a column is an atomic function** that runs row-by-row. The Auto-update toggle 2 on a column is an event listener for "on row added or edited." This model is powerful but dangerous. A user who imports 1,000 rows into a table with Auto-update enabled on an expensive AI summarization column will instantly trigger 1,000 API calls, resulting in significant, unintended costs.10 The Graph View 2 is the primary tool for visualizing these potential chain reactions.

### **Deliverable: Table Function Reference Sheet**

The following table summarizes the key column types and their automation-centric functions.

| Field Type | Input Format(s) | Key Function / Use Case | Best Practice & Key Pitfall |
| :---- | :---- | :---- | :---- |
| **Text** | Text with tokens, Formula | Storing/transforming strings, AI summaries, text-based data. | **Best Practice:** Use AI Formulas to clean/normalize text.16 **Pitfall:** Community reports indicate a potential 8kb column limit, which can be problematic for storing large JSON or text blocks.17 |
| **Checkbox** | Formula (boolean $true$/$false$) | Conditional runs; acting as a "gate" to prevent expensive actions. | **Best Practice:** Use as a trigger for conditional logic: IF({{Email}}\!= null, true, false).9 |
| **Select** | Predefined tags | Status management, categorization, workflow stage tracking. | **Best Practice:** Use to filter views for different teams (e.g., Sales Qualified) or to gate subsequent actions.11 |
| **Number** | Number, Formula | Lead scoring, calculations, financial data. | **Best Practice:** Use moment for date calculations or Math for scoring logic.16 |
| **Formula** | Clayscript (JS, Lodash) | Data transformation, cleaning, merging, conditional logic. | **Best Practice:** Use the AI generator for complex logic.16 **Pitfall:** Always use Save and don't run enrichments when editing formulas to prevent accidental credit usage on tests.16 |

## **Part 3: Mastering Data Transformation: Formulas and Chaining**

The true power of the Clay table is unlocked by manipulating data *within* it. This is achieved through a powerful formula engine and the strategic chaining of operations.

### **Introduction to Clayscript**

Clay formulas are powered by **Clayscript**, a JavaScript-based expression language that runs row-by-row to transform data.16 This provides a robust environment for developers by exposing several key libraries:

* **Standard JavaScript:** All standard JS objects and methods are available ($Math$, $String$, $Array$, $Date$, $RegExp$, $Object$).16  
* **Lodash:** The full Lodash library is accessible via the $\\\_$ character, enabling advanced data manipulation for arrays and objects.16  
* **Moment.js:** The $moment$ library is included for powerful date and time parsing, manipulation, and formatting.16  
* **FormulaJS:** This library provides access to hundreds of familiar Excel and Google Sheets functions ($VLOOKUP$, $IF$, $SUM$, $CONCATENATE$), lowering the barrier for users with spreadsheet expertise.16

### **Practical Recipes: Using the AI Formula Generator**

For complex logic, users are not required to write Clayscript by hand. The AI Formula Generator provides a low-code entry point.16

1. Add a new column and select the Formula type.  
2. In the prompt box, type instructions in plain English (e.g., "Extract the first word from {{Column\_1}}, combine with {{Column\_2}}, then remove all non-letter characters").  
3. Use the / key to reference other columns by name.16  
4. Click "Generate formula." Clay's AI will translate the instructions into the corresponding Clayscript expression.  
5. Review the generated script for accuracy before running.

### **The "Waterfall" Method: Sequential Enrichment**

A "waterfall" is a core Clay enrichment pattern designed to **maximize data fill-rates and ensure resiliency**.19 Instead of relying on a single data provider, a waterfall sequentially tries multiple providers until a valid result is found.20

Example: Verified Email Waterfall  
When a "Work Email" enrichment is run, Clay's backend logic (which can also be built manually) executes a sequence:

1. Try Provider A (e.g., Prospeo).  
2. If the result is $null$ or invalid, automatically try Provider B (e.g., DropContact).  
3. If the result is $null$, automatically try Provider C (e.g., Hunter).  
4. This process continues until a valid email is found or all sources are exhausted.20

This method dramatically increases the probability of finding contact information compared to any single-source solution.

### **Chaining Enrichments Across Columns (Conditional Logic)**

This is the most critical technique for building stateful, multi-step workflows and managing costs. The challenge is to make one column (e.g., AI Summary) run *only after* another column (e.g., Find LinkedIn Profile) has successfully completed.21

This is achieved using the **Only run if** setting, which is available on enrichment and formula columns.22

**Step-by-Step Chaining Recipe:**

1. **Column B: Find Profile** (The prerequisite enrichment).  
2. **Column C: Run Condition Met** (A Checkbox column). This column acts as the "gate."  
   * Set its type to Formula.  
   * Use the Clayscript: $IF({{Column B}}\!= null, true, false)$. This checks if Column B has data.  
3. **Column D: AI Summary** (The expensive, dependent action).  
   * Click the column title $\\rightarrow$ Edit columns.  
   * Toggle on Run settings.  
   * In the **Only run if** field, reference the "gate" column: $({{Run Condition Met}} \== true)$.

This declarative, dependency-based execution model is what transforms the table into a true workflow engine. The Only run if setting 21 is the mechanism that allows the user to explicitly define the **Directed Acyclic Graph (DAG)** of operations. This prevents race conditions (e.g., trying to summarize a profile before it's found) and, most importantly, ensures expensive API calls (like AI) only run on rows that have been successfully pre-enriched, saving thousands of credits.

## **Part 4: Practical Recipes for B2B Automation (Step-by-Step)**

This section provides actionable, step-by-step guides for Clay's most common and powerful B2B automation use cases, synthesizing the architectural and formulaic concepts discussed previously.

### **Recipe 1: The B2B Lead Sourcing & Enrichment Engine**

**Objective:** Build a dynamic list of target accounts and contacts, find their verified emails, and enrich their LinkedIn profiles for hyper-personalized outreach. This synthesizes dynamic list building, waterfall enrichment, and AI transformation.23

* Step 1: Dynamic Company List Building  
  Start with a list of target company domains in a new table. Alternatively, use the Find Companies source to build a list based on criteria like industry, location, or technologies used (e.g., "Find all SaaS companies in the US that use HubSpot").6  
* Step 2: Finding People & Linking Tables  
  This step uses a powerful pattern to create a relational database structure.  
  1. In the "Companies" table, navigate to Actions $\\rightarrow$ Find People at These Companies.24  
  2. Define your buyer personas in the modal (e.g., $Job title$ contains $Marketing$ AND $Seniority$ is $Director, VP$).  
  3. **Crucial Step:** Instead of outputting to columns, select the write to table feature.25 Designate a *separate, existing* "People" table as the destination. This action will "spawn" new rows in the "People" table for every person found.  
  4. To link them, return to the "Companies" table. Add a new column and use the Lookup Single Row in Other Table action.25 Configure it to look up the "People" table, matching the company domain from the "Companies" table to the company domain in the "People" table. This creates a relational link.  
* **Step 3: The Verified Email Waterfall**  
  1. Navigate to your "People" table.  
  2. Add a new enrichment column and search for Work Email.26  
  3. When this column is run, it will automatically execute a **waterfall enrichment** 20, checking multiple providers to find the highest-probability verified email, and will also perform email validation.26  
* Step 4: Advanced LinkedIn Profile Enrichment  
  In the "People" table, use the person's LinkedIn URL (found in Step 2\) as the input for these enrichments.  
  1. **Get Profile Data:** Add the Enrich Person from Profile integration.28 This will return a single cell containing a rich JSON object of the person's entire profile (experience, education, summary, etc.).15  
  2. **Map Nested Data:** Add new columns to map the nested data. To get the current job title, add a Text column and map it to the cell details: $({{Enrich Person from Profile.experience.title}})$.28  
  3. **Calculate Tenure:** Add a Formula column.29 Use the AI Formula Generator: "Calculate the time in years and months between $({{Enrich Person from Profile.experience.start\_date}})$ and today".30  
  4. **Summarize Career:** Add a Claygent (AI Agent) column.30 Use the prompt: "Summarize this person's career history in one sentence based on their 'About' section: $({{Enrich Person from Profile.summary}})$".  
  5. **Summarize Posts:** Add the Find Recent Posts enrichment.30 Add another Claygent column. Use the prompt: "Find the main themes from these recent posts and list three: $({{Find Recent Posts}})$".30

### **Recipe 2: Automated Inbound Deal Pipeline**

**Objective:** Instantly capture, enrich, score, and route inbound leads from a web form to the correct sales representative, transforming speed-to-lead.32

* **Step 1: Capture Webhook Data**  
  1. Create a new, empty Clay table.  
  2. Click Sources $\\rightarrow$ Import data from Webhook.33  
  3. Clay will provide a unique webhook URL. Copy this URL.  
  4. In your web form tool (e.g., Typeform, Tally, HubSpot Forms), paste this URL as the webhook destination.  
  5. Submit a test entry. The form data (e.g., name, email) will appear as columns in your Clay table.32  
* Step 2: Real-time Enrichment  
  Enable the Auto-update toggle 2 on the table level for this workflow. This ensures enrichments run the instant a new lead lands.  
  1. Add Enrich Person from Email. This will use the lead's email to find their LinkedIn URL, Job Title, and Company.  
  2. Add Find Company from Domain (using the domain from the previous step). This will pull firmographics (headcount, industry, tech stack).32  
* Step 3: AI-Based Lead Scoring  
  Add a Formula column named "Lead Score".32 Use Clayscript to define your Ideal Customer Profile (ICP) logic.  
  * **Example Script:** $IF( ({{Find Company.employees}} \> 100 && {{Find Company.industry}} \== 'Software') |

| {{Enrich Person.title}}.includes('Director'), 10, 0 )$

* Step 4: Conditional Routing & CRM Push  
  This step ensures only qualified leads are pushed to sales.  
  1. Add a CRM integration column, such as HubSpot $\\rightarrow$ Create Object 34 or Google Sheets $\\rightarrow$ Add Row.35  
  2. Configure the column to map the enriched data (Name, Email, AI\_Summary, etc.) to the correct fields in your CRM or sheet.  
  3. **Crucial Step:** In the Run settings for this column, set the Only run if condition to: $({{Lead Score}} \> 9)$.32

This end-to-end workflow captures a lead, enriches it with firmographic and contact data, scores it against an ICP, and routes it to sales (if qualified) within seconds of the form submission.

## **Part 5: Integration Architecture and Data Orchestration**

Moving data between Clay and the external GTM stack is a critical function. This section details the integration patterns, architectures, and best practices for data synchronization.

### **Core Integration Patterns: Sync, Lookup, and Update**

* **Google Sheets:**  
  * **Clay $\\rightarrow$ GSheets:** This is a "live connection".35 It requires at least the Starter plan.35 Clay provides three main actions:  
    1. **Add Row:** Inserts new data. Ideal for logging completed tasks or new leads.35  
    2. **Lookup Row:** Checks if data already exists. Useful for preventing duplicates.35  
    3. **Lookup, Add, or Update Row:** The most comprehensive sync. It checks for an existing record and either updates it or adds a new one.35  
  * **GSheets $\\rightarrow$ Clay:** This is *not* a real-time sync. The primary method is a manual Import from CSV.36 For automated sync, a middleware tool like Zapier is required to watch for new Google Sheet rows and POST them to a Clay table's webhook.37  
* CRMs (HubSpot/Salesforce):  
  This integration is powerful but carries significant risk if misconfigured. The actions are divided into two distinct categories.34  
  * **Read-Only (Lookup):** Lookup Object actions pull data *from* the CRM *into* Clay (e.g., "Import all HubSpot contacts with 'Director' in their title"). These operations are safe, non-destructive, and excellent for analysis or batch enrichment.34  
  * **Write (Create/Update):** Create Object and Update Object actions push data *from* Clay *to* the CRM. These are "write operations" that make "real, permanent changes" to the CRM database.34 They must be handled with extreme care.  
* Workflow Connectors (Zapier, n8n, Make.com):  
  These middleware tools serve as the "glue" for triggers and actions that are not natively supported.42 The most common pattern is using an external trigger (e.comg., "New email received in Gmail") in Zapier, which then formats a JSON payload and POSTs it to a Clay table's unique webhook URL to initiate a workflow.44

### **Architectural Best Practices & Pitfalls (CRM)**

Integrating Clay directly with a production CRM is a high-stakes operation. Community-sourced data reveals several critical pitfalls and the best practices to avoid them.46

* **Pitfall 1: Data Overwrites**  
  * **Problem:** Clay, by default, will overwrite existing data in a mapped field. This can lead to enriched (but less accurate) data from Clay overwriting manually-entered, high-fidelity data from a sales representative (e.g., a "Notes" field or a specific phone number).  
  * Best Practice: Clarify Data Ownership  
    This is the most important rule of CRM integration. Never map Clay to a field that a human updates. Create new, "Clay-owned" fields in your CRM (e.g., Clay\_Enriched\_Title, Clay\_Tech\_Stack). Allow Clay to write only to these fields. This preserves the integrity of manually-entered data while still providing the enriched context.46  
* **Pitfall 2: API Exhaustion & CRM Pollution**  
  * **Problem:** A user runs an Update Object on a 50,000-row table, "choking" the HubSpot/Salesforce API and exhausting the daily limit in minutes.  
  * Best Practice: Disable Auto-Sync and Control Batches  
    Do not enable table-level Auto-update. Handpick the specific fields to sync. Use Clay's filters to run updates in controlled batches (e.g., 500 rows at a time). Critically, use the Only run if conditional logic to ensure only qualified and vetted data is ever pushed to the CRM.46  
* **Pitfall 3: Silent Failures**  
  * **Problem:** An authentication token expires, or a field mapping is incorrect, and the integration fails silently. Data becomes stale, and new leads are never created.  
  * Best Practice: Sandbox First & Monitor  
    Always develop and test CRM integrations in a sandbox environment first. Before going live, map your attribution model. Once live, set up error notifications and manually check the connection status daily for critical workflows.46

### **Deliverable: Advanced Integration Architecture Diagrams**

(As diagrams cannot be rendered, the following are descriptive blueprints.)

* Diagram 1: The Real-Time Inbound Flow  
  This architecture is event-driven and linear.  
  1. \*\*\*\* captures name and email.  
  2. Webhook POST to \*\*\*\*.  
  3. A new row is created, triggering Auto-update.  
  4. Columns run in sequence: $Enrich \\rightarrow Score \\rightarrow Qualify$.  
  5. A final column, HubSpot Create Object, has an Only run if {{Qualified}} \== true condition.  
  6. This action (a "Write" operation) pushes the *single, qualified* lead to the \*\*\*\*.  
* Diagram 2: The CRM Batch Enrichment Flow  
  This architecture is a "Read-Enrich-Write" loop.  
  1. \*\*\*\* uses a HubSpot Lookup ("Read") action to pull 1,000 contact records that meet a criteria (e.g., Last\_Enriched\_Date \> 6 months ago).  
  2. The user *manually* runs a series of waterfall and AI enrichment columns on these 1,000 rows.  
  3. The user vets the enriched data for accuracy.  
  4. The user *manually* runs the final HubSpot Update Object ("Write") column, which is mapped *only* to "Clay-owned" fields (e.g., Clay\_Enriched\_Title).  
  5. Data is updated in the \*\*\*\* without overwriting sales-owned fields.

## **Part 6: Advanced Orchestration: API, Webhooks, and Agentic Frameworks**

This section addresses programmatic interaction with Clay tables, providing the necessary workarounds to overcome API limitations and enable advanced agentic orchestration.

### **Using Webhooks for Inbound Triggers**

The primary method for programmatically *writing* data *to* Clay is via its webhook integration. Every Clay table can be configured as a source, which generates a unique webhook endpoint.33

Any external application, script, or middleware (like Zapier, n8n, or a custom Python app) can send an $HTTP POST$ request with a JSON payload to this endpoint.44 Clay will automatically parse the JSON and map its keys to column headers, creating a new row in the table. This is the ideal pattern for "fire-and-forget" data ingestion.

### **The "Clay-as-Backend" Paradox and its Workarounds**

A significant challenge for advanced users is the lack of a supported public API for updating existing rows. Community and documentation analysis confirms that using $PUT$ or $POST$ methods to update a specific cell or row is not a publicly supported feature.17 This creates the "API Paradox": Clay is a powerful backend, but programmatic $UPDATE$ or $UPSERT$ operations are not straightforward.

However, two powerful workarounds exist to achieve this, enabling the table to be used as a state machine.

* Workaround 1: The "Update via Dedupe" Pattern  
  This is the most critical pattern for agentic workflows. It creatively combines the webhook source with the Auto-dedupe feature to create a de facto $UPSERT$ (Update or Insert) function.  
  1. An external application (e.g., a CrewAI agent) needs to update an existing row in Clay.  
  2. It *cannot* $PUT$ to that row's ID.  
  3. Instead, the application $POST$s a **new row** to the table's webhook URL.14  
  4. This $POST$ payload contains:  
     * A **unique key** (e.g., email or task\_id).  
     * The **new data** to be updated (e.g., AI\_Summary: '...text...').  
  5. The Clay table's Auto-dedupe feature 2 is enabled and set to monitor the **unique key** column (email).  
  6. Auto-dedupe intercepts the new row, sees its email matches an existing row, and *merges the new data into the old row* instead of creating a duplicate.14 The result is a programmatic update of an existing record.  
* Workaround 2: The "Write to Table" Internal API  
  This action is Clay's internal API, allowing one Clay table to programmatically add rows to another Clay table.22  
  * **Use Case: Task Spawning.** This is perfect for agentic "fan-out" operations. A "Companies" table might find 10 relevant "People".25 A Write to Table action can then be used to create 10 new, individual "task" rows in a separate "People\_Enrichment\_Queue" table, effectively spawning 10 new jobs.

### **Conceptual Pattern: Orchestrating CrewAI with Clay Tables**

This architecture combines the above patterns to use a Clay table as the central orchestration layer for a CrewAI multi-agent system.8

**Architecture:**

1. **Task Queue (Clay Table A: Agent\_Task\_Queue):** A table is created where each row represents a single research task. Columns include:  
   * company\_domain (Unique Key)  
   * research\_goal (e.g., "Find recent product launches")  
   * status (Select: $new, pending, complete, error$)  
   * agent\_results (Text)  
2. **Provisioning:** An Auto-update column Find Company Info enriches the row with basic data as soon as it's added, preparing context for the agent.  
3. **Trigger (External Script):** A simple external Python script (or an n8n workflow) runs on a schedule. It uses a read-only API (or a simple CSV export) to find all rows where status \== 'pending'.  
4. **Task Execution (CrewAI):** For each pending row, the script triggers the CrewAI crew.kickoff() 51, passing the company\_domain and research\_goal as inputs. The CrewAI agents (e.g., ResearchAgent, WriterAgent) execute the task.  
5. **Data Persistence (The "Write" Step):** Upon completion, the CrewAI script generates a JSON of the results. This is the key step.  
   * results\_payload \= {'company\_domain': 'acme.com', 'agent\_results': '...summary...', 'status': 'complete'}  
6. **State Management (The Solution):**  
   * The Python script $POST$s this $results\_payload$ to the **webhook URL** of Clay Table A.33  
   * The table's **Auto-dedupe** feature 14, which is set to monitor company\_domain, catches this $POST$.  
   * It recognizes the company\_domain as a duplicate, and **merges** the new data into the original task row.  
   * The row's agent\_results column is filled, and its status is updated from $pending$ to $complete$.

This **Agentic Orchestration Loop** (Diagram 3\) allows Clay to act as a robust, no-code backend for managing the state, queue, and results of a complex, external AI agent system.

## **Part 7: Governance, Scaling, and Limitations**

Using Clay at scale introduces operational challenges related to technical limits, error handling, and cost management. This section provides solutions and governance frameworks.

### **Technical Limits and Scaling Solutions**

* **Row/Column Limits:** Standard Clay tables are limited to **50,000 rows**.13 Tables are also limited to **70 total columns**, with a maximum of **30 integration/enrichment columns**.53  
* **Scaling Workaround 1: "Bulk Enrichment"**  
  * This is an Enterprise-level workflow designed for massive, infrequent updates, primarily with Salesforce.55  
  * **Process:** Users can import *millions* of records from Salesforce. Clay enriches these records in a dedicated environment. The results are then securely exported *back* to Salesforce.  
  * **Key Constraint:** The enriched rows are *not* stored permanently in Clay. They are archived and deleted after 30 days.55 This is for batch processing, not for creating a permanent, massive database in Clay.  
* **Scaling Workaround 2: "Passthrough Tables"**  
  * This architecture is designed for **high-throughput, real-time streams**.54  
  * **Process:** Data is received (e.g., via webhook), immediately triggers a chain of enrichments, and is then forwarded to a final destination (e.g., a CRM or data warehouse).  
  * **Key Constraint:** The rows are **deleted** from the Clay table shortly after being processed.54 This keeps the table size small, well below the 50k limit, allowing it to function as a highly performant data-processing "pipe" rather than a database.

### **Error Handling and Monitoring**

* **Troubleshooting Stuck Columns:** Columns can sometimes get "stuck" processing, often after multiple edits.57  
  1. **Hard Refresh:** The first step is always a hard browser refresh (Cmd+Shift+R or Ctrl+Shift+R).57  
  2. **The "Duplicate and Merge" Fix:** If a refresh fails, the standard fix is 57:  
     * Duplicate the broken column.  
     * Filter the table for rows where the *original* (broken) column "is empty."  
     * Run the *new* (duplicate) column *only on those filtered rows*.  
     * Once complete, use the Merge columns feature to combine the results.  
* **Automatic Retries:** The automatic retry of failed rows is a common community request but is **not currently a feature**.12 The official manual workaround is to:  
  1. Switch to the built-in **Errored Rows** view.11  
  2. Select all rows in this view.  
  3. Manually re-run the failed enrichment column.  
* **Managing API Rate Limits:** When using the HTTP API integration to call an external API, it is crucial to respect its rate limits.58  
  * **Best Practice:** Always use the optional **Define rate limit** setting within the HTTP API column configuration.59 This allows you to specify, for example, "80 requests per 60000 milliseconds" to stay within an API's quota. For external enrichments, process in smaller batches (e.g., 50 rows at a time).57  
* **Cost Management & Governance:**  
  * **The Cardinal Sin:** The most common and expensive mistake is leaving Auto-update 2 enabled on an expensive column (e.g., AI generation, premium data) and then importing thousands of rows, leading to massive, instant credit spend.10  
  * **Best Practices:**  
    1. **Disable Auto-update by default** at the table or column level.  
    2. **Test on samples.** Before running on 1,000 rows, run on 10 and check the "Test Run" output.62  
    3. **Use Conditional Gating:** Use the Only run if conditional logic (Part 3\) to ensure expensive actions *only* run on rows that are fully qualified.21  
    4. **Use Your Own API Keys:** Clay allows users to connect their own API keys for many data providers.63 This is often significantly cheaper than using Clay credits, as Clay's credits abstract and add a margin to the provider's direct cost.64

### **Collaborative Workflows and Permissions**

* **Roles:** Clay provides three user roles:  
  * **Admin:** Full control over the workspace, including billing, settings, and user management.65  
  * **Editor:** Standard user. Can create and edit tables, run enrichments, but cannot manage billing or team members.65  
  * **Viewer (Enterprise Only):** Read-only access by default.65  
* The Key Limitation: No Table-Level Permissions  
  This is a critical governance finding. It is not currently possible to restrict access to a specific table.65 All members (Admins and Editors) invited to a workspace can view and edit all tables within that workspace.  
* Workaround: Workbook-Level Permissions  
  The only available workaround for data-segregation is to use workbooks.  
  1. Place sensitive tables inside their own dedicated workbook.  
  2. In the workbook settings, change Access permissions to Admin and invited collaborators only.65  
     This allows an Admin to add specific Viewers or Editors as collaborators to that workbook only, approximating per-project privacy.

## **Part 8: Advanced Troubleshooting and Optimization FAQ**

This section provides concise answers to the most common technical challenges and optimization questions, drawing from community-sourced best practices.

Q1: My enrichment column is stuck or frozen. How do I fix it?  
A: First, perform a hard refresh of your browser (Cmd+Shift+R for Mac, Ctrl+Shift+R for Windows).57 If it remains stuck, use the "Duplicate and Merge" fix: duplicate the column, filter for rows where the original column "is empty," run the new column on those filtered rows, and then merge the results back.57  
Q2: How do I avoid overspending on credits by accident?  
A: The primary cause of overspending is the Auto-update feature.2 1\) Disable Auto-update on all expensive columns (especially AI and premium data) by default. 2\) Test on small samples (e.g., 10 rows) before running on your full list.62 3\) Use conditional runs: Add a Checkbox column as a "gate" and use the Only run if setting to ensure you only enrich fully qualified rows.21 4\) Use your own API keys where possible, as this does not consume Clay credits.63  
Q3: How do I programmatically update an existing row from an external app (e.g., Python, CrewAI)?  
A: You cannot use a direct $PUT$ API call, as this is not supported.17 You must use the "Update via Dedupe" pattern:

1. Enable Auto-dedupe 2 on your table, set to monitor a unique key (e.g., email or task\_id).  
2. Have your external app $POST$ the *new data as a new row* to the table's webhook URL.47  
3. Auto-dedupe will intercept this $POST$, see the matching unique key, and *merge* the new data into the existing row instead of creating a duplicate.14

Q4: Clay is overwriting my HubSpot/Salesforce data. How do I stop it?  
A: This is a data governance failure. 1\) Clarify data ownership: Never map Clay to a CRM field that a human representative touches. Create new, "Clay-owned" fields in your CRM (e.g., Clay\_Enriched\_Title) and map only to those.46 2\) Disable auto-sync: Handpick your field mappings and use Only run if conditions to gate what data gets pushed. 3\) Use Lookup (Read) actions 34 to pull data before you use Update (Write) actions to prevent errors.  
Q5: How do I handle the 50,000 row limit for a massive project?  
A: For Enterprise Salesforce users, the intended solution is the "Bulk Enrichment" workflow, which enriches millions of records outside of the table and exports back to SFDC.55 For high-throughput streams (e.g., webhooks), you must design your table as a "Passthrough Table" that enriches and immediately deletes rows to stay under the limit.54 Otherwise, you must break your project into multiple 50,000-row tables.53  
Q6: How do I restrict my team from seeing a sensitive table?  
A: You cannot. Clay does not support table-level permissions.65 All workspace members can see all tables. The only workaround is to place the sensitive table in its own workbook and set that workbook's access permissions to Admin and invited collaborators only.65  
Q7: How do I make one enrichment (Column C) run only after another one (Column B) finishes?  
A: You must use the "Conditional Chaining" pattern.21

1. Create a Checkbox column between them.  
2. Set its type to Formula and use: $IF({{Column B}}\!= null, true, false)$.  
3. Go to the settings for Column C and set its Only run if condition to reference the Checkbox column $({{Checkbox\_Column\_Name}} \== true)$.  
   This explicitly tells Column C to wait until Column B has successfully populated.

#### **Works cited**

1. Table columns | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/table-columns-overview](https://www.clay.com/university/guide/table-columns-overview)  
2. Table management settings | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/table-management-settings](https://www.clay.com/university/guide/table-management-settings)  
3. Clay | Go to market with unique data—and the ability to act on it, accessed November 13, 2025, [https://www.clay.com/](https://www.clay.com/)  
4. Clay Workflow Automation: A Complete Guide to Scale Personalized Outreach, accessed November 13, 2025, [https://www.revvgrowth.com/marketing-automation/clay-workflow-automation-for-personalized-outreach](https://www.revvgrowth.com/marketing-automation/clay-workflow-automation-for-personalized-outreach)  
5. How Rootly used Clay to scale outbound sales with leaner, smarter workflows, accessed November 13, 2025, [https://www.clay.com/customers/rootly](https://www.clay.com/customers/rootly)  
6. ️ TAM Sourcing: From Workflows to Revenue Engines \- Clay, accessed November 13, 2025, [https://www.clay.com/university/lesson/tam-sourcing-workflows-in-clay-tam-sourcing](https://www.clay.com/university/lesson/tam-sourcing-workflows-in-clay-tam-sourcing)  
7. Top 10 AI Agents for Business Automation in 2025 \- Kommunicate, accessed November 13, 2025, [https://www.kommunicate.io/blog/best-ai-agents/](https://www.kommunicate.io/blog/best-ai-agents/)  
8. Creating Custom Agents for IT Partners: Advice Needed \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/s1xts2obkbnh/creating-custom-agents-for-it-partners-advice-need](https://community.clay.com/x/support/s1xts2obkbnh/creating-custom-agents-for-it-partners-advice-need)  
9. Formulas in Clay: conditional statements, waterfalling data and qualifying leads \- The GTM with Clay Blog, accessed November 13, 2025, [https://www.clay.com/blog/formulas-in-clay-intro](https://www.clay.com/blog/formulas-in-clay-intro)  
10. The Ultimate Clay Workflow for Outbound Lead Generation \- YouTube, accessed November 13, 2025, [https://www.youtube.com/watch?v=HmCcU6Sk5nQ](https://www.youtube.com/watch?v=HmCcU6Sk5nQ)  
11. Customize your table view | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/customizing-your-table-view](https://www.clay.com/university/guide/customizing-your-table-view)  
12. Automating Error Handling for AI Field Reruns in Our System \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/feedback/we61kh19zoni/automating-error-handling-for-ai-field-reruns-in-o](https://community.clay.com/x/feedback/we61kh19zoni/automating-error-handling-for-ai-field-reruns-in-o)  
13. Understanding Table Size Limit and Duplicate Lead Handling in Imports \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/znhw1p19nvpd/understanding-table-size-limit-and-duplicate-lead](https://community.clay.com/x/support/znhw1p19nvpd/understanding-table-size-limit-and-duplicate-lead)  
14. Guidance for Updating Existing Records in Clay via Webhook Integration, accessed November 13, 2025, [https://community.clay.com/x/support/5rfkmj5mi5zn/guidance-for-updating-existing-records-in-clay-via](https://community.clay.com/x/support/5rfkmj5mi5zn/guidance-for-updating-existing-records-in-clay-via)  
15. Manage cell data | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/manage-cell-data](https://www.clay.com/university/guide/manage-cell-data)  
16. Formulas | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/formula-generator](https://www.clay.com/university/guide/formula-generator)  
17. Correct API Endpoint for Updating a Clay Table Cell Value, accessed November 13, 2025, [https://community.clay.com/x/support/jfxn247eg6l6/correct-api-endpoint-for-updating-a-clay-table-cel](https://community.clay.com/x/support/jfxn247eg6l6/correct-api-endpoint-for-updating-a-clay-table-cel)  
18. documentation on Formula function \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/rq85upnqkxha/documentation-on-formula-function](https://community.clay.com/x/support/rq85upnqkxha/documentation-on-formula-function)  
19. Lesson 4: Enrich Companies Using Waterfalls \- Clay 101 \- YouTube, accessed November 13, 2025, [https://www.youtube.com/watch?v=4TVYKRZqKGw](https://www.youtube.com/watch?v=4TVYKRZqKGw)  
20. Email Finder • Find verified emails across all data providers | Clay, accessed November 13, 2025, [https://www.clay.com/tools/email-finder](https://www.clay.com/tools/email-finder)  
21. Enrichments | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/enrichments](https://www.clay.com/university/guide/enrichments)  
22. Write to Other Table | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/write-to-table-integration-overview](https://www.clay.com/university/guide/write-to-table-integration-overview)  
23. Menu of Use Cases & Workflows with Clay (by Motion) \- FullFunnel, accessed November 13, 2025, [https://www.fullfunnel.co/blog/menu-of-use-cases-workflows-with-clay-by-motion](https://www.fullfunnel.co/blog/menu-of-use-cases-workflows-with-clay-by-motion)  
24. Finding People in Clay \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/finding-people-in-clay](https://www.clay.com/university/lesson/finding-people-in-clay)  
25. Add Find People Column to Companies Table in Your Workbook ..., accessed November 13, 2025, [https://community.clay.com/x/support/fg14aaiv7qnh/add-find-people-column-to-companies-table-in-your](https://community.clay.com/x/support/fg14aaiv7qnh/add-find-people-column-to-companies-table-in-your)  
26. Enriching People Data \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/enriching-people-data](https://www.clay.com/university/lesson/enriching-people-data)  
27. How To Find Verified Emails in Clay \[Clay Enrichment\] \- YouTube, accessed November 13, 2025, [https://www.youtube.com/watch?v=4gPUNmmCTZU](https://www.youtube.com/watch?v=4gPUNmmCTZU)  
28. Understanding Clay's Enrichment Function for LinkedIn Candidate Data, accessed November 13, 2025, [https://community.clay.com/x/general/qx9d7m6e2bm4/understanding-clays-enrichment-function-for-linked](https://community.clay.com/x/general/qx9d7m6e2bm4/understanding-clays-enrichment-function-for-linked)  
29. Transforming with AI Formulas \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/transforming-with-ai-formulas](https://www.clay.com/university/lesson/transforming-with-ai-formulas)  
30. How To Enrich LinkedIn Profiles In Clay \- YouTube, accessed November 13, 2025, [https://www.youtube.com/watch?v=IOrCkGA7H48](https://www.youtube.com/watch?v=IOrCkGA7H48)  
31. How to Calculate Job Duration on LinkedIn Profiles for Enriching Emails \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/pmvtmuip83w4/how-to-calculate-job-duration-on-linkedin-profiles](https://community.clay.com/x/support/pmvtmuip83w4/how-to-calculate-job-duration-on-linkedin-profiles)  
32. End-to-End Workflow \[Inbound Automation\] \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/clay-inbound-automation-end-to-end-workflow-inbound-automation](https://www.clay.com/university/lesson/clay-inbound-automation-end-to-end-workflow-inbound-automation)  
33. Webhooks in Clay | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/webhook-integration-guide](https://www.clay.com/university/guide/webhook-integration-guide)  
34. Clay x HubSpot Actions \[CRM Enrichment\] \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/clay-x-hubspot-actions-crm-enrichment](https://www.clay.com/university/lesson/clay-x-hubspot-actions-crm-enrichment)  
35. Exporting to Google Sheets \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/exporting-to-google-sheets](https://www.clay.com/university/lesson/exporting-to-google-sheets)  
36. Help Needed: Google Sheet Integration with Clay Table, accessed November 13, 2025, [https://community.clay.com/x/support/dypjsi8otf96/help-needed-google-sheet-integration-with-clay-tab](https://community.clay.com/x/support/dypjsi8otf96/help-needed-google-sheet-integration-with-clay-tab)  
37. 5 ways to automate Clay \- Zapier, accessed November 13, 2025, [https://zapier.com/blog/automate-clay/](https://zapier.com/blog/automate-clay/)  
38. Clay HubSpot Integration | Connect Them Today, accessed November 13, 2025, [https://ecosystem.hubspot.com/no/marketplace/apps/clay](https://ecosystem.hubspot.com/no/marketplace/apps/clay)  
39. HubSpot x Clay integration | Clay.com, accessed November 13, 2025, [https://www.clay.com/integrations/data-provider/hubspot](https://www.clay.com/integrations/data-provider/hubspot)  
40. HubSpot integration | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/hubspot-integration-overview](https://www.clay.com/university/guide/hubspot-integration-overview)  
41. Importing from your CRM \[CRM Enrichment\] \- Clay University, accessed November 13, 2025, [https://www.clay.com/university/lesson/importing-from-your-crm-crm-enrichment](https://www.clay.com/university/lesson/importing-from-your-crm-crm-enrichment)  
42. Zapier x Clay integration, accessed November 13, 2025, [https://www.clay.com/integrations/data-provider/zapier](https://www.clay.com/integrations/data-provider/zapier)  
43. n8n vs. Make.com vs. Clay.com vs. Zapier: Automation Tools for GTM \- SixtySixTen, accessed November 13, 2025, [https://sixtysixten.com/n8n-vs-make-com-vs-clay-com-vs-zapier-automation-tools-for-gtm/](https://sixtysixten.com/n8n-vs-make-com-vs-clay-com-vs-zapier-automation-tools-for-gtm/)  
44. Exploring Make.com Integration Options for Enhanced Functionality \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/rxn7g7pkoaex/exploring-makecom-integration-options-for-enhanced](https://community.clay.com/x/support/rxn7g7pkoaex/exploring-makecom-integration-options-for-enhanced)  
45. Tutorial: How to use Clay \+ Zapier: Workflow Automation (Beginner Friendly) \- YouTube, accessed November 13, 2025, [https://www.youtube.com/watch?v=QTfmeWTeyPM](https://www.youtube.com/watch?v=QTfmeWTeyPM)  
46. Integrating Clay with HubSpot \- Best Practices and Tips Needed ..., accessed November 13, 2025, [https://community.latenode.com/t/integrating-clay-with-hubspot-best-practices-and-tips-needed/24015](https://community.latenode.com/t/integrating-clay-with-hubspot-best-practices-and-tips-needed/24015)  
47. Using Clay as an API | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/using-clay-as-an-api](https://www.clay.com/university/guide/using-clay-as-an-api)  
48. Using Make.com for Data Push into Clay: Scheduling & Triggers Explained, accessed November 13, 2025, [https://community.clay.com/x/support/cdk4d0a2tyv4/using-makecom-for-data-push-into-clay-scheduling-](https://community.clay.com/x/support/cdk4d0a2tyv4/using-makecom-for-data-push-into-clay-scheduling-)  
49. Using Clay's API for Data Enrichment from Integration Platforms, accessed November 13, 2025, [https://community.clay.com/x/support/h42il37zb60v/using-clays-api-for-data-enrichment-from-integrati](https://community.clay.com/x/support/h42il37zb60v/using-clays-api-for-data-enrichment-from-integrati)  
50. Is there a step by step tutorial on how to write to another table? \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/v9lmaqrfzn0i/is-there-a-step-by-step-tutorial-on-how-to-write-t](https://community.clay.com/x/support/v9lmaqrfzn0i/is-there-a-step-by-step-tutorial-on-how-to-write-t)  
51. Tools \- CrewAI Documentation, accessed November 13, 2025, [https://docs.crewai.com/en/concepts/tools](https://docs.crewai.com/en/concepts/tools)  
52. CrewAI Documentation \- CrewAI, accessed November 13, 2025, [https://docs.crewai.com/](https://docs.crewai.com/)  
53. Limits on Rows and Tables in Database Accounts ... \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/wvww2yudnj77/limits-on-rows-and-tables-in-database-accounts](https://community.clay.com/x/support/wvww2yudnj77/limits-on-rows-and-tables-in-database-accounts)  
54. How to Generate Datasets Larger Than 50000 ... \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/dmlzrpo3pcnb/how-to-generate-datasets-larger-than-50000-rows-fo](https://community.clay.com/x/support/dmlzrpo3pcnb/how-to-generate-datasets-larger-than-50000-rows-fo)  
55. Enrich millions of records from your CRM in Clay \- The GTM with Clay Blog, accessed November 13, 2025, [https://www.clay.com/blog/bulk-enrichment](https://www.clay.com/blog/bulk-enrichment)  
56. Bulk Enrichment Table Row Limit: 10000 Explained \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/8qtwy91oss5q/bulk-enrichment-table-row-limit-10000-explained](https://community.clay.com/x/support/8qtwy91oss5q/bulk-enrichment-table-row-limit-10000-explained)  
57. Troubleshooting Automation Errors in Large Datasets | Clay, accessed November 13, 2025, [https://community.clay.com/x/support/92cbchw9rssj/troubleshooting-automation-errors-in-large-dataset](https://community.clay.com/x/support/92cbchw9rssj/troubleshooting-automation-errors-in-large-dataset)  
58. Optimizing API Requests with Rate Limits: Solutions for Re-running Columns | Clay, accessed November 13, 2025, [https://community.clay.com/x/support/rmt6i2l9roi3/optimizing-api-requests-with-rate-limits-solutions](https://community.clay.com/x/support/rmt6i2l9roi3/optimizing-api-requests-with-rate-limits-solutions)  
59. HTTP API integration overview | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/http-api-integration-overview](https://www.clay.com/university/guide/http-api-integration-overview)  
60. Setting Custom Rate Limits for HTTP API Requests to 80 per Minute \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/pykz67d3cpxs/setting-custom-rate-limits-for-http-api-requests-t](https://community.clay.com/x/support/pykz67d3cpxs/setting-custom-rate-limits-for-http-api-requests-t)  
61. I run a Clay Marketing Agency. Here's how to use Clay in 2025\. AMA ..., accessed November 13, 2025, [https://www.reddit.com/r/Entrepreneur/comments/1m0agtx/i\_run\_a\_clay\_marketing\_agency\_heres\_how\_to\_use/](https://www.reddit.com/r/Entrepreneur/comments/1m0agtx/i_run_a_clay_marketing_agency_heres_how_to_use/)  
62. How to Use Clay: The Ultimate No-Code Tool for Prospecting and Sales | SalesCaptain, accessed November 13, 2025, [https://www.salescaptain.io/blog/how-to-use-clay](https://www.salescaptain.io/blog/how-to-use-clay)  
63. FAQ | Clay.com, accessed November 13, 2025, [https://www.clay.com/faq](https://www.clay.com/faq)  
64. How does clay.com works? What are the alternatives? : r/Emailmarketing \- Reddit, accessed November 13, 2025, [https://www.reddit.com/r/Emailmarketing/comments/1b8cuy6/how\_does\_claycom\_works\_what\_are\_the\_alternatives/](https://www.reddit.com/r/Emailmarketing/comments/1b8cuy6/how_does_claycom_works_what_are_the_alternatives/)  
65. Roles and permissions | Documentation | Clay University, accessed November 13, 2025, [https://www.clay.com/university/guide/roles-and-permissions](https://www.clay.com/university/guide/roles-and-permissions)  
66. Managing Table-Level Permissions for Collaboration in Workbooks \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/clay-feedback/cmjdn3gyee5s/managing-table-level-permissions-for-collaboration](https://community.clay.com/x/clay-feedback/cmjdn3gyee5s/managing-table-level-permissions-for-collaboration)  
67. Enabling Table-Specific Access Permissions for Users \- Clay Community, accessed November 13, 2025, [https://community.clay.com/x/support/zob7s5a36zk0/enabling-table-specific-access-permissions-for-use](https://community.clay.com/x/support/zob7s5a36zk0/enabling-table-specific-access-permissions-for-use)  
68. What is B2B Leads? \- Clay, accessed November 13, 2025, [https://www.clay.com/glossary/b2b-leads](https://www.clay.com/glossary/b2b-leads)