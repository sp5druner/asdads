def format_score(score):
    if score >= 1_000_000:
        return f"{score / 1_000_000:.1f}M"
    elif score >= 1_000:
        return f"{score / 1_000:.1f}k"
    return str(score)

def parse_score(score):
    if isinstance(score, (int, float)):
        return score
    score = score.upper()
    if 'M' in score:
        return float(score.replace('M', '')) * 1_000_000
    if 'K' in score:
        return float(score.replace('K', '')) * 1_000
    return float(score)
