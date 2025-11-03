# 🏗️ Streamlit App Generator

## Overview

A meta-application that generates custom Streamlit data capture applications based on the Clinical Research template pattern.

**Perfect for teams that need variations of the same data capture solution!**

## What It Generates

For each project, the generator creates:

### 📁 SQL Scripts
1. **01_setup_database.sql** - Database, schemas, roles, warehouse (incremental naming)
2. **02_create_tables.sql** - Custom tables with your defined columns and data types
3. **03_reference_data.sql** - Lookup tables for dropdowns (if configured)
4. **04_security_setup.sql** - RBAC permissions (if enabled)
5. **05_audit_framework.sql** - Audit logging tables (if enabled)

### 🎨 Streamlit Application
- Complete data capture app following Clinical Research pattern
- ✅ Uses `session = get_active_session()` (Streamlit in Snowflake compatible!)
- ✅ Python 3.11 compatible
- ✅ No external packages
- ✅ Forms for each table
- ✅ Navigation between forms
- ✅ Proper error handling

### 📖 Documentation
- README.md with project overview
- DEPLOYMENT_GUIDE.md with step-by-step instructions
- Python 3.11 deployment warnings

## How to Use

### Deploy the Generator

1. **In Snowsight:**
   - Create Streamlit App
   - **Python Version: 3.11** ⚠️
   - Paste `app_generator.py`
   - Run

### Generate Your Custom App

1. **Step 1: Project Setup**
   - Enter project name, database prefix
   - Configure warehouse size

2. **Step 2: Define Tables**
   - Add tables (e.g., ADVERSE_EVENTS, PATIENT_FEEDBACK)
   - Define columns with data types
   - Mark required fields

3. **Step 3: Reference Data**
   - Add lookup tables (e.g., STATUS, PRIORITY)
   - Define values for dropdowns

4. **Step 4: Security & Audit**
   - Enable RBAC
   - Configure audit logging
   - Set up change tracking

5. **Step 5: Generate Code**
   - Click "Generate" button
   - All SQL scripts and Streamlit app created

6. **Step 6: Download & Deploy**
   - Download all generated files
   - Execute SQL scripts
   - Deploy Streamlit app
   - Start capturing data!

## Key Features

### ✅ Incremental Naming Convention
- Database: `{PREFIX}_DB`
- Warehouse: `{PREFIX}_WH`
- Roles: `{PREFIX}_ADMIN`, `{PREFIX}_USER`, `{PREFIX}_READONLY`

### ✅ Follows Proven Pattern
- Based on Clinical Research app that works perfectly
- No SnowflakeConnection class complexity
- Direct session usage
- Clean, simple code

### ✅ Team-Specific Customization
- Each team defines their own tables
- Custom columns and data types
- Team-specific reference data
- Project-specific audit needs

### ✅ Security Consistent Across Projects
- Standard RBAC pattern
- Reusable security model
- Audit framework template
- Best practices built-in

## Use Cases

- ✅ Clinical teams needing incident reporting
- ✅ Safety teams capturing near-misses
- ✅ Quality teams tracking improvements
- ✅ Research teams collecting observations
- ✅ Any team needing structured data capture!

## Deployment

### The Generator Itself
```
Database: Can run from any database
Python: 3.11
Packages: None (built-in only)
```

### Generated Apps
```
Database: Custom (you define)
Python: 3.11
Packages: None (built-in only)
Pattern: Matches Clinical Research app
```

## Benefits

**For IT/Data Teams:**
- ✅ Generate apps in minutes, not hours
- ✅ Consistent architecture across projects
- ✅ No copy-paste errors
- ✅ Standardized security

**For Business Teams:**
- ✅ Get custom solutions quickly
- ✅ Exactly the tables/fields they need
- ✅ Professional interface
- ✅ Snowflake-powered reliability

## Learned Lessons Applied

✅ Python 3.11 (not 3.10!)  
✅ No external packages  
✅ session = get_active_session()  
✅ No SnowflakeConnection class  
✅ Simple, clean code  
✅ Proper quote escaping  
✅ PARSE_JSON with SELECT not VALUES  

**No blonde moments in generated code!** 😄✨

Generated: {datetime.now().strftime('%Y-%m-%d')}

