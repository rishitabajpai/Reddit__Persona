import praw
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Reddit setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="RedditPersonaScript"
)

def get_user_content(username, limit=20):
    user = reddit.redditor(username)
    posts = []
    comments = []

    for post in user.submissions.new(limit=limit):
        posts.append(f"Title: {post.title}\nText: {post.selftext}\nLink: https://reddit.com{post.permalink}\n")

    for comment in user.comments.new(limit=limit):
        comments.append(f"Comment: {comment.body}\nLink: https://reddit.com{comment.permalink}\n")

    return posts, comments

def main():
    url = input("Enter Reddit profile URL: ")
    username = url.strip('/').split('/')[-1]

    print(f"Fetching posts and comments for {username}...")
    posts, comments = get_user_content(username)

    combined = "\n\n--- POSTS ---\n\n" + "\n".join(posts) + "\n\n--- COMMENTS ---\n\n" + "\n".join(comments)

    filename = f"{username}_rawdata.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(combined)

    print(f"\n✅ Reddit data saved to: {filename}")
    print("📝 Now copy the content into ChatGPT and ask it to generate a user persona!")

if __name__ == "__main__":
    main()