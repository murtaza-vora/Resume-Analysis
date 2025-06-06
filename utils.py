from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    return dictionary.get(key, None)




industry_keywords = {
    "IT Industry": ["it", "information technology", "software", "developer", "programmer", "engineer", "web", "data",
                    "network", "cybersecurity", "artificial intelligence", "machine learning"],
    "Finance Industry": ["finance", "banking", "accounting", "financial", "analyst", "investment", "insurance", "tax",
                         "audit", "trader"],
    "Healthcare Industry": ["healthcare", "medical", "doctor", "nurse", "pharmaceutical", "hospital", "clinical",
                            "health", "biomedical", "research"],
    "Education Industry": ["education", "teacher", "instructor", "professor", "tutor", "academy", "school", "training",
                           "e-learning", "curriculum"],
    "Marketing Industry": ["marketing", "digital marketing", "advertising", "branding", "market research",
                           "public relations", "social media", "seo", "campaign"],
    "Sales Industry": ["sales", "business development", "account manager", "customer", "retail", "wholesale",
                       "distribution", "merchandising", "salesforce"],
    "Manufacturing Industry": ["manufacturing", "production", "operations", "supply chain", "logistics",
                               "quality control", "factory", "assembly", "engineering"],
    "Consulting Industry": ["consulting", "management consulting", "strategy", "advisory", "business consulting",
                            "consultant", "solution"],
    "Hospitality Industry": ["hospitality", "hotel", "restaurant", "travel", "tourism", "event", "catering",
                             "guest services", "resort", "accommodation"],
    "Media and Entertainment Industry": ["media", "entertainment", "journalism", "broadcast", "television", "film",
                                         "music", "production", "content", "editing"],
    "Real Estate Industry": ["real estate", "property", "realtor", "developer", "investment", "commercial",
                             "residential", "brokerage", "appraisal"],
    "Automotive Industry": ["automotive", "vehicle", "automobile", "car", "mechanic", "manufacturing", "assembly",
                            "engineering", "parts"],
    "Fashion Industry": ["fashion", "apparel", "clothing", "retail", "design", "stylist", "textile", "brand",
                         "merchandising"],
    "Energy Industry": ["energy", "renewable", "solar", "wind", "oil", "gas", "power", "utilities", "sustainability",
                        "electricity"],
    "Construction Industry": ["construction", "builder", "contractor", "architect", "engineering", "project management",
                              "building"],
    "Aerospace Industry": ["aerospace", "aviation", "aircraft", "aeronautical", "engineering", "defense", "space",
                           "pilot"],
    "Pharmaceutical Industry": ["pharmaceutical", "medicine", "drug", "pharmacy", "clinical trials", "research",
                                "biotechnology"],
    "Telecommunications Industry": ["telecommunications", "telecom", "network", "communication", "wireless", "internet",
                                    "service provider"],
    "Transportation and Logistics Industry": ["transportation", "logistics", "shipping", "supply chain", "warehouse",
                                              "distribution", "freight"],
    "Sports Industry": ["sports", "athletics", "fitness", "coach", "sports management", ]}
