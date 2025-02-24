import nltk
import textstat
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from seo_publisher.models import Article

# Download NLTK data if not already installed
nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(text, num_keywords=5):
    """
    Extracts the most common keywords from the text.
    """
    words = word_tokenize(text.lower())  # Tokenize
    stop_words = set(stopwords.words('english'))  # Remove stopwords
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    freq_dist = nltk.FreqDist(words)  # Count word frequencies
    return [word for word, freq in freq_dist.most_common(num_keywords)]

def generate_meta_description(text):
    """
    Creates a meta description from the first 150 characters of the summary.
    """
    return text[:150] + "..." if len(text) > 150 else text

def check_readability(text):
    """
    Ensures the content is readable using Flesch Reading Ease Score.
    """
    score = textstat.flesch_reading_ease(text)
    return "Easy" if score > 60 else "Medium" if score > 40 else "Difficult"

def optimize_articles():
    """
    Optimize articles for SEO by extracting keywords, generating meta descriptions,
    and checking readability.
    """
    articles = Article.objects.filter(published=False)  # Get unpublished articles

    for article in articles:
        keywords = extract_keywords(article.content)  # Extract keywords
        meta_description = generate_meta_description(article.content)  # Create meta description
        readability = check_readability(article.content)  # Check readability

        # Store SEO metadata in the database
        article.metadata = f"Keywords: {', '.join(keywords)} | Meta Description: {meta_description} | Readability: {readability}"
        article.save()

    print("SEO optimization completed!")

    return articles

