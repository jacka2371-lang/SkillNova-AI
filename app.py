import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
import pandas as pd
import re
from registration import show_registration
from login import show_login
from theme import apply_theme, show_hero
from learning import show_learning_center
from jobs import show_jobs

apply_theme()
st.set_page_config(
    page_title="Resume AI Dashboard",
    page_icon="📄",
    layout="wide"
)

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None


# Login and registration navigation
if not st.session_state["logged_in"]:

    st.title("Resume AI Account")

    page = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True
    )

    if page == "Login":
        show_login()
    else:
        show_registration()

    st.stop()


# Logged-in user's sidebar

# Sidebar profile and navigation
user = st.session_state["user"]

if "profile_icon" not in st.session_state:
    st.session_state["profile_icon"] = "👤"

with st.sidebar:
    st.title("My Account")

    st.write(
        f"{st.session_state['profile_icon']} "
        f"Welcome, {user['name']}!"
    )

    page = st.radio(
    "Navigation",
    [
        "Resume AI Dashboard",
        "🎓 Learning Center",
        "💼 Apply for Jobs",
        "My Profile",
        "Settings",
        "Logout",
    ],
    )

    st.divider()

    if st.button("Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()


# Display the selected page
if page == "👤 My Profile":
    st.title("👤 My Profile")
    st.write("Your account information")

    st.text_input(
        "Full Name",
        value=user["name"],
        disabled=True
    )

    st.text_input(
        "Registered Email",
        value=user["email"],
        disabled=True
    )

    st.info("Your profile information is linked to your account.")

    st.stop()


elif page == "⚙️ Settings":
    st.title("⚙️ Settings")

    st.subheader("Profile Appearance")

    selected_icon = st.selectbox(
        "Choose your profile icon",
        ["👤", "👩", "👨", "🧑"],
        index=["👤", "👩", "👨", "🧑"].index(
            st.session_state["profile_icon"]
        )
    )

    st.session_state["profile_icon"] = selected_icon

    st.subheader("Account")
    st.write("Email:", user["email"])
    st.caption(
        "Password changes and account deletion "
        "are not available yet."
    )

    st.stop()


    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()


# Learning Center page
if page == "🎓 Learning Center":
    show_learning_center(user["id"])
    st.stop()

# Apply for Jobs page
elif page == "💼 Apply for Jobs":
    # The resume skills will be connected after a resume is analyzed.
    resume_skills = st.session_state.get("current_resume_skills", [])
    show_jobs(resume_skills)
    st.stop()

# Main Resume AI Dashboard
st.title("Resume AI Intelligence Skills Management System")
st.write("Compare multiple resumes against a job description.")


SKILLS = [
    "Python", "Java", "C++", "C#", "JavaScript",
    "SQL", "HTML", "CSS", "React",
    "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "Data Analysis",
    "Pandas", "NumPy", "TensorFlow", "PyTorch",
    "Streamlit", "Flask", "Django",
    "Git", "GitHub", "Excel", "Power BI",
    "Communication", "Problem Solving",
    "Teamwork", "Leadership", "Docker",
    "AWS", "Azure", "Linux", "REST API"
]


def extract_resume_text(uploaded_file):
    if uploaded_file.name.lower().endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(
                page.extract_text() or ""
                for page in pdf.pages
            )

    document = Document(
        BytesIO(uploaded_file.getvalue())
    )
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs
    )


def detect_skills(text):
    found = []
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)
    return found


