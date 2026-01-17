import feedparser
import os
import re

# Constants
FEED_URL = "https://devbattery.com/feed.xml"
README_PATH = "README.md"
MAX_POSTS = 6
COLUMNS = 2

def generate_table(posts):
    html = "<table>\n"
    for i in range(0, len(posts), COLUMNS):
        html += "  <tr>\n"
        row_posts = posts[i:i + COLUMNS]
        for post in row_posts:
            # Safely get title, link, date, and image
            title = post.get('title', 'No Title')
            link = post.get('link', '#')
            # Format date: 'Fri, 17 Jan 2026 00:00:00 +0900' -> '2026-01-17'
            # Assuming standard RSS date format, or just using raw if parsing fails
            try:
                date_struct = post.published_parsed
                date_str = f"{date_struct.tm_year}-{date_struct.tm_mon:02d}-{date_struct.tm_mday:02d}"
            except:
                date_str = post.get('published', '')[:10]
            
            # Find image: try 'teaser_image', 'media_content', or 'enclosure'
            image_url = ""
            if 'teaser_image' in post:
                image_url = post['teaser_image']
            elif 'media_content' in post:
                image_url = post['media_content'][0]['url']
            elif 'media_content_url' in post: # sometimes parsed flattened
                 image_url = post['media_content_url']
            
            # Formatting the cell
            html += "    <td align=\"center\" width=\"50%\">\n"
            html += f"      <a href=\"{link}\"><img src=\"{image_url}\" width=\"100%\" style=\"border-radius: 10px;\" alt=\"{title}\"></a><br/>\n"
            html += f"      <a href=\"{link}\"><b>{title}</b></a><br/>\n"
            html += f"      {date_str}\n"
            html += "    </td>\n"
        
        # If the row is not full (e.g. 1 item in a 2-column row), add empty cells
        if len(row_posts) < COLUMNS:
             for _ in range(COLUMNS - len(row_posts)):
                 html += "    <td></td>\n"
        
        html += "  </tr>\n"
    html += "</table>\n"
    return html

def update_readme():
    # Parse Feed
    feed = feedparser.parse(FEED_URL)
    posts = feed.entries[:MAX_POSTS]
    
    # Generate HTML
    new_content = generate_table(posts)
    
    # Read README
    with open(README_PATH, 'r') as f:
        content = f.read()
    
    # Replace Content
    pattern = r"<!-- BLOG-POST-LIST:START -->.*<!-- BLOG-POST-LIST:END -->"
    replacement = f"<!-- BLOG-POST-LIST:START -->\n{new_content}\n<!-- BLOG-POST-LIST:END -->"
    
    new_readme_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write README
    with open(README_PATH, 'w') as f:
        f.write(new_readme_content)

if __name__ == "__main__":
    update_readme()
