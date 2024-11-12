import streamlit as st
from datetime import datetime
import os
import database.handlers as handlers

st.set_page_config(page_title="Трекер достижений")


handlers.init_database()

# Заголовок
st.title("Трекер достижений")

# Форма ввода
with st.form("achievement_form"):
    description = st.text_input("Ваш вклад в ваши цели")
    points = st.slider("Оценка вклада", min_value=5, max_value=50, value=5)
    submitted = st.form_submit_button("Добавить достижение")

    if submitted and description:
        handlers.add_achievement(description, points)
        st.balloons()  # Анимация
        st.success("Достижение добавлено!")

# Кнопка удаления всех достижений
if st.button("Удалить все достижения"):
    handlers.delete_all_achievements()
    st.warning("Все достижения удалены!")

# Отображение достижений
with st.expander("Показать все достижения", expanded=True):
    achievements = handlers.get_achievements()
    for achievement in achievements:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{achievement[1]}**")
            st.caption(f"Добавлено: {achievement[3]}")
        with col2:
            # Создаем квадрат, размер которого пропорционален весу достижения
            size = achievement[2] * 2
            st.markdown(f"""
                <div style="
                    width: {size}px;
                    height: {size}px;
                    background-color: #1f77b4;
                    margin: 5px;
                "></div>
            """, unsafe_allow_html=True)