from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import instaloader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.json.get('username')

        # Initialize Instaloader
        L = instaloader.Instaloader()

        # Fetch captions from Instagram posts
        captions = []
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            for post in profile.get_posts():
                captions.append(post.caption)
        except instaloader.exceptions.ProfileNotExistsException:
            return jsonify({'error': 'Invalid username'})

        # Perform sentiment analysis using TextBlob
        positive_count = 0
        negative_count = 0

        for caption in captions:
            blob = TextBlob(caption)
            polarity = blob.sentiment.polarity
            if polarity > 0:
                positive_count += 1
            elif polarity < 0:
                negative_count += 1

        total_captions = len(captions)
        if total_captions == 0:
            return jsonify({'error': 'No captions found'})

        # Calculate probability
        positive_percent = (positive_count / total_captions) * 100
        negative_percent = (negative_count / total_captions) * 100
        probability = max(positive_percent, negative_percent)

        # Determine result and response message
        if probability >= 50:
            result = f"Real ({probability:.2f}% chance)"
        else:
            result = f"Fake ({100 - probability:.2f}% chance)"

        response_data = {'result': result}
        return jsonify(response_data)
    else:
        return render_template('index.html')

app.run(port="5000", debug=True)
