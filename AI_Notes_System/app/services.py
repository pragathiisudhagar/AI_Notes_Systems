import os
import google.generativeai as genai
from flask import current_app

class AIService:
    @staticmethod
    def _get_model():
        api_key = current_app.config['GEMINI_API_KEY']
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')

    @classmethod
    def summarize_note(cls, content):
        model = cls._get_model()
        if not model:
            return "Gemini API key not configured."
        try:
            prompt = f"Please provide a concise summary of the following note content:\n\n{content}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"

    @classmethod
    def generate_key_points(cls, content):
        model = cls._get_model()
        if not model:
            return "Gemini API key not configured."
        try:
            prompt = f"Extract the key bullet points from the following note content:\n\n{content}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"

    @classmethod
    def generate_quiz(cls, content):
        model = cls._get_model()
        if not model:
            return "Gemini API key not configured."
        try:
            prompt = f"Generate 3-5 quiz questions with answers based on the following note content. Format as Question and Answer pairs:\n\n{content}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"
