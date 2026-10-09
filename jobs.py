
import re
import html

import requests
import streamlit as st


JOB_API = "https://remotive.com/api/remote-jobs"


@st.cache_data(ttl=900, show_spinner=False)
def search_remote_jobs(search_term):
    params = {"search": search_term, "limit": 30}

    response = requests.get(
        JOB_API,
        params=params,
        timeout=15,
        headers={"User-Agent": "ResumeSkillsLearningPlatform/1.0"},
    )
    response.raise_for_status()

    payload = response.json()
    jobs = payload.get("jobs", [])

    # Keep only records with the fields needed for a useful result.
    return [
        job for job in jobs
        if job.get("title") and job.get("url")
    ]


def clean_description(description):
    description = re.sub(
        r"(?is)<(script|style).*?>.*?</\1>",
        " ",
        description or "",
    )
    description = re.sub(r"(?i)<br\s*/?>", "\n", description)
    description = re.sub(r"(?i)</p\s*>", "\n", description)
    description = re.sub(r"<[^>]+>", " ", description)
    description = html.unescape(description)
    description = re.sub(r"\s+", " ", description)
    return description.strip()


def show_jobs(resume_skills=None):
    st.title("💼 Apply for Jobs")
    st.caption("Discover remote opportunities and compare them with your skills.")

    resume_skills = resume_skills or []

    if resume_skills:
        st.markdown("**Skills detected from your resume**")
        st.write(", ".join(resume_skills[:20]))
        suggested_search = " ".join(resume_skills[:3])
    else:
        suggested_search = "Python"

    with st.form("job_search_form"):
        search_term = st.text_input(
            "Search role or skills",
            value=suggested_search,
            placeholder="Example: Python, data analyst, machine learning",
        )
        submitted = st.form_submit_button(
            "🔎 Find matching jobs",
            use_container_width=True,
        )

    if "job_search_term" not in st.session_state:
        st.session_state["job_search_term"] = suggested_search

    if submitted:
        if not search_term.strip():
            st.warning("Enter a job title or skill to search.")
            return
        st.session_state["job_search_term"] = search_term.strip()

    query = st.session_state["job_search_term"]

    try:
        with st.spinner("Searching live job listings..."):
            jobs = search_remote_jobs(query)
    except requests.RequestException:
        st.error(
            "We couldn't reach the job service right now. "
            "Please try again later."
        )
        return
    except (ValueError, TypeError):
        st.error("The job service returned an unexpected response.")
        return

    st.caption(f"Search: {query} · {len(jobs)} listings returned by the source")

    if not jobs:
        st.info(
            "No matching listings were returned. Try a broader term such as "
            "'Python', 'developer', 'data analyst', or 'marketing'."
        )
        return

    normalized_resume_skills = {
        skill.casefold() for skill in resume_skills
    }

    for job in jobs:
        title = job.get("title", "Untitled role")
        company = job.get("company_name", "Company not listed")
        location = job.get("candidate_required_location", "Remote")
        tags = job.get("tags") or []
        job_url = job.get("url", "")
        description = clean_description(job.get("description", ""))
        tags_text = ", ".join(str(tag) for tag in tags)

        job_terms = {
            str(tag).casefold() for tag in tags
        }
        match_count = len(normalized_resume_skills & job_terms)

        with st.container(border=True):
            st.subheader(title)
            st.write(f"🏢 **{company}**")
            st.caption(f"📍 {location or 'Remote'}")

            if tags:
                st.write("**Skills / tags:** " + tags_text)

            if resume_skills:
                st.write(f"**Matching resume tags:** {match_count}")

            if description:
                with st.expander("Read job description"):
                    st.write(description[:3500])

            if job_url.startswith("https://") or job_url.startswith("http://"):
                st.link_button("View job & apply ↗", job_url)
            else:
                st.caption("No valid application link was supplied by the source.")

    st.caption(
        "Listings are supplied by Remotive. Confirm eligibility, location, "
        "salary and application details on the original listing before applying."
    )
