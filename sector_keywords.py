# Expand the keyword list for better matching with weights
sector_keywords = {
    "Healthcare": {
        "hospital": 1,
        "medical": 1,
        "health": 0.5,
        "clinic": 1,
        "care": 0.3,
        "biotechnology": 1,
        "pharmaceutical": 1,
        "therapeutics": 1,
        "medicine": 0.8,
        "treatment": 0.4,
        "nursing": 0.6,
        "surgery": 0.7,
        "dental": 0.5,
        "wellness": 0.4,
        "doctor": 0.7,
        "patient": 0.5,
        "telemedicine": 0.6,  # Added keyword with weight
        "diagnostics": 0.7,  # Added keyword with weight
        "healthcare": 1,  # Added keyword with weight
        "medical research": 0.8,  # Added keyword with weight
        "health services": 0.6,  # Added keyword with weight
        "healthcare management": 0.7,  # Added keyword with weight
        "healthcare technology": 0.8,  # Added keyword with weight
    },
    "Technology": {
        "software": 1,
        "technology": 1,
        "computer": 0.5,
        "internet": 0.5,
        "data": 0.3,
        "network": 0.3,
        "it": 0.2,
        "cloud": 0.7,
        "cybersecurity": 1,
        "ai": 1,
        "tech": 0.5,
        "hardware": 0.6,
        "programming": 0.7,
        "digital": 0.4,
        "analytics": 0.5,
        "iot": 0.6,
        "machine learning": 0.8,
        "blockchain": 0.7,
        "saas": 0.6,  # Added keyword with weight
        "mobile": 0.5,  # Added keyword with weight
        "artificial intelligence": 0.9,  # Added keyword with weight
        "data science": 0.8,  # Added keyword with weight
        "information technology": 0.7,  # Added keyword with weight
        "computer systems": 0.6,  # Added keyword with weight
    },
    "Manufacturing": {
        "manufacturing": 1,
        "industrial": 0.5,
        "factory": 1,
        "production": 0.5,
        "machinery": 0.7,
        "equipment": 0.3,
        "automotive": 0.5,
        "manufacture": 1,
        "assembly": 0.4,
        "fabrication": 0.6,
        "textiles": 0.4,
        "electronics": 0.5,
        "steel": 0.4,
        "automation": 0.6,
        "robotics": 0.7,
        "aerospace": 0.6,  # Added keyword with weight
        "chemicals": 0.5,  # Added keyword with weight
        "industrial engineering": 0.8,  # Added keyword with weight
        "mechanical engineering": 0.7,  # Added keyword with weight
        "supply chain management": 0.6,  # Added keyword with weight
        "quality control": 0.5,  # Added keyword with weight
    },
    "Finance": {
        "financial": 1,
        "banking": 1,
        "investment": 0.5,
        "insurance": 0.7,
        "fintech": 1,
        "market": 0.3,
        "trading": 0.5,
        "finance": 1,
        "bank": 0.5,
        "stocks": 0.4,
        "bonds": 0.4,
        "loans": 0.3,
        "mortgages": 0.4,
        "funds": 0.5,
        "crypto": 0.6,
        "equity": 0.5,
        "accounting": 0.6,  # Added keyword with weight
        "wealth management": 0.7,  # Added keyword with weight
        "financial services": 0.9,  # Added keyword with weight
        "investment banking": 0.8,  # Added keyword with weight
        "asset management": 0.7,  # Added keyword with weight
        "financial planning": 0.6,  # Added keyword with weight
    },
    "Consumer Services": {
        "retail": 1,
        "consumer": 0.5,
        "service": 0.3,
        "restaurant": 1,
        "hospitality": 0.7,
        "entertainment": 0.5,
        "shopping": 0.5,
        "store": 0.3,
        "customer": 0.4,
        "leisure": 0.5,
        "tourism": 0.6,
        "accommodation": 0.4,
        "beauty": 0.4,
        "travel": 0.6,
        "luxury": 0.5,
        "ecommerce": 0.7,  # Added keyword with weight
        "gaming": 0.6,  # Added keyword with weight
        "hospitality management": 0.8,  # Added keyword with weight
        "customer service": 0.7,  # Added keyword with weight
        "retail management": 0.6,  # Added keyword with weight
        "food service": 0.5,  # Added keyword with weight
    },
    "Energy": {
        "energy": 1,
        "oil": 0.7,
        "gas": 0.7,
        "petroleum": 0.5,
        "solar": 1,
        "renewable": 1,
        "power": 0.3,
        "electricity": 0.5,
        "wind": 0.8,
        "hydro": 0.6,
        "nuclear": 0.7,
        "bioenergy": 0.5,
        "geothermal": 0.4,
        "battery": 0.6,
        "conservation": 0.5,
        "utilities": 0.6,  # Added keyword with weight
        "carbon capture": 0.7,  # Added keyword with weight
        "energy storage": 0.8,  # Added keyword with weight
        "energy efficiency": 0.7,  # Added keyword with weight
        "renewable energy": 0.9,  # Added keyword with weight
    },
    "Real Estate": {
        "property": 1,
        "real estate": 1,
        "housing": 0.5,
        "commercial": 0.7,
        "residential": 0.7,
        "land": 0.4,
        "development": 0.5,
        "construction": 0.6,
        "buildings": 0.4,
        "leasing": 0.5,
        "rental": 0.4,
        "mortgage": 0.6,  # Added keyword with weight
        "reits": 0.7,  # Added keyword with weight
        "real estate development": 0.9,  # Added keyword with weight
        "property management": 0.8,  # Added keyword with weight
        "commercial real estate": 0.7,  # Added keyword with weight
        "residential real estate": 0.6,  # Added keyword with weight
    },
    "Education": {
        "school": 1,
        "education": 1,
        "university": 0.7,
        "college": 0.7,
        "learning": 0.5,
        "academic": 0.4,
        "scholarship": 0.3,
        "teaching": 0.5,
        "courses": 0.4,
        "research": 0.6,
        "e-learning": 0.5,
        "training": 0.6,  # Added keyword with weight
        "tutoring": 0.5,  # Added keyword with weight
        "higher education": 0.8,  # Added keyword with weight
        "online education": 0.7,  # Added keyword with weight
        "educational technology": 0.6,  # Added keyword with weight
        "curriculum development": 0.5,  # Added keyword with weight
    },
    "Agriculture": {
        "farming": 1,
        "agriculture": 1,
        "crops": 0.5,
        "livestock": 0.7,
        "horticulture": 0.5,
        "organic": 0.4,
        "fertilizers": 0.3,
        "irrigation": 0.4,
        "aquaculture": 0.6,
        "agritech": 0.5,
        "forestry": 0.6,  # Added keyword with weight
        "agribusiness": 0.7,  # Added keyword with weight
        "sustainable agriculture": 0.8,  # Added keyword with weight
        "agricultural engineering": 0.7,  # Added keyword with weight
        "crop management": 0.6,  # Added keyword with weight
        "animal husbandry": 0.5,  # Added keyword with weight
    },
    "Transportation": {
        "transport": 1,
        "logistics": 1,
        "shipping": 0.7,
        "freight": 0.7,
        "rail": 0.5,
        "airlines": 0.6,
        "trucking": 0.5,
        "transit": 0.4,
        "maritime": 0.6,
        "delivery": 0.5,
        "ride-sharing": 0.6,  # Added keyword with weight
        "autonomous vehicles": 0.7,  # Added keyword with weight
        "transportation management": 0.8,  # Added keyword with weight
        "supply chain logistics": 0.7,  # Added keyword with weight
        "freight forwarding": 0.6,  # Added keyword with weight
        "public transportation": 0.5,  # Added keyword with weight
    },
    "Media and Entertainment": {  # Added new sector
        "media": 1,
        "entertainment": 1,
        "film": 0.7,
        "television": 0.7,
        "music": 0.6,
        "publishing": 0.5,
        "news": 0.4,
        "broadcasting": 0.6,
        "streaming": 0.7,
        "content creation": 0.5,
        "digital media": 0.8,  # Added keyword with weight
        "entertainment technology": 0.7,  # Added keyword with weight
        "media production": 0.6,  # Added keyword with weight
        "publishing industry": 0.5,  # Added keyword with weight
        "news media": 0.4,  # Added keyword with weight
    },
    "Telecommunications": {  # Added new sector
        "telecommunications": 1,
        "telecom": 1,
        "wireless": 0.7,
        "broadband": 0.6,
        "internet service": 0.5,
        "mobile network": 0.6,
        "fiber optics": 0.5,
        "satellite": 0.4,
        "voip": 0.4,
        "5g": 0.7,
        "network infrastructure": 0.8,  # Added keyword with weight
        "telecom services": 0.7,  # Added keyword with weight
        "wireless communication": 0.6,  # Added keyword with weight
        "internet of things": 0.5,  # Added keyword with weight
        "telecom equipment": 0.4,  # Added keyword with weight
    },
    "Professional Services": {  # Added new sector
        "consulting": 1,
        "legal": 0.8,
        "accounting": 0.7,
        "marketing": 0.6,
        "advertising": 0.6,
        "hr": 0.5,
        "recruitment": 0.5,
        "public relations": 0.4,
        "management": 0.3,
        "outsourcing": 0.4,
        "professional services": 0.9,  # Added keyword with weight
        "financial services": 0.8,  # Added keyword with weight
        "human resources": 0.7,  # Added keyword with weight
        "marketing services": 0.6,  # Added keyword with weight
        "advertising agency": 0.5,  # Added keyword with weight
    },
    "Construction": {  # Added new sector
        "construction": 1,
        "building": 0.7,
        "contractor": 0.6,
        "engineering": 0.5,
        "architecture": 0.5,
        "design": 0.4,
        "renovation": 0.3,
        "infrastructure": 0.4,
        "civil engineering": 0.6,
        "residential construction": 0.5,
        "commercial construction": 0.6,  # Added keyword with weight
        "construction management": 0.7,  # Added keyword with weight
        "building materials": 0.8,  # Added keyword with weight
        "construction technology": 0.7,  # Added keyword with weight
        "construction services": 0.6,  # Added keyword with weight
    },
    "Automotive": {  # Added new sector
        "automotive": 1,
        "cars": 0.7,
        "vehicles": 0.6,
        "auto": 0.5,
        "electric vehicles": 0.6,
        "autonomous vehicles": 0.7,
        "car rental": 0.5,
        "car sharing": 0.4,
        "automotive technology": 0.8,
        "automotive industry": 0.7,
        "automotive engineering": 0.6,
        "vehicle manufacturing": 0.5,
        "automotive design": 0.4,
        "automotive parts": 0.6,  # Added keyword with weight
        "automotive services": 0.7,  # Added keyword with weight
        "automotive software": 0.8,  # Added keyword with weight
    },
    "Retail": {  # Added new sector
        "retail": 1,
        "shopping": 0.7,
        "store": 0.6,
        "fashion": 0.5,
        "apparel": 0.5,
        "beauty": 0.4,
        "cosmetics": 0.3,
        "jewelry": 0.4,
        "luxury": 0.6,
        "retail technology": 0.5,
        "retail industry": 0.6,
        "retail management": 0.7,
        "retail services": 0.8,
        "retail marketing": 0.7,
        "retail sales": 0.6,
        "retail analytics": 0.5,  # Added keyword with weight
        "retail logistics": 0.6,  # Added keyword with weight
        "retail operations": 0.7,  # Added keyword with weight
    },
    "Security": {  # Added new sector
        "security": 1,
        "cybersecurity": 0.7,
        "cyber": 0.6,
        "hacking": 0.5,
        "crime": 0.4,
        "law enforcement": 0.3,
        "intelligence": 0.4,
        "defense": 0.5,
        "military": 0.6,
        "security industry": 0.7,
        "security services": 0.8,
        "security management": 0.7,
        "security technology": 0.6,
        "security policy": 0.5,
    },
    "Legal": {  # Added new sector
        "legal": 1,
        "law": 0.7,
        "lawyer": 0.6,
        "attorney": 0.5,
        "court": 0.4,
        "justice": 0.3,
        "legal services": 0.5,
        "legal technology": 0.6,
        "legal industry": 0.7,
        "legal practice": 0.8,
        "legal advice": 0.7,
        "legal counsel": 0.6,
        "legal representation": 0.5,
    },
    "Insurance": {  # Added new sector
        "insurance": 1,
        "insurer": 0.7,
        "coverage": 0.6,
        "policy": 0.5,
        "claims": 0.4,
        "premium": 0.3,
        "insurance industry": 0.5,
        "insurance services": 0.6,
        "insurance technology": 0.7,
        "insurance policy": 0.8,
        "insurance coverage": 0.7,
        "insurance claims": 0.6,
        "insurance premium": 0.5,
    },
    "Defense": {  # Added new sector
        "defense": 1,
        "military": 0.7,
        "security": 0.6,
        "defense industry": 0.5,
        "defense services": 0.6,
        "defense technology": 0.7,
        "defense policy": 0.8,
        "defense coverage": 0.7,
        "defense claims": 0.6,
        "defense premium": 0.5,
    },
    "Government": {  # Added new sector
        "government": 1,
        "public": 0.7,
        "administration": 0.6,
        "policy": 0.5,
        "services": 0.4,
        "government industry": 0.5,
        "government services": 0.6,
        "government technology": 0.7,
        "government policy": 0.8,
        "government administration": 0.7,
        "government services": 0.6,
        "government operations": 0.5,
    },
    "Nonprofit": {  # Added new sector
        "nonprofit": 1,
        "charity": 0.7,
        "foundation": 0.6,
        "organization": 0.5,
        "nonprofit industry": 0.6,
        "nonprofit services": 0.7,
        "nonprofit technology": 0.8,
        "nonprofit policy": 0.7,
        "nonprofit administration": 0.6,
        "nonprofit operations": 0.5,
    },
    "Education": {  # Added new sector
        "education": 1,
        "school": 0.7,
        "college": 0.6,
        "university": 0.5,
        "education industry": 0.6,
        "education services": 0.7,
        "education technology": 0.8,
        "education policy": 0.7,
        "education administration": 0.6,
        "education operations": 0.5,
    },
    "Consulting": {  # Added new sector
        "consulting": 1,
        "consultant": 0.7,
        "consulting services": 0.6,
        "consulting industry": 0.5,
        "consulting technology": 0.4,
        "consulting policy": 0.3,
        "consulting administration": 0.4,
        "consulting operations": 0.5,
    },
    "Marketing": {  # Added new sector
        "marketing": 1,
        "advertising": 0.7,
        "branding": 0.6,
        "digital marketing": 0.5,
        "social media": 0.4,
        "marketing industry": 0.5,
        "marketing services": 0.6,
        "marketing technology": 0.7,
        "marketing policy": 0.8,
        "marketing administration": 0.7,
        "marketing operations": 0.6,
    },
    "Advertising": {  # Added new sector
        "advertising": 1,
        "advertiser": 0.7,
        "advertising services": 0.6,
        "advertising industry": 0.5,
        "advertising technology": 0.4,
        "advertising policy": 0.3,
        "advertising administration": 0.4,
        "advertising operations": 0.5,
    },
    "HR": {  # Added new sector
        "hr": 1,
        "human resources": 0.7,
        "hr services": 0.6,
        "hr industry": 0.5,
        "hr technology": 0.4,
        "hr policy": 0.3,
        "hr administration": 0.4,
        "hr operations": 0.5,
    },
    "Recruitment": {  # Added new sector
        "recruitment": 1,
        "recruiter": 0.7,
        "recruitment services": 0.6,
        "recruitment industry": 0.5,
        "recruitment technology": 0.4,
        "recruitment policy": 0.3,
        "recruitment administration": 0.4,
        "recruitment operations": 0.5,
    },
    "Unmatched": {},  # Dynamic catch-all category for unmatched keywords
}

