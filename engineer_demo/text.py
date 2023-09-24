import openai
from engineer_demo.fetching_data import get_text_from_article
from newspaper.article import ArticleException


def summarize_text(text: str, model_type: str, max_number_words: int) -> str:
    """
    Summarize a longer text into a shorter
    message using OpenAI's chat model.

    Parameters:
    - text (str): The input text that is to be summarized.
    - model_type (str):  The type model what you want to use
    - max_number_words (int): The max number words of summarized text

    Returns:
    - str: The summarized text suitable for a max_number_words.
    """

    # Using the chat model for condensing the text
    response = openai.ChatCompletion.create(
        model=model_type,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarize"
                f" long texts into text with maximum {max_number_words} words.",
            },
            {
                "role": "user",
                "content": f"Summarize the following text into a text "
                f"with maximum {max_number_words} words, the text is {text}",
            },
        ],
    )
    summarized_text = response["choices"][0]["message"]["content"].strip()

    return summarized_text


def summary_article(article_url: str) -> str:
    """
    Summarizes the content of an article given its URL.

    Args:
    - article_url (str): The URL of the article to be summarized.

    Returns:
    - str: The summarized version of the article content.
    """
    try:
        text = get_text_from_article(article_url)
        summarized_text = summarize_text(text, "gpt-3.5-turbo", 150)
        return summarized_text
    except ArticleException as e:
        return f"Error summarizing the article: {str(e)}"


def analyze_sentiment(text: str, model_type: str = "gpt-3.5-turbo") -> str:
    """
    Analyze the sentiment of a given text using the OpenAI API.

    Args:
    - text (str): The text to be analyzed.
    - model_type (str): The model to use for the analysis.

    Returns:
    - str: The full response from the model.
    """
    try:
        # Use the language model to predict sentiment
        response = openai.ChatCompletion.create(
            model=model_type,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes"
                    " sentiment in the given text.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this text: '{text}'",
                },
            ],
        )

        # Return the full response from the model
        return response.choices[0].message["content"].strip()

    except Exception as e:
        print(f"Error: {e}")
        return "Error in processing the request."
