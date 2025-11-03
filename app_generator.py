"""
Streamlit App Generator
=======================
A meta-application that generates custom Streamlit data capture applications
based on user-defined requirements.

⚠️ DEPLOYMENT REQUIREMENT:
   - Runs in Streamlit in Snowflake
   - Python 3.11 runtime (NOT 3.10!)
   - No external packages needed

This tool creates:
1. SQL scripts for database setup (with incremental naming)
2. Table definitions with custom columns and data types
3. Reference data tables
4. Audit framework
5. Security setup
6. Complete Streamlit application (Streamlit in Snowflake compatible!)
7. Documentation and deployment guides

Author: Data Solutions Team
Date: 2025-11-03
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import snowflake.snowpark.context as snowpark_context

# Initialize Snowflake session for Streamlit in Snowflake
session = snowpark_context.get_active_session()

# Page configuration
st.set_page_config(
    page_title="Streamlit App Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .step-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .config-card {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏗️ Streamlit App Generator</h1>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>
    Generate custom Streamlit data capture applications with SQL backend - based on Clinical Research template
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'project_config' not in st.session_state:
    st.session_state.project_config = {
        'project_name': '',
        'database_name': '',
        'tables': [],
        'audit_enabled': True,
        'security_features': []
    }

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("## 🧭 Generator Steps")
        
        steps = [
            "1️⃣ Project Setup",
            "2️⃣ Define Tables",
            "3️⃣ Security & Audit",
            "4️⃣ Generate Code",
            "5️⃣ Download & Deploy"
        ]
        
        selected_step = st.radio("Select Step", steps, index=st.session_state.current_step - 1)
        st.session_state.current_step = steps.index(selected_step) + 1
        
        st.markdown("---")
        
        # Show current configuration summary
        with st.expander("📋 Current Configuration"):
            if st.session_state.project_config['project_name']:
                st.write(f"**Project:** {st.session_state.project_config['project_name']}")
                st.write(f"**Database:** {st.session_state.project_config['database_name']}")
                st.write(f"**Tables:** {len(st.session_state.project_config['tables'])}")
            else:
                st.info("No configuration yet")
        
        st.markdown("---")
        
        # Project History
        with st.expander("📚 Project History"):
            try:
                history_query = """
                SELECT 
                    project_name,
                    database_name,
                    generated_timestamp,
                    generated_by,
                    table_count,
                    status
                FROM GENERATOR_GOVERNANCE.PROJECT_HISTORY
                ORDER BY generated_timestamp DESC
                LIMIT 20
                """
                history_df = session.sql(history_query).to_pandas()
                
                if not history_df.empty:
                    st.dataframe(history_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No projects generated yet")
            except:
                st.info("Generate your first project to see history")
        
        st.markdown("---")
        st.markdown("### 🔄 Actions")
        
        if st.button("🗑️ Clear All"):
            st.session_state.project_config = {
                'project_name': '',
                'database_name': '',
                'tables': [],
                'audit_enabled': True,
                'security_features': []
            }
            st.session_state.current_step = 1
            st.rerun()
        
        if st.button("💾 Save Config"):
            config_json = json.dumps(st.session_state.project_config, indent=2)
            st.download_button(
                "Download Configuration",
                config_json,
                file_name=f"{st.session_state.project_config['database_name']}_config.json",
                mime="application/json"
            )
        
        if st.button("📚 Browse All Projects"):
            st.session_state.show_history = True
            st.rerun()

def main():
    """Main application function"""
    render_sidebar()
    
    # Check if user wants to browse history
    if st.session_state.get('show_history', False):
        render_project_history()
    else:
        # Render current step
        if st.session_state.current_step == 1:
            render_step1_project_setup()
        elif st.session_state.current_step == 2:
            render_step2_define_tables()
        elif st.session_state.current_step == 3:
            render_step3_security_audit()
        elif st.session_state.current_step == 4:
            render_step4_generate_code()
        elif st.session_state.current_step == 5:
            render_step5_download_deploy()

def render_project_history():
    """View all generated projects for governance"""
    st.markdown('<div class="step-header"><h2>📚 Project History & Governance</h2></div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Generator"):
        st.session_state.show_history = False
        st.rerun()
    
    st.markdown("### Generated Projects Audit Trail")
    st.info("Track all projects generated through this tool for governance and compliance")
    
    try:
        # Query all projects
        query = """
        SELECT 
            project_id,
            project_name,
            database_name,
            generated_timestamp,
            generated_by,
            table_count,
            total_columns,
            status
        FROM GENERATOR_GOVERNANCE.PROJECT_HISTORY
        ORDER BY generated_timestamp DESC
        """
        
        df = session.sql(query).to_pandas()
        
        if not df.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Projects", len(df))
            with col2:
                st.metric("Total Tables", df['TABLE_COUNT'].sum())
            with col3:
                st.metric("Total Columns", df['TOTAL_COLUMNS'].sum())
            with col4:
                unique_users = df['GENERATED_BY'].nunique()
                st.metric("Users", unique_users)
            
            st.markdown("---")
            
            # Display all projects
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Select project to view details
            st.markdown("---")
            st.markdown("### 🔍 View Project Details")
            
            project_ids = df['PROJECT_ID'].tolist()
            selected = st.selectbox(
                "Select Project",
                [""] + project_ids,
                format_func=lambda x: "Choose a project..." if x == "" else df[df['PROJECT_ID']==x]['PROJECT_NAME'].values[0] if x else ""
            )
            
            if selected:
                # Get full project details
                detail_query = f"""
                SELECT *
                FROM GENERATOR_GOVERNANCE.PROJECT_HISTORY
                WHERE project_id = '{selected}'
                """
                
                detail_df = session.sql(detail_query).to_pandas()
                
                if not detail_df.empty:
                    project = detail_df.iloc[0]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Project Info")
                        st.write(f"**Name:** {project['PROJECT_NAME']}")
                        st.write(f"**Database:** {project['DATABASE_NAME']}")
                        st.write(f"**Generated:** {project['GENERATED_TIMESTAMP']}")
                        st.write(f"**By:** {project['GENERATED_BY']}")
                        st.write(f"**Tables:** {project['TABLE_COUNT']}")
                        st.write(f"**Columns:** {project['TOTAL_COLUMNS']}")
                    
                    with col2:
                        st.markdown("#### Actions")
                        
                        # Download buttons for this project
                        if st.button("📥 Download SQL"):
                            st.download_button(
                                "Download SQL Script",
                                project['SQL_SCRIPT'],
                                file_name=f"{project['DATABASE_NAME']}_setup.sql",
                                mime="text/sql",
                                key="dl_hist_sql"
                            )
                        
                        if st.button("📥 Download App"):
                            st.download_button(
                                "Download Streamlit App",
                                project['STREAMLIT_APP_CODE'],
                                file_name=f"{project['DATABASE_NAME'].lower()}_app.py",
                                mime="text/python",
                                key="dl_hist_app"
                            )
                    
                    # Show configuration
                    with st.expander("⚙️ View Configuration"):
                        st.json(project['CONFIGURATION'])
        else:
            st.info("No projects in history yet. Generate your first project!")
    
    except Exception as e:
        st.error(f"Error loading project history: {str(e)}")
        st.info("The governance table will be created automatically when you generate your first project")


def render_step1_project_setup():
    """Step 1: Project and database setup"""
    st.markdown('<div class="step-header"><h2>1️⃣ Project Setup</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Basic Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "Project Name *",
            value=st.session_state.project_config.get('project_name', ''),
            placeholder="e.g., Patient Safety Reporting",
            help="Descriptive name for your project"
        )
        
        # Database selection - existing or new
        use_existing_db = st.checkbox("Use Existing Database", value=False)
        
        if use_existing_db:
            # Get list of existing databases
            try:
                dbs_query = "SHOW DATABASES"
                dbs_result = session.sql(dbs_query).collect()
                db_names = [row['name'] for row in dbs_result if not row['name'].startswith('SNOWFLAKE')]
                
                selected_db = st.selectbox(
                    "Select Existing Database *",
                    db_names,
                    help="Choose from your existing databases"
                )
                database_prefix = selected_db.replace('_DB', '').replace('_', '_')
                database_name = selected_db
                
                st.info(f"Using existing database: `{selected_db}`")
            except Exception as e:
                st.error(f"Error loading databases: {str(e)}")
                database_prefix = ""
                database_name = ""
        else:
            # Create new database
            database_prefix = st.text_input(
                "Database Name Prefix *",
                value=st.session_state.project_config.get('database_prefix', ''),
                placeholder="e.g., PATIENT_SAFETY",
                help="All caps, underscores only - will create {PREFIX}_DB"
            )
            database_name = f"{database_prefix}_DB" if database_prefix else ""
        
        project_description = st.text_area(
            "Project Description",
            value=st.session_state.project_config.get('description', ''),
            placeholder="Brief description of what this application will do..."
        )
    
    with col2:
        team_name = st.text_input(
            "Team/Department Name",
            value=st.session_state.project_config.get('team_name', ''),
            placeholder="e.g., Clinical Quality Team"
        )
        
        primary_contact = st.text_input(
            "Primary Contact",
            value=st.session_state.project_config.get('primary_contact', ''),
            placeholder="e.g., jane.smith@health.gov"
        )
        
        # Warehouse selection from existing
        try:
            wh_query = "SHOW WAREHOUSES"
            wh_result = session.sql(wh_query).collect()
            wh_names = [row['name'] for row in wh_result]
            
            selected_warehouse = st.selectbox(
                "Select Warehouse *",
                wh_names,
                help="Choose an existing warehouse for compute"
            )
        except Exception as e:
            st.error(f"Error loading warehouses: {str(e)}")
            selected_warehouse = "COMPUTE_WH"
    
    # Database naming convention
    st.markdown("---")
    st.markdown("### 📝 Database Naming Convention")
    
    if database_prefix:
        database_name = f"{database_prefix}_DB"
        schema_raw = f"RAW_DATA"
        schema_apps = f"APPS"
        
        st.info(f"""
        **Configuration:**
        - Database: `{database_name}`
        - Raw Data Schema: `{database_name}.{schema_raw}`
        - Apps Schema: `{database_name}.{schema_apps}`
        - Warehouse: `{selected_warehouse}`
        """)
    
    # Save configuration
    if st.button("💾 Save & Continue →", type="primary"):
        if project_name and (database_name or database_prefix):
            st.session_state.project_config.update({
                'project_name': project_name,
                'database_prefix': database_prefix if database_prefix else database_name.replace('_DB', ''),
                'database_name': database_name if database_name else f"{database_prefix}_DB",
                'use_existing_db': use_existing_db,
                'description': project_description,
                'team_name': team_name,
                'primary_contact': primary_contact,
                'warehouse_name': selected_warehouse,
                'schema_raw': 'RAW_DATA',
                'schema_apps': 'APPS'
            })
            st.success("✅ Project configuration saved!")
            st.session_state.current_step = 2
            st.rerun()
        else:
            st.error("Please fill in required fields (Project Name and Database)")


def render_step2_define_tables():
    """Step 2: Define data tables"""
    st.markdown('<div class="step-header"><h2>2️⃣ Define Data Tables</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Add Tables to Your Application")
    st.info("Define the tables where your team will capture data. Each table will have a dedicated form in the Streamlit app.")
    
    # Show existing tables
    if st.session_state.project_config['tables']:
        st.markdown("#### Current Tables")
        for idx, table in enumerate(st.session_state.project_config['tables']):
            with st.expander(f"📊 {table['table_name']} ({len(table['columns'])} columns)"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Description:** {table['description']}")
                    st.write(f"**Columns:** {', '.join([c['name'] for c in table['columns']])}")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_{idx}"):
                        st.session_state.project_config['tables'].pop(idx)
                        st.rerun()
    
    # Add new table
    st.markdown("---")
    st.markdown("#### ➕ Add New Table")
    
    # Number of columns selector (outside form so it updates immediately)
    if 'num_columns' not in st.session_state:
        st.session_state.num_columns = 5
    
    num_columns = st.number_input("Number of Columns", min_value=1, max_value=50, value=st.session_state.num_columns, key="num_cols_input")
    st.session_state.num_columns = num_columns
    
    with st.form("add_table"):
        table_name = st.text_input(
            "Table Name *",
            placeholder="e.g., ADVERSE_EVENTS",
            help="All caps, underscores only"
        )
        
        table_description = st.text_input(
            "Table Description",
            placeholder="e.g., Record adverse events and incidents"
        )
        
        st.markdown(f"**Define {num_columns} Columns:**")
        
        columns = []
        for i in range(num_columns):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                col_name = st.text_input(f"Column {i+1} Name", key=f"col_name_{i}", placeholder="e.g., event_date")
            with col2:
                col_type = st.selectbox(f"Type", ["VARCHAR", "INTEGER", "FLOAT", "BOOLEAN", "DATE", "TIMESTAMP_NTZ", "TEXT", "VARIANT"], key=f"col_type_{i}")
            with col3:
                col_length = st.text_input(f"Length", key=f"col_len_{i}", value="255" if col_type == "VARCHAR" else "")
            with col4:
                col_required = st.checkbox("Required", key=f"col_req_{i}")
            
            if col_name:
                col_def = {
                    'name': col_name,
                    'type': col_type if col_type != "VARCHAR" or not col_length else f"{col_type}({col_length})",
                    'required': col_required
                }
                columns.append(col_def)
        
        submitted = st.form_submit_button("Add Table")
        
        if submitted and table_name and columns:
            table_config = {
                'table_name': table_name,
                'description': table_description,
                'columns': columns
            }
            st.session_state.project_config['tables'].append(table_config)
            # Reset column count for next table
            st.session_state.num_columns = 5
            st.success(f"✅ Table {table_name} added!")
            st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.current_step = 1
            st.rerun()
    with col2:
        if st.button("Continue →", type="primary"):
            if st.session_state.project_config['tables']:
                st.session_state.current_step = 3
                st.rerun()
            else:
                st.warning("Please add at least one table")


def render_step3_security_audit():
    """Step 3: Security and audit configuration"""
    st.markdown('<div class="step-header"><h2>3️⃣ Security & Audit Configuration</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Security Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Access Control")
        role_based = st.checkbox("Role-Based Access Control (RBAC)", value=True)
        row_level = st.checkbox("Row-Level Security", value=False)
        data_masking = st.checkbox("Dynamic Data Masking", value=False)
    
    with col2:
        st.markdown("#### Audit Features")
        audit_enabled = st.checkbox("Audit Logging", value=True)
        change_tracking = st.checkbox("Change Data Capture", value=True)
        user_tracking = st.checkbox("User Activity Tracking", value=True)
    
    st.session_state.project_config.update({
        'audit_enabled': audit_enabled,
        'security_features': {
            'rbac': role_based,
            'row_level_security': row_level,
            'data_masking': data_masking,
            'change_tracking': change_tracking,
            'user_tracking': user_tracking
        }
    })
    
    # Show what will be created
    st.markdown("---")
    st.markdown("### 📋 What Will Be Generated")
    
    security_items = []
    if role_based:
        security_items.append("✅ User roles (ADMIN, USER, READONLY)")
    if row_level:
        security_items.append("✅ Row access policies")
    if data_masking:
        security_items.append("✅ Masking policies for sensitive data")
    if audit_enabled:
        security_items.append("✅ Audit logging tables and triggers")
    if change_tracking:
        security_items.append("✅ Change history tracking")
    if user_tracking:
        security_items.append("✅ User activity monitoring")
    
    for item in security_items:
        st.markdown(item)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_step3"):
            st.session_state.current_step = 2
            st.rerun()
    with col2:
        if st.button("Generate Code →", key="next_step3", type="primary"):
            st.session_state.current_step = 4
            st.rerun()


def render_step4_generate_code():
    """Step 4: Generate all code"""
    st.markdown('<div class="step-header"><h2>4️⃣ Generate Code</h2></div>', unsafe_allow_html=True)
    
    config = st.session_state.project_config
    
    if not config['project_name'] or not config['tables']:
        st.error("Please complete Steps 1 and 2 first")
        return
    
    st.success("✅ Configuration complete - ready to generate!")
    
    # Show summary
    st.markdown("### 📊 Generation Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Data Tables", len(config['tables']))
    with col2:
        total_columns = sum(len(t['columns']) for t in config['tables'])
        st.metric("Total Columns", total_columns)
    
    # Generate button
    if st.button("🏗️ Generate Complete Application", type="primary"):
        with st.spinner("Generating your custom Streamlit application..."):
            # Store generated code in session state
            generate_all_code()
            st.success("✅ Code generation complete!")
            st.session_state.current_step = 5
            st.rerun()


def render_step5_download_deploy():
    """Step 5: Download and deployment"""
    st.markdown('<div class="step-header"><h2>5️⃣ Download & Deploy</h2></div>', unsafe_allow_html=True)
    
    # Check if code has been generated
    if 'generated_code' not in st.session_state:
        st.warning("⚠️ Code not generated yet")
        st.info("Click the button below to generate your custom application first:")
        
        if st.button("🏗️ Generate Application Now", type="primary"):
            with st.spinner("Generating your custom Streamlit application..."):
                generate_all_code()
                st.success("✅ Code generation complete!")
                st.rerun()
        return
    
    st.success("✅ Your custom application is ready!")
    
    code = st.session_state.generated_code
    config = st.session_state.project_config
    
    # Deployment options
    deployment_option = st.radio(
        "Choose Deployment Method",
        ["📋 Copy & Paste (Recommended)", "📥 Download Files"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if "Download" in deployment_option:
        # Download buttons for each generated file
        st.markdown("### 📥 Download Generated Files")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### SQL Script")
            if code.get('sql_scripts'):
                script_name = list(code['sql_scripts'].keys())[0]
                script_content = code['sql_scripts'][script_name]
                st.download_button(
                    f"📄 {script_name}",
                    script_content,
                    file_name=f"{config['database_prefix']}_complete_setup.sql",
                    mime="text/sql"
                )
                st.info(f"One complete SQL file with all setup scripts")
        
        with col2:
            st.markdown("#### Streamlit App")
            if 'streamlit_app' in code:
                st.download_button(
                    "🎨 streamlit_app.py",
                    code['streamlit_app'],
                    file_name=f"{config['database_prefix'].lower()}_app.py",
                    mime="text/python"
                )
        
        with col3:
            st.markdown("#### Documentation")
            if 'readme' in code:
                st.download_button(
                    "📖 README.md",
                    code['readme'],
                    file_name="README.md",
                    mime="text/markdown"
                )
            if 'deployment_guide' in code:
                st.download_button(
                    "📋 Deployment Guide",
                    code['deployment_guide'],
                    file_name="DEPLOYMENT_GUIDE.md",
                    mime="text/markdown"
                )
        
        # Manual deployment instructions
        st.markdown("---")
        st.markdown("### 🚀 Manual Deployment Steps")
        
        st.markdown(f"""
        1. **Download** the complete SQL script above
        2. **Execute SQL** in Snowflake worksheet as ACCOUNTADMIN
        3. **Download** the Streamlit app
        4. **Create Streamlit app** in Snowsight:
           - Database: `{config['database_name']}`
           - Schema: `{config['schema_apps']}`
           - Python Version: **3.11** ⚠️
           - Paste the app code
        5. **Launch** and start capturing data!
        """)
    
    else:  # Copy & Paste deployment (recommended)
        st.markdown("### 📋 Copy & Paste Deployment")
        st.info("Copy the SQL script below and execute it in a Snowflake worksheet as ACCOUNTADMIN")
        
        # Show the complete SQL script for easy copy/paste
        st.markdown("#### 🔨 Complete Setup SQL")
        
        sql_script = list(code.get('sql_scripts', {}).values())[0] if code.get('sql_scripts') else ""
        
        st.code(sql_script, language='sql')
        
        st.success("👆 Copy the entire SQL script above and run it in a Snowflake worksheet!")
        
        st.markdown("---")
        st.markdown("#### 🎨 Streamlit App Code")
        
        st.info("After SQL execution, create the Streamlit app:")
        
        st.code(code.get('streamlit_app', ''), language='python')
        
        st.markdown(f"""
        **To Deploy the App:**
        1. ✅ Copy SQL above → Run in worksheet
        2. ✅ Copy Streamlit code above
        3. ✅ Go to Snowsight > Streamlit Apps
        4. ✅ Create new app:
           - Database: `{config['database_name']}`
           - Schema: `{config['schema_apps']}`
           - Python: **3.11**
        5. ✅ Paste code and Run!
        """)
        
        # Quick actions
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Generate New App"):
                # Clear and start over
                for key in list(st.session_state.keys()):
                    if key != 'current_step':
                        del st.session_state[key]
                st.session_state.current_step = 1
                st.rerun()
        
        with col2:
            if st.button("📋 View Full Config"):
                st.json(config)
        
        with col3:
            # Download the combined SQL
            if sql_script:
                st.download_button(
                    "💾 Download SQL",
                    sql_script,
                    file_name=f"{config['database_prefix']}_complete_setup.sql",
                    mime="text/sql"
                )


def generate_all_code():
    """Generate all SQL scripts and Streamlit app"""
    config = st.session_state.project_config
    
    # For now, generate code inline (will be extracted to modules later)
    # This keeps the app simple for Streamlit in Snowflake (no external imports)
    
    sql_scripts = generate_sql_scripts_inline(config)
    streamlit_app = generate_streamlit_app_inline(config)
    docs = generate_documentation_inline(config)
    
    # Store in session state
    st.session_state.generated_code = {
        'sql_scripts': sql_scripts,
        'streamlit_app': streamlit_app,
        'readme': docs['readme'],
        'deployment_guide': docs['deployment_guide']
    }
    
    # Save to governance/history table
    save_project_to_history(config, sql_scripts, streamlit_app)


def save_project_to_history(config, sql_scripts, streamlit_app):
    """Save generated project to history table for governance"""
    try:
        # Ensure governance schema exists
        session.sql("CREATE SCHEMA IF NOT EXISTS GENERATOR_GOVERNANCE").collect()
        
        # Create history table if it doesn't exist
        create_history_table = """
        CREATE TABLE IF NOT EXISTS GENERATOR_GOVERNANCE.PROJECT_HISTORY (
            project_id VARCHAR(100) PRIMARY KEY DEFAULT UUID_STRING(),
            project_name VARCHAR(255),
            database_name VARCHAR(255),
            generated_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            generated_by VARCHAR(255) DEFAULT CURRENT_USER(),
            table_count INTEGER,
            total_columns INTEGER,
            configuration VARIANT,
            sql_script TEXT,
            streamlit_app_code TEXT,
            status VARCHAR(50) DEFAULT 'GENERATED'
        )
        """
        session.sql(create_history_table).collect()
        
        # Save this project
        import json
        
        table_count = len(config.get('tables', []))
        total_columns = sum(len(t.get('columns', [])) for t in config.get('tables', []))
        config_json = json.dumps(config)
        
        # Escape quotes for SQL
        config_json_escaped = config_json.replace("'", "''")
        sql_escaped = list(sql_scripts.values())[0].replace("'", "''") if sql_scripts else ""
        app_escaped = streamlit_app.replace("'", "''")
        
        insert_history = f"""
        INSERT INTO GENERATOR_GOVERNANCE.PROJECT_HISTORY
        (project_name, database_name, table_count, total_columns, configuration, sql_script, streamlit_app_code)
        SELECT 
            '{config.get('project_name', 'Unnamed')}',
            '{config.get('database_name', '')}',
            {table_count},
            {total_columns},
            PARSE_JSON('{config_json_escaped}'),
            '{sql_escaped}',
            '{app_escaped}'
        """
        
        session.sql(insert_history).collect()
        
    except Exception as e:
        # Don't fail generation if history save fails
        st.warning(f"Note: Project history save: {str(e)}")


def generate_sql_scripts_inline(config):
    """Generate SQL scripts based on configuration - ALL IN ONE FILE"""
    
    db_name = config['database_name']
    db_prefix = config['database_prefix']
    
    # Combine everything into ONE comprehensive SQL script
    combined_sql = f"""-- ============================================================================