def get_skill_recommendations(missing_skills):
    recommendations = {
        "Python": "Practise functions, lists, dictionaries, file handling, and build a Python project.",
        "Java": "Practise object-oriented programming, collections, exception handling, and build a Java application.",
        "SQL": "Learn SELECT, WHERE, JOIN, GROUP BY, and practise queries using a sample database.",
        "HTML": "Build web pages using semantic HTML and accessible forms.",
        "CSS": "Practise layouts, Flexbox, Grid, responsive design, and styling a webpage.",
        "JavaScript": "Learn variables, functions, arrays, DOM manipulation, and asynchronous programming.",
        "React": "Learn components, props, state, hooks, and build a small interactive application.",
        "Machine Learning": "Study data preparation, train/test splitting, model evaluation, and build a small prediction project.",
        "Deep Learning": "Learn neural networks, training, loss functions, and model evaluation.",
        "Artificial Intelligence": "Study AI fundamentals and build a small practical AI project.",
        "Data Analysis": "Practise cleaning, exploring, visualising, and explaining real datasets.",
        "Pandas": "Practise DataFrames, filtering, missing values, groupby, and merging datasets.",
        "NumPy": "Practise arrays, indexing, vectorised operations, and numerical calculations.",
        "TensorFlow": "Learn tensors, model building, training, and evaluating a basic neural network.",
        "PyTorch": "Practise tensors, automatic differentiation, and building a simple neural network.",
        "Streamlit": "Build an interactive Python dashboard with forms, charts, and data tables.",
        "Flask": "Build a small web application with routes, templates, and form handling.",
        "Django": "Learn models, views, templates, URLs, and database integration.",
        "Git": "Practise commits, branches, merges, and resolving merge conflicts.",
        "GitHub": "Publish projects with clear README files, useful commits, and setup instructions.",
        "Excel": "Practise formulas, lookups, pivot tables, and data visualisation.",
        "Power BI": "Create dashboards using data cleaning, relationships, and interactive reports.",
        "Docker": "Learn images, containers, Dockerfiles, and containerise a small application.",
        "AWS": "Study cloud fundamentals and deploy a small application using an appropriate AWS service.",
        "Azure": "Study cloud fundamentals and deploy a small application using an appropriate Azure service.",
        "Linux": "Practise terminal commands, file permissions, directories, and process management.",
        "REST API": "Learn HTTP methods, status codes, JSON, and how to build or consume an API.",
        "Communication": "Practise explaining technical projects clearly and presenting your work.",
        "Problem Solving": "Solve coding problems regularly and explain your approach before writing code.",
        "Teamwork": "Practise collaborative projects, code reviews, task planning, and documenting contributions.",
        "Leadership": "Practise planning a small project, coordinating tasks, and communicating progress.",
        "C++": "Practise functions, classes, STL containers, and data structures.",
        "C#": "Learn object-oriented programming, collections, exception handling, and build a small application."
    }

    results = []

    for skill in missing_skills:
        suggestion = recommendations.get(
            skill,
            f"Study {skill}, practise it with a small project, and document what you learn."
        )

        results.append({
            "Skill to improve": skill,
            "Recommended next step": suggestion
        })

    return results




st.header("1. Choose Your Job Role")

job_roles = {
    "Python Developer": [
        "Python", "SQL", "Git", "REST API"
    ],
    "Data Analyst": [
        "Python", "SQL", "Pandas", "Excel",
        "Power BI", "Data Analysis"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React"
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Pandas",
        "NumPy", "TensorFlow"
    ],
    "Java Developer": [
        "Java", "SQL", "Git"
    ],
}

selected_role = st.selectbox(
    "Select the job role you want to apply for",
    list(job_roles.keys())
)

job_description = "Required skills: " + ", ".join(
    job_roles[selected_role]
)

st.info(f"Selected role: {selected_role}")
st.write("Skills required:", ", ".join(job_roles[selected_role]))


st.header("2. Upload Candidate Resumes")

