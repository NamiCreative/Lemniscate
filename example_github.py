from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access your GitHub token
github_token = os.getenv('GITHUB_TOKEN')

# Now you can use github_token in your API calls or git operations