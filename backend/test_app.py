#!/usr/bin/env python3
"""
Simple test script for Truth Weaver
"""

def test_imports():
    """Test all imports"""
    try:
        from pipeline import preprocess, stt, postprocess, analyze, output
        print("✅ All pipeline modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_analysis():
    """Test the analysis pipeline with sample text"""
    try:
        from pipeline import analyze
        
        # Sample transcript from the project description
        sample_transcript = """
        I've mastered Python for 6 years... built incredible systems...
        Actually... maybe 3 years? Still learning advanced...
        LED A TEAM OF FIVE! EIGHT MONTHS! MACHINE LEARNING!
        I... I work alone mostly... never been comfortable with... with people...
        Just 2 months debugging... I'm not... I'm not what they think...
        """
        
        revealed_truth, deception_patterns = analyze.extract_truth(sample_transcript, "phoenix_2024")
        
        print("✅ Analysis pipeline working!")
        print(f"📊 Revealed Truth: {revealed_truth}")
        print(f"🕵️ Deception Patterns: {deception_patterns}")
        return True
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_output():
    """Test output generation"""
    try:
        from pipeline import output
        
        revealed_truth = {
            "programming_experience": "3-4 years",
            "programming_language": "python",
            "skill_mastery": "intermediate",
            "leadership_claims": "fabricated",
            "team_experience": "individual contributor",
            "skills and other keywords": ["Machine Learning"]
        }
        
        deception_patterns = [
            {
                "lie_type": "experience_inflation",
                "contradictory_claims": ["6 years", "3 years"]
            }
        ]
        
        result = output.generate_json("", revealed_truth, deception_patterns, "phoenix_2024")
        print("✅ Output generation working!")
        print(f"📄 Generated JSON: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Output error: {e}")
        return False

def main():
    """Run all tests"""
    print("🕵️ Truth Weaver - Testing Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Analysis Test", test_analysis),
        ("Output Test", test_output)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Truth Weaver is ready!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
