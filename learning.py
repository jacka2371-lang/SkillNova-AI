
from pathlib import Path
import sqlite3
from datetime import date

import streamlit as st


DB_PATH = Path(__file__).resolve().parent / "resume_ai.db"

LESSON_CODE = "python_variables_01"

QUESTIONS = [
    {
        "question": "Which symbol is used to assign a value to a variable in Python?",
        "options": ["==", "=", ":"],
        "answer": "=",
        "explanation": "The = symbol assigns a value. == checks whether two values are equal.",
    },
    {
        "question": "What is the data type of the value 25?",
        "options": ["str", "int", "bool"],
        "answer": "int",
        "explanation": "25 is an integer, so its type is int.",
    },
    {
        "question": 'What is the output of name = "Eliora"; print(name)?',
        "options": ["name", "Eliora", "Error"],
        "answer": "Eliora",
        "explanation": "print(name) displays the string stored in the variable name.",
    },
]


def connect_db():
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_learning_tables():
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS learning_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                module_code TEXT NOT NULL,
                attempt_date TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                points INTEGER NOT NULL,
                stars INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, module_code, attempt_date)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS learning_badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                badge_code TEXT NOT NULL,
                badge_name TEXT NOT NULL,
                earned_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, badge_code)
            )
        """)


def get_learning_stats(user_id):
    with connect_db() as connection:
        attempts = connection.execute("""
            SELECT COUNT(*) AS quizzes,
                   COALESCE(SUM(points), 0) AS points,
                   COALESCE(SUM(stars), 0) AS stars
            FROM learning_attempts
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        badges = connection.execute("""
            SELECT badge_name, earned_at
            FROM learning_badges
            WHERE user_id = ?
            ORDER BY earned_at DESC
        """, (user_id,)).fetchall()

    return dict(attempts), [dict(row) for row in badges]


def already_completed_today(user_id):
    with connect_db() as connection:
        result = connection.execute("""
            SELECT score, total, points, stars
            FROM learning_attempts
            WHERE user_id = ? AND module_code = ? AND attempt_date = ?
        """, (user_id, LESSON_CODE, date.today().isoformat())).fetchone()

    return dict(result) if result else None


def save_result(user_id, score, total):
    points = score * 10

    if score == total:
        stars = 3
    elif score / total >= 0.7:
        stars = 2
    elif score / total >= 0.5:
        stars = 1
    else:
        stars = 0

    with connect_db() as connection:
        cursor = connection.execute("""
            INSERT OR IGNORE INTO learning_attempts
            (user_id, module_code, attempt_date, score, total, points, stars)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            LESSON_CODE,
            date.today().isoformat(),
            score,
            total,
            points,
            stars,
        ))

        # Award points and badges only if today's attempt was newly saved.
        if cursor.rowcount == 1:
            connection.execute("""
                INSERT OR IGNORE INTO learning_badges
                (user_id, badge_code, badge_name)
                VALUES (?, ?, ?)
            """, (user_id, "first_quiz", "First Quiz"))

            if score == total:
                connection.execute("""
                    INSERT OR IGNORE INTO learning_badges
                    (user_id, badge_code, badge_name)
                    VALUES (?, ?, ?)
                """, (user_id, "perfect_score", "Perfect Score"))

    return points, stars


def show_learning_center(user_id):
    init_learning_tables()

    if not user_id:
        st.warning("Please log in to save your learning progress.")
        return

    st.title("🎓 Learning Center")
    st.caption("Learn a little every day. Track your progress as you grow.")

    stats, badges = get_learning_stats(user_id)

    first, second, third = st.columns(3)
    first.metric("⭐ Total Points", stats["points"])
    second.metric("🌟 Stars Earned", stats["stars"])
    third.metric("🏆 Badges", len(badges))

    st.progress(min(stats["quizzes"] / 10, 1.0))
    st.caption(f"Learning journey: {stats['quizzes']} quiz attempts saved")

    st.divider()
    st.subheader("📘 Today's lesson: Python Variables")

    st.markdown("""
    <div class="feature-card">
      <h3>What is a variable?</h3>
      A variable stores a value that you can use later in your program.

      <br><br>

      <b>Example</b>
      <br>
      <code>student_name = "Eliora"</code>
      <br>
      <code>age = 20</code>
      <br><br>

      <b>Remember</b>
      <br>
      <code>str</code> stores text, <code>int</code> stores whole numbers,
      and <code>bool</code> stores True or False.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.subheader("🧠 Quick quiz")

    previous = already_completed_today(user_id)

    if previous:
        st.success(
            f"You completed today's quiz! Score: {previous['score']}/"
            f"{previous['total']} · {previous['points']} points · "
            f"{'⭐' * previous['stars']}"
        )
    else:
        with st.form("daily_python_quiz"):
            answers = []

            for index, question in enumerate(QUESTIONS):
                st.markdown(f"**{index + 1}. {question['question']}**")
                selected = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"learning_q_{index}",
                    index=None,
                )
                answers.append(selected)

            submitted = st.form_submit_button(
                "Submit answers",
                use_container_width=True,
            )

        if submitted:
            if any(answer is None for answer in answers):
                st.warning("Answer all three questions before submitting.")
            else:
                score = sum(
                    answers[index] == question["answer"]
                    for index, question in enumerate(QUESTIONS)
                )

                points, stars = save_result(user_id, score, len(QUESTIONS))

                st.success(f"You scored {score}/{len(QUESTIONS)}!")
                st.write(f"Points earned: **{points}**")
                st.write(f"Stars earned: **{'⭐' * stars or 'No stars this time — keep learning!'}**")

                with st.expander("See the correct answers and explanations"):
                    for question in QUESTIONS:
                        st.markdown(f"**{question['question']}**")
                        st.write(f"Answer: {question['answer']}")
                        st.caption(question["explanation"])

                st.rerun()

    st.divider()
    st.subheader("🏆 Your achievements")

    if badges:
        columns = st.columns(min(3, len(badges)))
        for index, badge in enumerate(badges):
            with columns[index % len(columns)]:
                st.markdown(
                    f"""
                    <div class="badge-card">
                        <div style="font-size:28px">🏅</div>
                        <b>{badge['badge_name']}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Complete your first quiz to unlock your first badge!")
