#!/usr/bin/env python3
import sys
import json

def generate_research_data(company_name):
    """Generate mock research data for the given company"""
    return {
        "Company": company_name,
        "TripAdivsor": {
            "Average Reviews Score": 4.5,
            "Reviews Scores Distrib": {
                "5_stars": 41,
                "4_stars": 32,
                "3_stars": 12,
                "2_stars": 5,
                "1_star": 10
            },
            "Sample Reviews": [
                "Great experience with this company!",
                "Good service but a bit pricey.",
                "Would recommend to others."
            ]
        },
        "GoogleMaps": {
            "Average Reviews Score": 5.6,
            "Reviews Scores Distrib": {
                "5_stars": 31,
                "4_stars": 22,
                "3_stars": 12,
                "2_stars": 15,
                "1_star": 20
            },
            "Sample Reviews": [
                "Excellent customer service.",
                "The staff was very helpful.",
                "Quick response to our inquiry."
            ]
        }
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Company name is required", "Company": ""}))
        sys.exit(1)
    
    company_name = sys.argv[1]
    research_data = generate_research_data(company_name)
    print(json.dumps(research_data, indent=2))

if __name__ == "__main__":
    main()
