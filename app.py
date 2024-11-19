import streamlit as st
from dotenv import load_dotenv
from object_detection.video_stream import LiveIngredientDetector
from object_detection.model import load_model
from llm.recipe_suggestion import get_recipe_suggestions
from constants import GROQ_API_KEY, CFG_MODEL_PATH, PAGE_TITLE, WELCOME_MESSAGE

class RecipeSuggestionApp:
    def __init__(self):
        load_dotenv()
        st.set_page_config(page_title=PAGE_TITLE, layout="centered")
        self.model = None
        self.initialize_session_state()

    def initialize_session_state(self):
        if 'ingredients' not in st.session_state:
            st.session_state.ingredients = []

    def load_model(self):
        self.model = load_model(CFG_MODEL_PATH)

    def display_detected_ingredients(self, detected_ingredients):
        if detected_ingredients:
            st.session_state.ingredients.extend(detected_ingredients)
            st.write(f"Detected ingredients: {', '.join(st.session_state.ingredients)}")
        else:
            st.warning("No ingredients detected.")

    def get_manual_ingredients(self):
        user_input = st.text_input("Enter ingredients manually (comma-separated):")
        if user_input:
            additional_ingredients = [ingredient.strip() for ingredient in user_input.split(",")]
            st.session_state.ingredients.extend(additional_ingredients)

    def show_recipe_suggestions(self):
        st.write(f"Current ingredients in the system: {', '.join(st.session_state.ingredients)}")
        response = get_recipe_suggestions(st.session_state.ingredients, GROQ_API_KEY)
        st.write("Here are your recipe suggestions:")
        st.write(response)

    def run(self):
        st.title(PAGE_TITLE)
        st.write(WELCOME_MESSAGE)

        if self.model is None:
            self.load_model()

        input_option = st.radio("Choose your input method:", ["Detect Ingredients Live", "Manually Enter Ingredients"])

        if input_option == "Detect Ingredients Live":
            st.write("Starting live object detection...")
            detector = LiveIngredientDetector(self.model,confidence=0.5)
            detected_ingredients = detector.run_detection()
            self.display_detected_ingredients(detected_ingredients)
        else:
            self.get_manual_ingredients()

        if st.session_state.ingredients:
            self.show_recipe_suggestions()

if __name__ == "__main__":
    app = RecipeSuggestionApp()
    app.run()


