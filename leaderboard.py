import json
import os

SCORES_FILE = os.path.join(os.path.dirname(__file__), 'scores.json')


def load_scores():
    """Load scores from file."""
    if not os.path.exists(SCORES_FILE):
        return []

    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_score(name, score):
    """Save a new score to the leaderboard."""
    scores = load_scores()
    scores.append({'name': name, 'score': score})

    # Sort by score descending and keep top 10
    scores.sort(key=lambda x: x['score'], reverse=True)
    scores = scores[:10]

    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2)

    return scores


def get_top_scores(limit=10):
    """Get top scores from the leaderboard."""
    scores = load_scores()
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:limit]


def is_high_score(score):
    """Check if score qualifies for leaderboard."""
    scores = load_scores()
    if len(scores) < 10:
        return True
    return score > min(s['score'] for s in scores)
