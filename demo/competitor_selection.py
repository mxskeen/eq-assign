import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xray import XRaySession, FilterResult, Evaluation
from xray.serializer import save_trace
from demo.mock_data import REFERENCE_PRODUCT, CANDIDATE_PRODUCTS, GENERATED_KEYWORDS


class CompetitorSelectionPipeline:
    # 3-step pipeline for selecting competitor products with X-Ray tracing.
    
    def __init__(self, reference_product: dict):
        self.reference_product = reference_product
        self.filter_config = {
            "price_multiplier_min": 0.5,
            "price_multiplier_max": 2.0,
            "min_rating": 3.8,
            "min_reviews": 100
        }
        
    def run(self) -> dict:
        # Execute pipeline and return selected competitor with trace.
        with XRaySession(
            name="competitor_selection",
            metadata={
                "reference_asin": self.reference_product["asin"],
                "reference_title": self.reference_product["title"]
            }
        ) as session:
            
            keywords = self._step1_generate_keywords(session)
            candidates = self._step2_search_candidates(session, keywords)
            selected = self._step3_apply_filters_and_rank(session, candidates)
            
            trace_path = save_trace(session, "traces/competitor_selection.json")
            
            return {
                "selected_competitor": selected,
                "trace_path": trace_path,
                "session": session
            }
    
    def _step1_generate_keywords(self, session: XRaySession) -> list[str]:
        # Step 1: Generate search keywords using LLM.
        with session.step("keyword_generation", step_type="llm") as step:
            step.set_input({
                "product_title": self.reference_product["title"],
                "category": self.reference_product["category"],
                "model": "gpt-4"
            })
            
            keywords = GENERATED_KEYWORDS
            
            step.set_output({
                "keywords": keywords,
                "keyword_count": len(keywords)
            })
            
            step.set_reasoning(
                "Analyzed product title to extract key attributes: "
                "material (stainless steel), capacity (1000ml), "
                "feature (insulated). Generated keyword variations "
                "combining these attributes with common search patterns."
            )
            
            return keywords
    
    def _step2_search_candidates(self, session: XRaySession, keywords: list[str]) -> list[dict]:
        # Step 2: Search for candidates using API.
        with session.step("candidate_search", step_type="api") as step:
            step.set_input({
                "keywords": keywords,
                "primary_keyword": keywords[0],
                "limit": 50
            })
            
            candidates = CANDIDATE_PRODUCTS
            
            step.set_output({
                "total_results_available": 2847,
                "candidates_fetched": len(candidates),
                "sample_candidates": [
                    {
                        "asin": c["asin"],
                        "title": c["title"],
                        "price": c["price"],
                        "rating": c["rating"],
                        "reviews": c["reviews"]
                    }
                    for c in candidates[:5]
                ]
            })
            
            step.set_reasoning(
                f"Searched using primary keyword '{keywords[0]}'. "
                f"Found 2,847 total matches in the catalog. "
                f"Retrieved top {len(candidates)} results ranked by relevance score. "
                "Results include a mix of branded and generic products."
            )
            
            return candidates
    
    def _step3_apply_filters_and_rank(self, session: XRaySession, candidates: list[dict]) -> dict:
        # Step 3: Apply filters and select best competitor.
        with session.step("apply_filters_and_rank", step_type="filter") as step:
            ref = self.reference_product
            config = self.filter_config
            
            min_price = ref["price"] * config["price_multiplier_min"]
            max_price = ref["price"] * config["price_multiplier_max"]
            
            step.set_input({
                "candidates_count": len(candidates),
                "reference_product": {
                    "asin": ref["asin"],
                    "title": ref["title"],
                    "price": ref["price"],
                    "rating": ref["rating"],
                    "reviews": ref["reviews"]
                },
                "filter_config": {
                    "price_range": {
                        "min": round(min_price, 2),
                        "max": round(max_price, 2),
                        "rule": f"{config['price_multiplier_min']}x - {config['price_multiplier_max']}x of reference price"
                    },
                    "min_rating": {
                        "value": config["min_rating"],
                        "rule": f"Must be at least {config['min_rating']} stars"
                    },
                    "min_reviews": {
                        "value": config["min_reviews"],
                        "rule": f"Must have at least {config['min_reviews']} reviews"
                    }
                }
            })
            
            qualified_candidates = []
            
            for candidate in candidates:
                evaluation = Evaluation(
                    candidate_id=candidate["asin"],
                    candidate_data={
                        "asin": candidate["asin"],
                        "title": candidate["title"],
                        "price": candidate["price"],
                        "rating": candidate["rating"],
                        "reviews": candidate["reviews"],
                        "category": candidate.get("category", "Unknown")
                    }
                )
                
                price_passed = min_price <= candidate["price"] <= max_price
                evaluation.add_filter_result(FilterResult(
                    filter_name="price_range",
                    passed=price_passed,
                    detail=self._get_price_detail(candidate["price"], min_price, max_price),
                    expected=f"INR {min_price:.0f} - INR {max_price:.0f}",
                    actual=f"INR {candidate['price']:.0f}"
                ))
                
                rating_passed = candidate["rating"] >= config["min_rating"]
                evaluation.add_filter_result(FilterResult(
                    filter_name="min_rating",
                    passed=rating_passed,
                    detail=self._get_rating_detail(candidate["rating"], config["min_rating"]),
                    expected=f">= {config['min_rating']}",
                    actual=str(candidate["rating"])
                ))
                
                reviews_passed = candidate["reviews"] >= config["min_reviews"]
                evaluation.add_filter_result(FilterResult(
                    filter_name="min_reviews",
                    passed=reviews_passed,
                    detail=self._get_reviews_detail(candidate["reviews"], config["min_reviews"]),
                    expected=f">= {config['min_reviews']}",
                    actual=str(candidate["reviews"])
                ))
                
                is_actual_product = "Water Bottles" in candidate.get("category", "")
                evaluation.add_filter_result(FilterResult(
                    filter_name="category_match",
                    passed=is_actual_product,
                    detail="Product is in Water Bottles category" if is_actual_product else "Product is an accessory, not a water bottle",
                    expected="Water Bottles category",
                    actual=candidate.get("category", "Unknown")
                ))
                
                all_passed = price_passed and rating_passed and reviews_passed and is_actual_product
                evaluation.qualified = all_passed
                
                if all_passed:
                    score = self._calculate_score(candidate, ref)
                    evaluation.metadata = {
                        "score": round(score, 3),
                        "score_breakdown": {
                            "review_score": round(min(candidate["reviews"] / 10000, 1.0), 3),
                            "rating_score": round((candidate["rating"] - 3.5) / 1.5, 3),
                            "price_proximity": round(1 - abs(candidate["price"] - ref["price"]) / ref["price"], 3)
                        }
                    }
                    qualified_candidates.append((candidate, score, evaluation))
                
                step.add_evaluation(evaluation)
            
            passed_count = len(qualified_candidates)
            failed_count = len(candidates) - passed_count
            
            if qualified_candidates:
                qualified_candidates.sort(key=lambda x: x[1], reverse=True)
                selected = qualified_candidates[0][0]
                
                step.set_output({
                    "total_evaluated": len(candidates),
                    "passed": passed_count,
                    "failed": failed_count,
                    "selected_competitor": {
                        "asin": selected["asin"],
                        "title": selected["title"],
                        "price": selected["price"],
                        "rating": selected["rating"],
                        "reviews": selected["reviews"],
                        "score": qualified_candidates[0][1]
                    },
                    "top_3_candidates": [
                        {
                            "rank": i + 1,
                            "asin": c[0]["asin"],
                            "title": c[0]["title"],
                            "score": round(c[1], 3)
                        }
                        for i, c in enumerate(qualified_candidates[:3])
                    ]
                })
                
                step.set_reasoning(
                    f"Applied 4 filters to {len(candidates)} candidates. "
                    f"{passed_count} passed all filters, {failed_count} were eliminated. "
                    f"Selected '{selected['title']}' as the best competitor based on "
                    f"composite score (reviews: {selected['reviews']}, "
                    f"rating: {selected['rating']}, price proximity to reference)."
                )
                
                return selected
            else:
                step.set_output({
                    "total_evaluated": len(candidates),
                    "passed": 0,
                    "failed": len(candidates),
                    "selected_competitor": None
                })
                
                step.set_reasoning(
                    f"Applied 4 filters to {len(candidates)} candidates. "
                    "No candidates passed all filters. Consider relaxing filter criteria."
                )
                
                return None
    
    def _get_price_detail(self, price: float, min_price: float, max_price: float) -> str:
        if price < min_price:
            return f"INR {price:.0f} is below minimum INR {min_price:.0f}"
        if price > max_price:
            return f"INR {price:.0f} exceeds maximum INR {max_price:.0f}"
        return f"INR {price:.0f} is within INR {min_price:.0f} - INR {max_price:.0f} range"
    
    def _get_rating_detail(self, rating: float, min_rating: float) -> str:
        if rating < min_rating:
            return f"Rating {rating} is below {min_rating} threshold"
        return f"Rating {rating} meets {min_rating} minimum"
    
    def _get_reviews_detail(self, reviews: int, min_reviews: int) -> str:
        if reviews < min_reviews:
            return f"{reviews} reviews is below {min_reviews} minimum"
        return f"{reviews} reviews meets {min_reviews} minimum"
    
    def _calculate_score(self, candidate: dict, reference: dict) -> float:
        # Calculate composite score: 40% reviews, 35% rating, 25% price (weighted).
        review_score = min(candidate["reviews"] / 10000, 1.0)
        rating_score = (candidate["rating"] - 3.5) / 1.5
        price_diff = abs(candidate["price"] - reference["price"]) / reference["price"]
        price_proximity = max(0, 1 - price_diff)
        
        return round(review_score * 0.40 + rating_score * 0.35 + price_proximity * 0.25, 3)
