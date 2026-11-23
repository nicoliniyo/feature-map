def segment(total):
    return 'gold' if total > 1000 else 'silver' if total > 200 else 'bronze'
