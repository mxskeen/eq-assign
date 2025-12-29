# Demo Runner
# entry point for running the competitor selection pipeline.

from demo.competitor_selection import CompetitorSelectionPipeline
from demo.mock_data import REFERENCE_PRODUCT


def main():
    print("X-Ray Demo: Competitor Selection Pipeline")

    
    print(f"\nReference Product: {REFERENCE_PRODUCT['title']}")
    print(f"  ASIN: {REFERENCE_PRODUCT['asin']}")
    print(f"  Price: INR {REFERENCE_PRODUCT['price']}")
    print(f"  Rating: {REFERENCE_PRODUCT['rating']} stars")
    print(f"  Reviews: {REFERENCE_PRODUCT['reviews']}")
    
    print("\nRunning pipeline...")
    
    pipeline = CompetitorSelectionPipeline(REFERENCE_PRODUCT)
    result = pipeline.run()
    
    print("\nPipeline completed!")
    
    if result["selected_competitor"]:
        selected = result["selected_competitor"]
        print(f"\nSelected Competitor: {selected['title']}")
        print(f"  ASIN: {selected['asin']}")
        print(f"  Price: INR {selected['price']}")
        print(f"  Rating: {selected['rating']} stars")
        print(f"  Reviews: {selected['reviews']}")
    else:
        print("\nNo competitor found matching all criteria.")
    
    print(f"\nX-Ray trace saved to: {result['trace_path']}")
    print("\nTo view the trace, start the dashboard and open the trace file.")
    
    return result


if __name__ == "__main__":
    main()