-- {config['project_name']} - Database Setup
-- ============================================================================
-- Generated by Streamlit App Generator
-- Date: {datetime.now().strftime('%Y-%m-%d')}
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- Create Database (IF NOT EXISTS to preserve existing data)
CREATE DATABASE IF NOT EXISTS {db_name}
    COMMENT = '{config.get('description', config['project_name'])}';

USE DATABASE {db_name};

-- Create Schemas (IF NOT EXISTS to preserve existing data)
CREATE SCHEMA IF NOT EXISTS {config['schema_raw']}
    COMMENT = 'Raw data capture tables';

CREATE SCHEMA IF NOT EXISTS {config['schema_apps']}
    COMMENT = 'Application and reference data';

CREATE SCHEMA IF NOT EXISTS AUDIT
    COMMENT = 'Audit and logging tables';

-- Create Roles
CREATE ROLE IF NOT EXISTS {db_prefix}_ADMIN
    COMMENT = 'Administrator role for {config['project_name']}';

CREATE ROLE IF NOT EXISTS {db_prefix}_USER
    COMMENT = 'Standard user role';

CREATE ROLE IF NOT EXISTS {db_prefix}_READONLY
    COMMENT = 'Read-only access role';

-- Grant Role Hierarchy
GRANT ROLE {db_prefix}_ADMIN TO ROLE SYSADMIN;
GRANT ROLE {db_prefix}_USER TO ROLE {db_prefix}_ADMIN;
GRANT ROLE {db_prefix}_READONLY TO ROLE {db_prefix}_USER;

