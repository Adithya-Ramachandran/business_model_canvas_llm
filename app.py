# app.py

import streamlit as st

# Import from your new modules
from src.ui_components import display_card
from src.canvas_state import initialize_canvas_state, save_canvas_to_file, load_canvas_from_file
from src.gemini_client import handle_llm_request
from src.constants import CANVAS_SECTIONS_MAP


def setup_page_style():
    """Injects custom CSS for styling the app."""
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #F0F2F6; }
        .st-emotion-cache-z5fcl4 { padding: 1rem 1rem 0.5rem; }
        .st-emotion-cache-1r6dm7m { padding: 1rem; }
        h1, h2, h3, h4, h5, h6 { color: #F0F2F6; margin-top: 0.5rem; margin-bottom: 0.5rem; }
        p { color: #E0E0E0; margin-bottom: 0.2rem; margin-top: 0.2rem; }
        .user-segment-text { font-size: 0.9em; margin-top: -5px; margin-bottom: 5px; color: #E0E0E0; }

        /* --- Default Green Buttons --- */
        .stButton>button {
            border-radius: 0.5rem;
            color: #F0F2F6;
            background-color: #0080FE;
            border-color: #00080;
        }
        .stButton>button:hover {
            background-color: #45a049;
            border-color: #45a049;
        }

        /* LLM Chat Box Styles */
        .llm-suggestion-box { background-color: #1A1A1A; border-left: 3px solid #6495ED; padding: 10px; margin: 5px 0; border-radius: 4px; font-size: 0.9em; color: #E0E0E0; }
        .llm-user-prompt { background-color: #333333; padding: 8px; margin: 5px 0; border-radius: 4px; font-size: 0.9em; color: #F0F2F6; }
        </style>
    """, unsafe_allow_html=True)


# The rest of your app.py file remains exactly the same.
def build_sidebar():
    """Builds the sidebar UI for canvas actions and LLM interaction."""
    with st.sidebar:
        st.header("Canvas Actions")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='save-button'>", unsafe_allow_html=True)
            st.button("Save", on_click=save_canvas_to_file, use_container_width=True,
                      help="Save your canvas to a local JSON file.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='load-button'>", unsafe_allow_html=True)
            st.button("Load", on_click=load_canvas_from_file, use_container_width=True,
                      help="Load a canvas from a JSON file.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='new-button'>", unsafe_allow_html=True)
            if st.button("New", use_container_width=True, help="Clear all fields and start a new canvas."):
                initialize_canvas_state(reset=True)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.header("AI Thinking Partner")
        st.markdown("<p style='font-size:0.9em;'>Select a mode and section, then ask for help.</p>",
                    unsafe_allow_html=True)

        interaction_mode = st.selectbox(
            "Choose interaction mode:",
            options=["Ask Critical Questions", "Play Devil's Advocate", "Break It Down", "Suggest Ideas"],
            key="llm_interaction_mode"
        )

        selected_section_name = st.selectbox(
            "Target Canvas Section:",
            options=list(CANVAS_SECTIONS_MAP.keys()),
            key="llm_target_section_select"
        )
        selected_section_key = CANVAS_SECTIONS_MAP[selected_section_name]

        current_llm_prompt = st.text_area("Your question or current thoughts:", key="llm_current_prompt_input",
                                          height=100)

        if st.button("Get Help from Assistant", use_container_width=True):
            if current_llm_prompt:
                handle_llm_request(current_llm_prompt, selected_section_key, selected_section_name, interaction_mode)
            else:
                st.warning("Please enter your thoughts or a question for the assistant.")

        st.markdown("---")
        st.subheader("Assistant Chat History")

        if st.button("Clear Chat History"):
            st.session_state.llm_chat_history = []
            st.rerun()

        for chat in st.session_state.get('llm_chat_history', []):
            role_class = 'llm-user-prompt' if chat['role'] == 'user' else 'llm-suggestion-box'
            role_name = 'You' if chat['role'] == 'user' else 'AI Assistant'
            st.markdown(f"<div class='{role_class}'><b>{role_name} ({chat['target_key']}):</b> {chat['content']}</div>",
                        unsafe_allow_html=True)


def build_bmc_view():
    """Renders the Business Model Canvas view."""
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>BUSINESS MODEL</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1.8, 1.8, 1.8, 1.8, 1.8])
    with c1:
        st.markdown("<h4>Target groups</h4>", unsafe_allow_html=True)
        display_card("target_groups_customers", "Customers", height=120, title_size="bold", outer_margin_bottom="10px")
        display_card("target_groups_users", "Users", height=120, title_size="bold")
    with c2:
        st.markdown("<h4>Brand & messages</h4>", unsafe_allow_html=True)
        display_card("brand_messages_dna", "DNA", height=300, title_size="bold")
    with c3:
        st.markdown("<h4>Offerings</h4>", unsafe_allow_html=True)
        display_card("offerings_products_services", "Products/Services", height=300, title_size="bold")
    with c4:
        st.markdown("<h4>Resources</h4>", unsafe_allow_html=True)
        display_card("resources_key_internal_assets", "Key Internal Assets", height=300, title_size="bold")
    with c5:
        st.markdown("<h4>Partners</h4>", unsafe_allow_html=True)
        display_card("partners_delivery", "Delivery", height=300, title_size="bold")

    st.markdown("---")
    st.markdown("<h3>Core Operational & Value Delivery</h3>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns([1.5, 1.0, 1.5, 1.5, 1.5])
    with m1:
        display_card("primary_customer_segment", "Primary Customer", height=85, border_color="#FF6347",
                     title_size="bold")
        display_card("jobs_to_get_done_functional", "+ functional jobs", height=85, title_size="bold")
        display_card("jobs_to_get_done_emotional", "+ emotional jobs", height=85, title_size="bold")
    with m2:
        display_card("pains_list", "Pains", height=180, border_color="#FF6347", title_size="bold")
        display_card("gains_list", "Gains", height=180, border_color="#FF6347", title_size="bold")
    with m3:
        display_card("channels_customer", "Channels (Customer)", height=180, title_size="bold")
        display_card("core_value", "Core value", height=180, border_color="#FF6347", title_size="bold")
    with m4:
        display_card("channels_partner", "Channels (Partner)", height=180, title_size="bold")
        display_card("unfair_advantage", "Unfair Advantage", height=180, border_color="#FF6347", title_size="bold")
    with m5:
        display_card("relationships_types", "Relationships", height=180, title_size="bold")
        display_card("processes_internal", "Processes", height=180, title_size="bold")

    st.markdown("---")
    st.markdown("<h3>Profit formula</h3>", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns([1.5, 2.5, 2.5, 2.5])
    with p1:
        display_card("profit_pattern", "Pattern", height=150, title_size="bold")
    with p2:
        display_card("profit_revenue_streams", "Revenue streams & pricing", height=150, title_size="bold")
    with p3:
        display_card("profit_costs", "Costs", height=150, title_size="bold")
    with p4:
        display_card("profit_investments", "Investments", height=150, title_size="bold")


def build_vpc_view():
    """Renders the Value Proposition Canvas view."""
    st.markdown("<h3>Value Proposition Canvas</h3>", unsafe_allow_html=True)
    st.info(
        "The goal is to achieve a 'fit' between what your customer wants (Customer Profile) and what you offer (Value Map). The AI Assistant can help you ensure your 'Pain Relievers' and 'Gain Creators' directly address the customer's Pains and Gains.")

    col_value_map, col_customer_profile = st.columns(2)

    with col_value_map:
        st.markdown("<h4 style='text-align: center;'>Value Map</h4>", unsafe_allow_html=True)
        display_card("offerings_products_services", "Products & Services",
                     st.session_state.get("offerings_products_services",
                                          "*(List the products and services your value proposition is built around.)*"),
                     height=200, title_size="bold", widget_key_prefix="vpc_")
        display_card("gain_creators", "Gain Creators",
                     st.session_state.get("gain_creators",
                                          "*(How do your products/services create gains for the customer? How do they produce outcomes customers desire?)*"),
                     height=200, title_size="bold", border_color="#28a745")
        display_card("pain_relievers", "Pain Relievers",
                     st.session_state.get("pain_relievers",
                                          "*(How do your products/services alleviate specific customer pains?)*"),
                     height=200, title_size="bold", border_color="#dc3545")

    with col_customer_profile:
        st.markdown("<h4 style='text-align: center;'>Customer Profile</h4>", unsafe_allow_html=True)
        display_card("primary_customer_segment", "Customer Segment",
                     st.session_state.get("primary_customer_segment",
                                          "*(Who is the specific customer segment you are targeting with this value proposition?)*"),
                     height=100, title_size="bold", widget_key_prefix="vpc_")
        display_card("gains_list", "Gains",
                     st.session_state.get("gains_list",
                                          "*(What outcomes and benefits do your customers want to achieve?)*"),
                     height=150, title_size="bold", border_color="#28a745", widget_key_prefix="vpc_")
        display_card("pains_list", "Pains",
                     st.session_state.get("pains_list",
                                          "*(What annoys your customers? What are their biggest obstacles and risks?)*"),
                     height=150, title_size="bold", border_color="#dc3545", widget_key_prefix="vpc_")
        display_card("jobs_to_get_done_functional", "Customer Jobs",
                     st.session_state.get("jobs_to_get_done_functional",
                                          "*(What functional, social, or emotional jobs are customers trying to get done?)*"),
                     height=150, title_size="bold", widget_key_prefix="vpc_")


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="wide", page_title="Business Model & Value Proposition Canvas",
                       initial_sidebar_state="expanded")
    setup_page_style()
    initialize_canvas_state()
    st.title("Interactive Business Model & Value Proposition Canvas")
    build_sidebar()

    st.subheader("Your Business Idea Overview")
    display_card(
        "business_idea_description", "Describe your overall business idea...",
        st.session_state.get("business_idea_description",
                             "*(e.g., 'A mobile app that connects local artisans with customers...')*"),
        height=150, outer_margin_bottom="20px", is_business_description=True
    )
    st.markdown("---")

    bmc_tab, vpc_tab = st.tabs(["Business Model Canvas", "Value Proposition Canvas"])

    with bmc_tab:
        build_bmc_view()

    with vpc_tab:
        build_vpc_view()


if __name__ == "__main__":
    main()