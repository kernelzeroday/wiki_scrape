import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
import logging
from sector_keywords import sector_keywords
import asyncio

# NLP setup
nltk.download('punkt')

async def deduce_sector(text, precomputed_scores=None):
    words = word_tokenize(text.lower())
    sector_scores = {sector: 0 for sector in sector_keywords}
    unmatched_words = defaultdict(int)
    for word in words:
        matched = False
        for sector, keywords in sector_keywords.items():
            if word in keywords:
                sector_scores[sector] += keywords[word]
                logging.info(f"Word '{word}' contributes {keywords[word]} to sector {sector}")
                matched = True
        if not matched:
            unmatched_words[word] += 1

    # Dynamic sector creation based on unmatched words
    dynamic_sectors = defaultdict(float)
    for word, count in unmatched_words.items():
        dynamic_sector = 'Dynamic-' + word
        dynamic_sectors[dynamic_sector] += count * 0.1
        logging.info(f"Unmatched word '{word}' contributes {count * 0.1} to dynamic sector '{dynamic_sector}'")

    # Validate dynamic sectors
    validated_dynamic_sectors = {}
    for sector, score in dynamic_sectors.items():
        if score >= 5:  # Minimum threshold for creating a new sector
            validated_dynamic_sectors[sector] = score
            logging.info(f"Validated dynamic sector '{sector}' with score {score}")

    sector_scores.update(validated_dynamic_sectors)
    max_score = max(sector_scores.values())
    matched_sectors = [sector for sector, score in sector_scores.items() if score == max_score and score > 0]
    logging.info(f"Sectors matched based on keywords: {matched_sectors}")
    return matched_sectors if matched_sectors else ["Unmatched"]

if __name__ == "__main__":
    # Example usage
    text = "This is an example text related to the Technology sector."
    asyncio.run(deduce_sector(text))