uploaded_files = st.file_uploader(
    "Select multiple PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if st.button("Compare Candidates", type="primary"):

    if not job_description.strip():
        st.warning("Please enter a job description.")

    elif not uploaded_files:
        st.warning("Please upload at least one resume.")

    else:
        required_skills = detect_skills(job_description)

        if not required_skills:
            st.warning(
                "No supported skills found in the job description."
            )

        else:
            results = []

            progress = st.progress(0)
            status = st.empty()

            for index, uploaded_file in enumerate(uploaded_files):
                status.write(
                    f"Analyzing {uploaded_file.name}..."
                )

                try:
                    resume_text = extract_resume_text(uploaded_file)
                    resume_skills = detect_skills(resume_text)
                    st.session_state["current_resume_skills"] = resume_skills

                    matched = [
                        skill for skill in required_skills
                        if skill in resume_skills
                    ]

                    missing = [
                        skill for skill in required_skills
                        if skill not in resume_skills
                    ]

                    score = (
                        len(matched) / len(required_skills)
                    ) * 100

                    results.append({
                        "Candidate File": uploaded_file.name,
                        "Match Score (%)": round(score, 1),
                        "Matched Skills": ", ".join(matched),
                        "Missing Skills": ", ".join(missing),
                        "Resume Skills": ", ".join(resume_skills),
                        "Status": "Analyzed"
                    })

                except Exception as error:
                    results.append({
                        "Candidate File": uploaded_file.name,
                        "Match Score (%)": 0.0,
                        "Matched Skills": "",
                        "Missing Skills": "",
                        "Resume Skills": "",
                        "Status": f"Error: {error}"
                    })

                progress.progress(
                    (index + 1) / len(uploaded_files)
                )

            status.empty()
            progress.empty()

            results_df = pd.DataFrame(results)

            # Rank successful analyses by score.
            successful = results_df[
                results_df["Status"] == "Analyzed"
            ].copy()

            failed = results_df[
                results_df["Status"] != "Analyzed"
            ].copy()

            successful = successful.sort_values(
                "Match Score (%)",
                ascending=False,
                kind="stable"
            )

            results_df = pd.concat(
                [successful, failed],
                ignore_index=True
            )

            st.session_state["comparison_results"] = results_df

if "comparison_results" in st.session_state:
    results_df = st.session_state["comparison_results"]

    st.header("3. Candidate Comparison Dashboard")

    successful = results_df[
        results_df["Status"] == "Analyzed"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric("Resumes Uploaded", len(results_df))
    col2.metric("Successfully Analyzed", len(successful))

    if not successful.empty:
        best = successful.iloc[0]
        col3.metric(
            "Highest Skill Match",
            f"{best['Match Score (%)']:.1f}%"
        )

        st.subheader("Ranked Candidates")

        st.dataframe(
            successful[
                [
                    "Candidate File",
                    "Match Score (%)",
                    "Matched Skills",
                    "Missing Skills"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Compare Individual Candidates")

        selected = st.selectbox(
            "Choose a candidate",
            successful["Candidate File"].tolist()
        )
        candidate = successful[
            successful["Candidate File"] == selected
        ].iloc[0]

        st.metric(
            "Skill Match",
            f"{candidate['Match Score (%)']:.1f}%"
        )

        st.write("**Matched skills:**")
        st.write(candidate["Matched Skills"] or "None")

        st.write("**Missing skills:**")
        st.write(candidate["Missing Skills"] or "None")

        st.subheader("Skill Improvement Recommendations")

        missing_text = candidate["Missing Skills"]

        if missing_text.strip():
            missing_skills = [
                skill.strip()
                for skill in missing_text.split(",")
                if skill.strip()
            ]

            recommendations = get_skill_recommendations(
                missing_skills
            )

            st.dataframe(
                pd.DataFrame(recommendations),
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "Only add a skill to your resume if you genuinely "
                "have that skill. Build a project to demonstrate "
                "your abilities."
            )
        else:
            st.success(
                "All detected job-description skills were found "
                "in this resume. Consider reviewing the candidate's "
                "experience and projects as well."
            )

    
    failed = results_df[
        results_df["Status"] != "Analyzed"
    ]

    if not failed.empty:
        st.subheader("Files That Could Not Be Analyzed")
        st.dataframe(failed, use_container_width=True)

    csv_data = results_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "Download Comparison Report (CSV)",
        data=csv_data,
        file_name="resume_comparison_report.csv",
        mime="text/csv"
    )

    st.caption(
        "Rankings reflect overlap with the predefined skill list only. "
        "They do not establish a candidate's overall suitability."
    )
