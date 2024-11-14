import streamlit as st
from config import load_config
from object_detection.video_stream import live_input
from object_detection.model import load_model
from llm.recipe_suggestion import get_recipe_suggestions

def main():
    """
    Main entry point for the application. Handles both object detection and recipe suggestion.
    """
   
    groq_api_key = load_config()

    st.set_page_config(page_title="Conversational Recipe Suggestion Bot", layout="centered")
    st.title("Conversational Recipe Suggestion Bot")
    st.write("Hello! I'm your friendly cooking assistant. Let's see what delicious dishes we can make with your ingredients!")

    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []

    cfg_model_path = 'models/updated_weights.pt'
    model = load_model(cfg_model_path)

    input_option = st.radio("Choose your input method:", ["Detect Ingredients Live", "Manually Enter Ingredients"])

    if input_option == "Detect Ingredients Live":
        st.write("Starting live object detection...")
        detected_ingredients = live_input(model)
        
        if detected_ingredients:
            st.session_state.ingredients.extend(detected_ingredients)
            st.write(f"Detected ingredients: {', '.join(st.session_state.ingredients)}")
    
    else:
        user_input = st.text_input("Enter ingredients manually (comma-separated):")
        
        if user_input:
            additional_ingredients = [ingredient.strip() for ingredient in user_input.split(",")]
            st.session_state.ingredients.extend(additional_ingredients)

    # if ingredients are detected or entered display them and fetch recipe suggestions
    if st.session_state.ingredients:
        st.write(f"Current ingredients in the system: {', '.join(st.session_state.ingredients)}")

        response = get_recipe_suggestions(st.session_state.ingredients, groq_api_key)
        st.write("Here are your recipe suggestions:")
        st.write(response)

if __name__ == "__main__":
    main()
