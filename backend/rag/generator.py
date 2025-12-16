import cohere
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Generator:
    """
    Answer generator using Cohere API
    """

    def __init__(self, model_name: str = "command-r-plus"):
        self.model_name = model_name
        self.api_key = os.getenv("COHERE_API_KEY")

        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(self.api_key)

    def generate_answer(self, question: str, context_chunks: List[Dict]) -> str:
        """
        Generate an answer based on the question and retrieved context chunks
        """
        if not context_chunks:
            return "This is not covered in the AI_BOOK."

        # Build context from retrieved chunks
        context_text = "\n\n".join([
            f"Document {i+1}: {chunk['title']}\nContent: {chunk['content'][:1000]}"  # Limit content to 1000 chars
            for i, chunk in enumerate(context_chunks)
        ])

        # Create the prompt for the language model
        prompt = f"""
        You are an AI assistant for the AI_BOOK, a textbook on Physical AI & Humanoid Robotics.
        Answer the user's question based ONLY on the provided context from the book.
        If the answer is not available in the provided context, respond with exactly: "This is not covered in the AI_BOOK."

        Context:
        {context_text}

        Question: {question}

        Answer:
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                max_tokens=500,
                temperature=0.3,
                stop_sequences=["\n\n"]
            )

            answer = response.generations[0].text.strip()

            # Check if the answer is empty or just a repetition of the context
            if not answer or len(answer.strip()) < 10:
                return "This is not covered in the AI_BOOK."

            return answer

        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return "This is not covered in the AI_BOOK."

    def generate_answer_with_selected_text(self, selected_text: str, question: str, context_chunks: List[Dict]) -> str:
        """
        Generate an answer based on the question, selected text, and retrieved context chunks
        """
        if not context_chunks:
            return "This is not covered in the AI_BOOK."

        # Build context from retrieved chunks
        context_text = "\n\n".join([
            f"Document {i+1}: {chunk['title']}\nContent: {chunk['content'][:1000]}"  # Limit content to 1000 chars
            for i, chunk in enumerate(context_chunks)
        ])

        # Create the prompt with selected text context
        prompt = f"""
        You are an AI assistant for the AI_BOOK, a textbook on Physical AI & Humanoid Robotics.
        The user has selected the following text: "{selected_text}"
        They have a question about it: "{question}"

        Answer the user's question based ONLY on the provided context from the book.
        If the answer is not available in the provided context, respond with exactly: "This is not covered in the AI_BOOK."

        Context:
        {context_text}

        Question: {question}

        Answer:
        """

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                max_tokens=500,
                temperature=0.3,
                stop_sequences=["\n\n"]
            )

            answer = response.generations[0].text.strip()

            # Check if the answer is empty or just a repetition of the context
            if not answer or len(answer.strip()) < 10:
                return "This is not covered in the AI_BOOK."

            return answer

        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return "This is not covered in the AI_BOOK."

# For testing
if __name__ == "__main__":
    try:
        generator = Generator()
        sample_question = "What is artificial intelligence?"
        sample_chunks = [
            {
                "title": "Introduction to AI",
                "content": "Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals."
            }
        ]

        answer = generator.generate_answer(sample_question, sample_chunks)
        print(f"Answer: {answer}")

    except ValueError as e:
        print(f"Generator initialization failed: {e}")
        print("Please set COHERE_API_KEY environment variable to test generation")