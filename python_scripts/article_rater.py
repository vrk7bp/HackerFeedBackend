def get_raw_article_rating(time, hit_bottom, num_taps, words):
    score = 0
    words_per_minute = 250
    if hit_bottom:
        score = score * 1.2  # arbitrary!!
    amount_read = words_per_minute * time / words
    score += amount_read
    score += num_taps
    return score