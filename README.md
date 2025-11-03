# 🏗️ Streamlit App Generator

## Overview

A meta-application that generates custom Streamlit data capture applications with full CRUD operations, based on proven Clinical Research template patterns.

**Perfect for teams that need custom data collection solutions!**

## What It Generates

For each project, the generator creates:

### 📁 Complete SQL Setup (One File)
- **Database & schemas** (uses existing or creates new with IF NOT EXISTS)
- **Custom tables** with your defined columns and data types
- **Roles** (ADMIN, USER, READONLY) with proper grants
- **Audit framework** (if enabled)
- **Security setup** (uses existing warehouse)

### 🎨 Full-Featured Streamlit Application
- ✅ Uses `session = get_active_session()` (Streamlit in Snowflake compatible!)
- ✅ Python 3.11 compatible
- ✅ No external packages
- ✅ **Create** - Forms for each table with proper data type widgets
- ✅ **Read** - View all records in searchable tables
- ✅ **Update** - Edit any record with pre-filled forms
- ✅ Handles all SQL data types correctly (VARCHAR, INTEGER, DATE, TIMESTAMP, etc.)
- ✅ TIMESTAMP fields have both date AND time inputs
- ✅ Proper quote handling (no SQL injection, no extra quotes!)
- ✅ Navigation between tables
- ✅ Audit trail (created_by, modified_by timestamps)

### 📖 Documentation
- README.md with project overview
- DEPLOYMENT_GUIDE.md with step-by-step instructions
- Python 3.11 deployment warnings

### 📊 Governance Tracking
- **Automatic project history** saved to GENERATOR_GOVERNANCE.PROJECT_HISTORY
- Track who generated what, when
- Download SQL and apps from history
- Complete audit trail for compliance

## How to Use

### Deploy the Generator

1. **In Snowsight:**
   - Create Streamlit App
   - **Python Version: 3.11** ⚠️
   - Paste `app_generator.py`
   - Run

### Generate Your Custom App

#### **Step 1: Project Setup**
- Enter project name and description
- **Choose:** Use existing database OR create new
- **Select:** Existing warehouse from dropdown
- Set team and contact information

#### **Step 2: Define Tables**
- Add tables (e.g., ADVERSE_EVENTS, PATIENT_FEEDBACK)
- Set number of columns (updates dynamically!)
- Define each column:
  - Name (e.g., event_date, severity_level)
  - Type (VARCHAR, INTEGER, FLOAT, BOOLEAN, DATE, TIMESTAMP_NTZ, TEXT)
  - Length (for VARCHAR)
  - Required checkbox
- Add multiple tables as needed

#### **Step 3: Security & Audit**
- Enable RBAC (role-based access control)
- Enable Audit Logging
- Configure Change Tracking
- Set up User Activity Monitoring

#### **Step 4: Generate Code**
- Review configuration summary
- Click "Generate Complete Application"
- Code generated instantly!

#### **Step 5: Download & Deploy**
- **Option 1:** Copy & Paste (Recommended!)
  - Copy complete SQL → Run in worksheet
  - Copy Streamlit code → Paste in Snowsight
  - Done!
- **Option 2:** Download Files
  - Download SQL script
  - Download Streamlit app
  - Download documentation
  - Deploy manually

### Browse Project History

- Click "📚 Browse All Projects" in sidebar
- See all generated projects
- View metrics (total projects, tables, users)
- Select any project to:
  - View configuration
  - Download SQL
  - Download app
  - See who created it and when

## Key Features

### ✅ Works with Existing Infrastructure
- Select existing databases (preserves data!)
- Select existing warehouses (no new creation)
- IF NOT EXISTS clauses everywhere (safe to re-run)

### ✅ All Data Types Handled Correctly
- **VARCHAR/TEXT:** Clean text (no extra quotes!)
- **INTEGER/FLOAT:** Numbers without quotes
- **BOOLEAN:** TRUE/FALSE
- **DATE:** Date picker → proper format
- **TIMESTAMP:** Date + Time pickers → combined

### ✅ Full CRUD Operations
- **Create:** Forms for data entry
- **Read:** View all records in tables
- **Update:** Edit any record
- **Audit:** Track who created/modified

### ✅ Enterprise-Grade
- Project governance and tracking
- Complete audit trail
- Compliance ready
- Production-safe code

### ✅ Based on Proven Patterns
- Clinical Research app that works perfectly
- No SnowflakeConnection class complexity
- Direct session usage
- Clean, simple code
- All lessons learned applied!

## Generated App Example

**For a table with columns:**
- medicine_type (VARCHAR)
- quantity (INTEGER)
- dispense_date (DATE)
- notes (TEXT)

**Generated Streamlit app will have:**

**Create Tab:**
- Medicine Type: [text input]
- Quantity: [number input]
- Dispense Date: [date picker]
- Notes: [text input]
- [Submit] button

**View/Edit Tab:**
- Table showing all records
- Select record from dropdown
- Edit form pre-filled with current values
- [Update Record] button
- Audit info (created by, modified by)

**Result:**
- Saves to Snowflake correctly
- No extra quotes on text!
- Numbers as numbers
- Dates in proper format

## Deployment

### The Generator Itself
```
Database: Any (will create GENERATOR_GOVERNANCE schema)
Python: 3.11 ⚠️
Packages: None (built-in only)
```

### Generated Apps
```
Database: Custom (you define or select existing)
Warehouse: Existing (you select)
Python: 3.11 ⚠️
Packages: None (built-in only)
Pattern: Matches Clinical Research app
```

## Use Cases

Perfect for:
- ✅ Clinical teams: Incident reporting, adverse events
- ✅ Safety teams: Near-miss tracking, safety observations
- ✅ Quality teams: Audit findings, improvement tracking
- ✅ Research teams: Data collection, observations
- ✅ Operations teams: Operational logs, maintenance records
- ✅ **Any team needing structured data capture!**

## Benefits

**For IT/Data Teams:**
- ✅ Generate apps in 5 minutes
- ✅ Consistent architecture
- ✅ No coding required
- ✅ Full governance tracking
- ✅ Reusable for all teams

**For Business Teams:**
- ✅ Get exactly what they need
- ✅ Custom tables and fields
- ✅ Professional interface
- ✅ View and edit capabilities
- ✅ Snowflake reliability

## Lessons Learned & Applied

✅ Python 3.11 (not 3.10!)  
✅ No external packages  
✅ session = get_active_session()  
✅ Simple, clean code  
✅ Proper quote handling  
✅ No nested f-string complexity  
✅ IF NOT EXISTS for safety  
✅ Works with existing infrastructure  

**Every generated app works in Streamlit in Snowflake!** ✨

## Version

Generator Version: 2.0  
Last Updated: {datetime.now().strftime('%Y-%m-%d')}  
Status: Production-Ready 🚀
