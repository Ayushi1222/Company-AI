"""
Conversational Company Research Assistant & Account Plan Generator

A comprehensive Streamlit application for intelligent company research and account planning.
Features:
- Multi-turn conversational interface
- Adaptive persona detection
- Multi-source data aggregation
- Interactive account plan generation
- PDF/DOCX export
- Text-to-speech support
"""

import streamlit as st
import time
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.conversation_manager import ConversationManager, ConversationState
from research.data_aggregator import DataAggregator
from account_plan.generator import AccountPlanGenerator
from export.pdf_exporter import PDFExporter
from export.docx_exporter import DOCXExporter
from utils.validators import validate_company_name, validate_file_upload
from utils.error_handlers import show_missing_api_keys_warning
from utils.tts import add_tts_button
from config.settings import FEATURES

st.set_page_config(
    page_title="Company Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.2rem;
        color:
        font-weight: 600;
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }
    
    /* Navbar container */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Button styling */
    .stButton button {
        height: 2.8rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border-radius: 8px;
        font-size: 0.95rem;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color:
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] h2 {
        color:
        font-size: 1.3rem;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 0.95rem;
    }
    
    /* Chat messages */
    .user-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        background-color:
        border-left: 4px solid
    }
    
    .assistant-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid
    }
    
    .status-box {
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid
    }
    
    /* Section headers */
    .section-header {
        color:
        border-bottom: 2px solid
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        font-weight: 600;
    }
    
    /* Navbar alignment */
    .navbar-container {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        margin-bottom: 0.5rem;
    }
    
    /* Download button styling */
    .stDownloadButton button {
        color: white;
        font-weight: 600;
        height: 3rem;
        font-size: 1.1rem;
    }
    
    .stDownloadButton button:hover {
        transform: scale(1.02);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color:
    }
    
    /* Divider styling */
    hr {
        margin: 1rem 0;
        border-color:
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        border-radius: 8px 8px 0 0;
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize all session state variables."""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    
    if 'data_aggregator' not in st.session_state:
        st.session_state.data_aggregator = DataAggregator()
    
    if 'plan_generator' not in st.session_state:
        st.session_state.plan_generator = AccountPlanGenerator()
    
    if 'current_research' not in st.session_state:
        st.session_state.current_research = None
    
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = None
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'researching' not in st.session_state:
        st.session_state.researching = False
    
    if 'export_data' not in st.session_state:
        st.session_state.export_data = None


def display_chat_message(role: str, content: str, timestamp: str = None):
    """Display a chat message."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <small><b>You</b> • {timestamp}</small><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <small><b>🤖 Assistant</b> • {timestamp}</small><br>
            {content}
        </div>
        """, unsafe_allow_html=True)


def show_status(message: str):
    """Display a status message."""
    st.markdown(f"""
    <div class="status-box">
        {message}
    </div>
    """, unsafe_allow_html=True)


def conduct_research(company_name: str, domain: str = None):
    """Conduct company research."""
    conv_manager = st.session_state.conversation_manager
    data_agg = st.session_state.data_aggregator
    
    conv_manager.set_state(ConversationState.RESEARCHING)
    st.session_state.researching = True
    
    status_placeholder = st.empty()
    
    try:
        with st.spinner("🔍 Researching company..."):
            status_placeholder.info("📊 Gathering data from multiple sources...")
            research_data = data_agg.research_company(
                company_name=company_name,
                company_domain=domain,
                include_news=True,
                include_officers=False
            )
        
        with st.spinner("📋 Generating account plan..."):
            status_placeholder.info("✨ Creating account plan structure...")
            plan = st.session_state.plan_generator.generate(research_data)
        
        st.session_state.current_research = research_data
        st.session_state.current_plan = plan
        
        conv_manager.set_state(ConversationState.PRESENTING_RESULTS)
        st.session_state.researching = False
        
        status_placeholder.success("✅ Research complete!")
        time.sleep(1)
        status_placeholder.empty()
        
        return True
        
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        status_placeholder.error(f"❌ Research failed: {str(e)}")
        st.session_state.researching = False
        conv_manager.set_state(ConversationState.IDLE)
        return False


def display_account_plan():
    """Display the account plan in tabs."""
    if not st.session_state.current_plan:
        return
    
    plan = st.session_state.current_plan
    sections = plan['sections']
    
    st.markdown('<h2 class="section-header">📋 Account Plan</h2>', unsafe_allow_html=True)
    
    tab_names = [s['title'] for s in sections.values()]
    tabs = st.tabs(tab_names)
    
    for tab, (section_key, section) in zip(tabs, sections.items()):
        with tab:
            st.markdown(f"
            
            content = section['content']
            
            if isinstance(content, dict):
                for key, value in content.items():
                    key_formatted = key.replace('_', ' ').title()
                    st.markdown(f"**{key_formatted}:**")
                    
                    if isinstance(value, list):
                        for item in value:
                            st.markdown(f"• {item}")
                    else:
                        st.write(value)
                    
                    st.markdown("")
            
            if section.get('editable', False):
                with st.expander("✏️ Edit Section"):
                    st.info("Manual editing coming soon! For now, regenerate the plan or use export to edit in Word.")


def display_research_summary():
    """Display research data summary."""
    if not st.session_state.current_research:
        return
    
    research = st.session_state.current_research
    
    with st.expander("📊 Research Data Summary", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Sources Used", len(research.get('sources_used', [])))
            st.metric("News Articles", len(research.get('news', [])))
        
        with col2:
            st.metric("Data Conflicts", len(research.get('conflicts', [])))
            st.write(f"**Status:** {research.get('status', 'unknown')}")
        
        if research.get('sources_used'):
            st.write("**Data Sources:**")
            for source in research['sources_used']:
                st.write(f"✓ {source}")
        
        if research.get('conflicts'):
            st.warning(f"⚠️ Found {len(research['conflicts'])} data conflicts. Review recommended.")


def export_plan(format: str):
    """Export account plan and return export data."""
    if not st.session_state.current_plan:
        st.error("No account plan to export")
        return None
    
    plan = st.session_state.current_plan
    company_name = plan['metadata']['company_name']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        if format == "PDF":
            exporter = PDFExporter()
            buffer = exporter.export(plan)
            filename = f"{company_name}_Account_Plan_{timestamp}.pdf"
            mime = "application/pdf"
        
        elif format == "DOCX":
            exporter = DOCXExporter()
            buffer = exporter.export(plan)
            filename = f"{company_name}_Account_Plan_{timestamp}.docx"
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        else:
            st.error("Unsupported format")
            return None
        
        return {
            'buffer': buffer,
            'filename': filename,
            'mime': mime,
            'format': format
        }
        
    except Exception as e:
        st.error(f"Export failed: {str(e)}")
        logger.error(f"Export error: {str(e)}")
        return None


def main():
    """Main application."""
    initialize_session_state()
    
    conv_manager = st.session_state.conversation_manager
    
    st.markdown('<div style="padding: 0.5rem 0; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
    
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([4, 1.5, 1.2, 1.2])
    
    with nav_col1:
        st.markdown('''
            <div style="display: flex; align-items: center; height: 100%;">
                <h1 class="main-header">🔍 Company Research Assistant</h1>
            </div>
        ''', unsafe_allow_html=True)
    
    with nav_col2:
        if st.button("🔄 New Conversation", use_container_width=True, key="new_conv_btn"):
            conv_manager.reset()
            st.session_state.current_research = None
            st.session_state.current_plan = None
            st.session_state.messages = []
            st.session_state.export_data = None
            st.rerun()
    
    with nav_col3:
        if st.session_state.current_plan:
            if st.button("📄 Export PDF", use_container_width=True, key="export_pdf_btn"):
                st.session_state.export_data = export_plan("PDF")
                st.rerun()
        else:
            st.markdown('<div style="height: 2.8rem;"></div>', unsafe_allow_html=True)
    
    with nav_col4:
        if st.session_state.current_plan:
            if st.button("📝 Export DOCX", use_container_width=True, key="export_docx_btn"):
                st.session_state.export_data = export_plan("DOCX")
                st.rerun()
        else:
            st.markdown('<div style="height: 2.8rem;"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('''
        <p style="text-align: center; color:
            Conversational AI for intelligent company research and account planning
        </p>
    ''', unsafe_allow_html=True)
    
    if st.session_state.export_data:
        export_info = st.session_state.export_data
        
        st.markdown("""
            <div style="padding: 1.5rem; border-radius: 12px; margin: 1rem 0; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="color: white; margin: 0 0 0.5rem 0; text-align: center;">
                    ✅ Export Ready!
                </h3>
                <p style="color: rgba(255,255,255,0.9); margin: 0; text-align: center;">
                    Your account plan has been generated successfully
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col_dl1, col_dl2, col_dl3 = st.columns([1, 3, 1])
        with col_dl2:
            st.download_button(
                label=f"⬇️ Download {export_info['filename']}",
                data=export_info['buffer'],
                file_name=export_info['filename'],
                mime=export_info['mime'],
                use_container_width=True,
                key="download_export_btn",
                type="primary"
            )
            
            if st.button("✖️ Close", key="close_export", use_container_width=True):
                st.session_state.export_data = None
                st.rerun()
    
    st.divider()
    
    with st.sidebar:
        st.markdown("
        st.markdown("""
        <div style=" padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="margin: 0; line-height: 1.6;">This AI assistant helps you:</p>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem; line-height: 1.8;">
                <li>Research companies from multiple sources</li>
                <li>Generate comprehensive account plans</li>
                <li>Export professional reports</li>
                <li>Adapt to your communication style</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        persona = conv_manager.get_persona()
        if persona != "neutral":
            st.info(f"**🎭 Communication Style:** {persona.title()}\n\n{conv_manager.persona_detector.get_persona_description()}")
        
        st.divider()
        
        st.markdown("
        show_missing_api_keys_warning()
        
        st.divider()
        
        st.markdown("
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Messages", len(st.session_state.messages))
        with col_info2:
            st.metric("State", conv_manager.get_state().name if hasattr(conv_manager.get_state(), 'name') else str(conv_manager.get_state()))
        
        if st.session_state.current_plan:
            st.success("✅ Account Plan Ready")
        
        st.divider()
        
        with st.expander("❓ Help & Examples", expanded=False):
            st.markdown("""
            **Example Queries:**
            
            - "Research Microsoft"
            - "Find information about Stripe"
            - "Analyze Tesla and create an account plan"
            
            **💡 Tips:**
            
            - Be specific with company names
            - Provide domain names when possible
            - Ask follow-up questions anytime
            - Export plans as PDF or DOCX
            """)
        
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; font-size: 0.85rem; color:
                <p>v1.0.0 | Built with ❤️</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h3 style="color:
    
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
                <div style="text-align: center; padding: 3rem 1rem; background-color:
                            border-radius: 12px; border: 2px dashed
                    <h4 style="color:
                    <p style="color:
                </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                display_chat_message(
                    message.get('role'),
                    message.get('content'),
                    message.get('timestamp')
                )
    
    user_input = st.chat_input("Ask me about a company...")
    
    if user_input:
        is_valid, error_msg = validate_company_name(user_input)
        
        if not is_valid:
            st.error(error_msg)
        else:
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                'role': 'user',
                'content': user_input,
                'timestamp': timestamp
            })
            
            result = conv_manager.process_user_message(user_input)
            
            if result.get('response'):
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': result['response'],
                    'timestamp': datetime.now().strftime("%H:%M")
                })
            
            action = result.get('action')
            
            if action == 'start_research':
                company = result.get('company')
                if conduct_research(company):
                    success_msg = f"✅ Research complete for **{company}**! Review the account plan below."
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': success_msg,
                        'timestamp': datetime.now().strftime("%H:%M")
                    })
            
            st.rerun()
    
    if st.session_state.current_plan:
        st.divider()
        display_research_summary()
        st.divider()
        display_account_plan()
    
    st.divider()
    st.markdown("""
    <div style="text-align: center; color:
        <p>Built with ❤️ for intelligent company research</p>
        <p>Data sources: NewsAPI, Hunter.io, Brandfetch, OpenCorporates, Web Scraping</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