-- Grant Permissions (using existing warehouse: {config.get('warehouse_name', 'COMPUTE_WH')})
GRANT USAGE ON DATABASE {db_name} TO ROLE {db_prefix}_USER;
GRANT USAGE ON SCHEMA {db_name}.{config['schema_raw']} TO ROLE {db_prefix}_USER;
GRANT USAGE ON SCHEMA {db_name}.{config['schema_apps']} TO ROLE {db_prefix}_USER;
GRANT USAGE ON WAREHOUSE {config.get('warehouse_name', 'COMPUTE_WH')} TO ROLE {db_prefix}_USER;

SELECT 'Database setup complete!' as status;

-- ============================================================================
-- CREATE TABLES
-- ============================================================================

USE DATABASE {db_name};
USE SCHEMA {config['schema_raw']};

"""
    
    # Add table definitions
    table_definitions = ""
    for table in config['tables']:
        columns_def = []
        for col in table['columns']:
            required = "NOT NULL" if col['required'] else ""
            columns_def.append(f"    {col['name']} {col['type']} {required}")
        
        columns_sql = ",\n".join(columns_def)
        
        table_definitions += f"""
-- {table['table_name']}
CREATE TABLE IF NOT EXISTS {config['schema_raw']}.{table['table_name']} (
    record_id VARCHAR(50) PRIMARY KEY DEFAULT UUID_STRING(),
{columns_sql},
    created_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    created_by VARCHAR(255) DEFAULT CURRENT_USER(),
    last_modified_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    last_modified_by VARCHAR(255) DEFAULT CURRENT_USER()
);

"""
    
    # Append table definitions to combined_sql
    combined_sql += table_definitions
    combined_sql += "\nSELECT 'Tables created successfully!' as status;\n\n"
    
    # Reference data removed per user request
    # Teams can add their own reference tables if needed
    
    # Add Security (if enabled)
    if False:  # Disabled reference data
        combined_sql += f"""-- ============================================================================
-- REFERENCE DATA
-- ============================================================================

USE SCHEMA {config['schema_apps']};

"""
        ref_definitions = ""
        ref_inserts = ""
        
        for ref in config['reference_data']:
            ref_definitions += f"""
CREATE OR REPLACE TABLE {config['schema_apps']}.{ref['table_name']} (
    value VARCHAR(255) PRIMARY KEY,
    display_order INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

"""
            values_sql = []
            for idx, val in enumerate(ref['values']):
                val_escaped = val.replace("'", "''")
                values_sql.append(f"SELECT '{val_escaped}', {idx + 1}, TRUE, CURRENT_TIMESTAMP()")
            
            ref_inserts += f"""
INSERT INTO {config['schema_apps']}.{ref['table_name']}
{' UNION ALL '.join(values_sql)};

"""
        
        combined_sql += ref_definitions
        combined_sql += ref_inserts
        combined_sql += "\nSELECT 'Reference data loaded!' as status;\n\n"
    
    # Add Security (if enabled)
    if config.get('security_features', {}).get('rbac'):
        combined_sql += f"""-- ============================================================================
-- SECURITY SETUP
-- ============================================================================

-- Grant table permissions
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA {config['schema_raw']} TO ROLE {db_prefix}_USER;
GRANT SELECT ON ALL TABLES IN SCHEMA {config['schema_apps']} TO ROLE {db_prefix}_USER;
GRANT SELECT ON ALL TABLES IN SCHEMA {config['schema_raw']} TO ROLE {db_prefix}_READONLY;

-- Grant future permissions
GRANT SELECT, INSERT, UPDATE ON FUTURE TABLES IN SCHEMA {config['schema_raw']} TO ROLE {db_prefix}_USER;
GRANT SELECT ON FUTURE TABLES IN SCHEMA {config['schema_apps']} TO ROLE {db_prefix}_USER;

SELECT 'Security configured!' as status;

"""
    
    # Add Audit Framework (if enabled)
    if config.get('audit_enabled'):
        combined_sql += f"""-- ============================================================================
-- AUDIT FRAMEWORK
-- ============================================================================

USE SCHEMA AUDIT;

-- Audit Log Table (IF NOT EXISTS to preserve existing audit data)
CREATE TABLE IF NOT EXISTS AUDIT_LOG (
    audit_id VARCHAR(50) PRIMARY KEY DEFAULT UUID_STRING(),
    table_name VARCHAR(255),
    operation VARCHAR(50),
    user_name VARCHAR(255) DEFAULT CURRENT_USER(),
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    record_id VARCHAR(50),
    changes VARIANT
);

SELECT 'Audit framework created!' as status;

"""
    
    # Final message
    combined_sql += f"""-- ============================================================================
-- SETUP COMPLETE
-- ============================================================================

SELECT '{config['project_name']} - Setup Complete!' as final_status;
SELECT 'Database: {db_name}' as info;
SELECT 'Ready for Streamlit app deployment' as next_step;
"""
    
    # Return as single script
    return {
        'complete_setup.sql': combined_sql
    }


def generate_streamlit_app_inline(config):
    """Generate the Streamlit application"""
    
    db_name = config['database_name']
    schema_raw = config['schema_raw']
    
    # Build the header
    header_line = '=' * (len(config['project_name']) + 30)
    gen_date = datetime.now().strftime('%Y-%m-%d')
    
    # Build the app code in parts to avoid f-string complexity
    app_header = f'''"""
{config['project_name']} - Data Capture Application
{header_line}
Generated by Streamlit App Generator
Date: {gen_date}

⚠️ DEPLOYMENT: Streamlit in Snowflake
   - Python 3.11
   - No external packages
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import snowflake.snowpark.context as snowpark_context

# Initialize Snowflake session
session = snowpark_context.get_active_session()

# Page configuration
st.set_page_config(
    page_title="{config['project_name']}",
    page_icon="📝",
    layout="wide"
)

# Header
st.title("📝 {config['project_name']}")
st.markdown("*{config.get('description', 'Data capture application')}*")

'''
    
    # Generate form functions
    form_functions = []
    table_names = []
    
    for table in config['tables']:
        table_name = table['table_name']
        table_display = table_name.replace('_', ' ').title()
        table_names.append(table_display)
        
        # Build form inputs
        form_inputs = []
        timestamp_columns = []
        
        for col in table['columns']:
            col_name = col['name']
            col_type_upper = col['type'].upper()
            col_display = col_name.replace('_', ' ').title()
            required = " *" if col['required'] else ""
            
            if 'TIMESTAMP' in col_type_upper:
                # For timestamp, we need both date and time
                timestamp_columns.append(col_name)
                form_inputs.append(f"            col1, col2 = st.columns(2)")
                form_inputs.append(f"            with col1:")
                form_inputs.append(f"                {col_name}_date = st.date_input('{col_display} Date{required}', key='{table_name.lower()}_{col_name}_date')")
                form_inputs.append(f"            with col2:")
                form_inputs.append(f"                {col_name}_time = st.time_input('{col_display} Time{required}', key='{table_name.lower()}_{col_name}_time')")
                form_inputs.append(f"            # Combine date and time")
                form_inputs.append(f"            {col_name} = f'{{str({col_name}_date)}} {{str({col_name}_time)}}'")
            else:
                # Regular widget
                widget_type = get_widget_for_datatype(col['type'])
                form_inputs.append(f"            {col_name} = st.{widget_type}('{col_display}{required}', key='{table_name.lower()}_{col_name}')")
        
        # Build INSERT query parts
        col_names = [col['name'] for col in table['columns']]
        col_names_str = ', '.join(col_names)
        
        # Build code that constructs the VALUES clause at runtime
        values_parts = []
        
        for col in table['columns']:
            col_name = col['name']
            col_type_upper = col['type'].upper()
            
            if 'VARCHAR' in col_type_upper or 'TEXT' in col_type_upper:
                # String - will be: "'value'"
                values_parts.append(f"\"'\" + str({col_name}).replace(\"'\", \"''\") + \"'\"")
            elif 'DATE' in col_type_upper or 'TIMESTAMP' in col_type_upper:
                # Date/Timestamp - will be: "'2025-11-03'"
                values_parts.append(f"\"'\" + str({col_name}) + \"'\"")
            else:
                # Numeric/boolean - will be: "123" or "TRUE"
                values_parts.append(f"str({col_name})")
        
        values_expr = ' + ", " + '.join(values_parts)
        
        # Build edit form inputs and UPDATE clauses
        edit_input_lines = []
        update_set_lines = []
        
        for col in table['columns']:
            if 'TIMESTAMP' not in col['type'].upper():
                col_name = col['name']
                col_upper = col_name.upper()
                col_display = col_name.replace('_', ' ').title()
                widget = get_widget_for_datatype(col['type'])
                
                edit_input_lines.append(f"                        edit_{col_name} = st.{widget}('{col_display}', value=str(record_data['{col_upper}']), key='edit_{col_name}')")
                
                # Build UPDATE SET clause with proper type handling
                if 'VARCHAR' in col['type'].upper() or 'TEXT' in col['type'].upper() or 'DATE' in col['type'].upper():
                    # String/date columns need quotes and escaping
                    update_set_lines.append(f"                                {col_name}_val = str(edit_{col_name}).replace(\"'\", \"''\")")
                    update_set_lines.append(f"                                set_clauses.append(\"{col_name} = '\" + {col_name}_val + \"'\")")
                else:
                    # Numeric columns don't need quotes
                    update_set_lines.append(f"                                set_clauses.append(\"{col_name} = \" + str(edit_{col_name}))")
        
        edit_inputs_str = '\n'.join(edit_input_lines)
        update_sets_str = '\n'.join(update_set_lines)
        
        # Build form function with tabs for Create and View/Edit
        form_func = f'''
def render_{table_name.lower()}_form():
    """Form for {table.get('description', table_name)}"""
    st.markdown("### {table.get('description', table_display)}")
    
    # Tabs for Create and View/Edit
    tab1, tab2 = st.tabs(["➕ Create New", "📋 View/Edit Records"])
    
    with tab1:
        st.markdown("#### Create New Record")
        
        with st.form("{table_name.lower()}_form"):
{chr(10).join(form_inputs)}
            
            submitted = st.form_submit_button("Submit {table_display}")
            
            if submitted:
                try:
                    # Build INSERT query with proper value quoting
                    values_clause = {values_expr}
                    
                    query = f"""
                    INSERT INTO {db_name}.{schema_raw}.{table_name}
                    ({col_names_str})
                    SELECT {{values_clause}}
                    """
                    session.sql(query).collect()
                    st.success("✅ Record saved successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving record: {{str(e)}}")
    
    with tab2:
        st.markdown("#### View & Edit Records")
        
        # Query existing records
        try:
            view_query = """
            SELECT record_id, {col_names_str}, created_timestamp, created_by, last_modified_timestamp
            FROM {db_name}.{schema_raw}.{table_name}
            ORDER BY created_timestamp DESC
            """
            df = session.sql(view_query).to_pandas()
            
            if not df.empty:
                st.markdown(f"**Total Records:** {{len(df)}}")
                
                # Display records with selection
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown("#### ✏️ Edit Record")
                st.info("💡 Select a Record ID from the dropdown below to edit")
                
                # Select record to edit
                record_ids = df['RECORD_ID'].tolist()
                selected_record = st.selectbox(
                    "Select Record ID to Edit", 
                    [""] + record_ids,
                    format_func=lambda x: "Choose a record..." if x == "" else x
                )
                
                if selected_record:
                    record_data = df[df['RECORD_ID'] == selected_record].iloc[0]
                    
                    with st.form("edit_form"):
                        st.success(f"📝 Editing: {{selected_record}}")
                        
                        # Show created info
                        st.caption(f"Created: {{record_data['CREATED_TIMESTAMP']}} by {{record_data['CREATED_BY']}}")
                        
{edit_inputs_str}
                        
                        update_submitted = st.form_submit_button("💾 Update Record")
                        
                        if update_submitted:
                            try:
                                # Build UPDATE SET clause
                                set_clauses = []
{update_sets_str}
                                
                                update_query = f"""
                                UPDATE {db_name}.{schema_raw}.{table_name}
                                SET {{', '.join(set_clauses)}},
                                    last_modified_timestamp = CURRENT_TIMESTAMP(),
                                    last_modified_by = CURRENT_USER()
                                WHERE record_id = '{{selected_record}}'
                                """
                                session.sql(update_query).collect()
                                st.success("✅ Record updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating record: {{str(e)}}")
            else:
                st.info("📝 No records yet. Create your first record in the 'Create New' tab!")
        except Exception as e:
            st.error(f"Error loading records: {{str(e)}}")
'''
        form_functions.append(form_func)
    
    # Build navigation
    nav_section = f'''
# Sidebar navigation
with st.sidebar:
    st.markdown("## Navigation")
    page = st.selectbox(
        "Select Form",
        {table_names}
    )

'''
    
    # Build routing
    routing_code = '\n'.join(form_functions)
    
    page_routing = '\n'.join([f"if page == '{tn}':\n    render_{config['tables'][i]['table_name'].lower()}_form()" for i, tn in enumerate(table_names)])
    
    # Combine all parts
    app_code = app_header + nav_section + routing_code + '\n\n# Route to forms\n' + page_routing + '''

# Footer
st.markdown("---")
st.markdown("*Generated by Streamlit App Generator | Powered by Snowflake*")
'''
    
    return app_code


def get_widget_for_datatype(datatype):
    """Map SQL datatypes to Streamlit widgets"""
    datatype_upper = datatype.upper()
    
    if 'VARCHAR' in datatype_upper or 'TEXT' in datatype_upper:
        return 'text_input'
    elif 'INTEGER' in datatype_upper or 'NUMBER' in datatype_upper:
        return 'number_input'
    elif 'FLOAT' in datatype_upper or 'DECIMAL' in datatype_upper:
        return 'number_input'
    elif 'BOOLEAN' in datatype_upper:
        return 'checkbox'
    elif 'DATE' in datatype_upper:
        return 'date_input'
    elif 'TIMESTAMP' in datatype_upper:
        return 'date_input'  # Can enhance with time later
    else:
        return 'text_input'


def generate_documentation_inline(config):
    """Generate documentation files"""
    
    readme = f"""# {config['project_name']}

## Overview
{config.get('description', 'Data capture application')}

**Team:** {config.get('team_name', 'N/A')}  
**Contact:** {config.get('primary_contact', 'N/A')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d')}

## Database Structure

**Database:** `{config['database_name']}`  
**Schemas:**
- `{config['schema_raw']}` - Data capture tables
- `{config['schema_apps']}` - Reference data
- `AUDIT` - Audit logs

**Tables:** {len(config['tables'])}
{chr(10).join([f"- {t['table_name']}: {t.get('description', 'Data table')}" for t in config['tables']])}

## Deployment

1. Run SQL scripts in order (01, 02, 03, etc.)
2. Deploy Streamlit app to Snowflake
3. Use Python 3.11 runtime
4. No packages needed

## Generated Files

- SQL Scripts: Database setup, tables, reference data, security, audit
- Streamlit App: Complete data capture interface
- Documentation: This README and deployment guide
"""
    
    deployment_guide = f"""# Deployment Guide - {config['project_name']}

## Quick Start

### 1. Execute SQL Scripts

Run in order as ACCOUNTADMIN:

```sql
-- 01_setup_database.sql
-- 02_create_tables.sql  
-- 03_reference_data.sql (if exists)
-- 04_security_setup.sql (if exists)
-- 05_audit_framework.sql (if exists)
```

### 2. Deploy Streamlit App

**In Snowsight:**
1. Go to Streamlit Apps
2. Click "+ Streamlit App"
3. **Python Version: 3.11** ⚠️
4. Database: `{config['database_name']}`
5. Schema: `{config['schema_apps']}`
6. Paste the app code
7. Click Run

### 3. Access

Users can access via Snowsight > Streamlit Apps

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return {
        'readme': readme,
        'deployment_guide': deployment_guide
    }


if __name__ == "__main__":
    main()

