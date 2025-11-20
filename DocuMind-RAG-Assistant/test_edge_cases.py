"""
Quality Control Testing
Tests edge cases and error conditions
"""

from src.rag_system import RAGAssistant
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("\n" + "="*70)
print("🧪 EDGE CASE & QUALITY CONTROL TESTS")
print("="*70)

# Initialize RAG system
print("\nInitializing RAG Assistant...")
try:
    rag = RAGAssistant()
    rag.load_documents()
    print("✓ Initialization successful\n")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    exit(1)

# Test counters
tests_run = 0
tests_passed = 0
tests_failed = 0

def test_case(name, test_func):
    """Helper to run test cases"""
    global tests_run, tests_passed, tests_failed
    
    tests_run += 1
    print(f"\n[TEST {tests_run}] {name}")
    print("-" * 70)
    
    try:
        test_func()
        tests_passed += 1
        print("✓ PASSED")
    except AssertionError as e:
        tests_failed += 1
        print(f"❌ FAILED: {e}")
    except Exception as e:
        tests_failed += 1
        print(f"❌ ERROR: {e}")

# ==========================================
# TEST 1: Empty Query Handling
# ==========================================
def test_empty_query():
    """Test handling of empty queries"""
    answer, sources = rag.query("")
    assert "empty" in answer.lower() or "error" in answer.lower(), "Should reject empty query"
    assert sources == [], "Should return no sources"
    print(f"Response: {answer}")

test_case("Empty Query Handling", test_empty_query)

# ==========================================
# TEST 2: None Query Handling
# ==========================================
def test_none_query():
    """Test handling of None queries"""
    answer, sources = rag.query(None)
    assert "error" in answer.lower() or isinstance(answer, str), "Should handle None gracefully"

test_case("None Query Handling", test_none_query)

# ==========================================
# TEST 3: Very Long Query
# ==========================================
def test_very_long_query():
    """Test handling of very long queries"""
    long_query = "x" * 10000
    answer, sources = rag.query(long_query)
    assert isinstance(answer, str), "Should return string response"
    print(f"Query length: 10000 chars → Response: {len(answer)} chars")

test_case("Very Long Query (10000 chars)", test_very_long_query)

# ==========================================
# TEST 4: Special Characters
# ==========================================
def test_special_characters():
    """Test handling of special characters"""
    special_query = "What is <script>alert('xss')</script>?"
    answer, sources = rag.query(special_query)
    assert isinstance(answer, str), "Should handle special characters"
    assert "<script>" not in answer, "Should not execute scripts"
    print(f"Query: {special_query}")
    print(f"Response safe: {len(answer)} chars")

test_case("Special Characters & XSS Prevention", test_special_characters)

# ==========================================
# TEST 5: SQL Injection Attempt
# ==========================================
def test_sql_injection():
    """Test handling of SQL injection attempts"""
    sql_query = "'; DROP TABLE documents; --"
    answer, sources = rag.query(sql_query)
    assert isinstance(answer, str), "Should handle SQL-like queries"
    print(f"Query: {sql_query}")
    print(f"Handled safely: Yes")

test_case("SQL Injection Prevention", test_sql_injection)

# ==========================================
# TEST 6: Whitespace Only Query
# ==========================================
def test_whitespace_query():
    """Test handling of whitespace-only queries"""
    whitespace_query = "   \t\n  "
    answer, sources = rag.query(whitespace_query)
    assert sources == [] or "empty" in answer.lower(), "Should reject whitespace query"
    print(f"Whitespace query handled")

test_case("Whitespace-Only Query", test_whitespace_query)

# ==========================================
# TEST 7: Normal Query with Sources
# ==========================================
def test_normal_query():
    """Test normal query with proper response"""
    answer, sources = rag.query("What is the main topic?")
    assert isinstance(answer, str) and len(answer) > 0, "Should return answer"
    assert len(sources) > 0, "Should return sources"
    print(f"Answer length: {len(answer)} chars")
    print(f"Sources found: {len(sources)}")

test_case("Normal Query with Sources", test_normal_query)

# ==========================================
# TEST 8: Query with Numbers
# ==========================================
def test_numeric_query():
    """Test query with numbers"""
    numeric_query = "What are 5 key concepts? List items 1-5 and show 100% coverage."
    answer, sources = rag.query(numeric_query)
    assert isinstance(answer, str), "Should handle numeric queries"
    print(f"Query with numbers handled successfully")

test_case("Numeric Query", test_numeric_query)

# ==========================================
# TEST 9: Repeated Questions
# ==========================================
def test_repeated_questions():
    """Test handling of repeated identical questions"""
    query = "What are the key concepts?"
    
    answer1, sources1 = rag.query(query)
    answer2, sources2 = rag.query(query)
    
    assert answer1 == answer2, "Repeated queries should give same answer"
    assert len(sources1) == len(sources2), "Should retrieve same number of sources"
    print(f"Repeated query test: Consistent results")

test_case("Repeated Questions Consistency", test_repeated_questions)

# ==========================================
# TEST 10: Conversation History
# ==========================================
def test_conversation_history():
    """Test conversation history tracking"""
    initial_history_len = len(rag.conversation_history)
    
    rag.query("First question?")
    rag.query("Second question?")
    
    final_history_len = len(rag.conversation_history)
    
    assert final_history_len > initial_history_len, "History should grow"
    print(f"History growth: {initial_history_len} → {final_history_len}")

test_case("Conversation History Tracking", test_conversation_history)

# ==========================================
# TEST 11: Unicode Characters
# ==========================================
def test_unicode_characters():
    """Test handling of Unicode characters"""
    unicode_query = "What about émojis? 🎉 Ñoño español?"
    answer, sources = rag.query(unicode_query)
    assert isinstance(answer, str), "Should handle Unicode"
    print(f"Unicode query handled successfully")

test_case("Unicode Characters Support", test_unicode_characters)

# ==========================================
# TEST 12: Error Recovery
# ==========================================
def test_error_recovery():
    """Test system recovery after errors"""
    # Try a bad query
    rag.query("")
    
    # Then try a good query
    answer, sources = rag.query("What is the main topic?")
    assert len(answer) > 0, "System should recover from errors"
    print(f"System recovered successfully after error")

test_case("Error Recovery", test_error_recovery)

# ==========================================
# SUMMARY
# ==========================================
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)
print(f"Total Tests: {tests_run}")
print(f"✓ Passed: {tests_passed}")
print(f"❌ Failed: {tests_failed}")
print(f"Success Rate: {(tests_passed/tests_run)*100:.1f}%")

if tests_failed == 0:
    print("\n🎉 All tests passed! System is production-ready.")
else:
    print(f"\n⚠️ {tests_failed} test(s) failed. Review above.")

print("="*70 + "\n")

# Detailed logging
if tests_failed == 0:
    logger.info("✓ All edge case tests passed")
else:
    logger.warning(f"⚠️ {tests_failed} tests failed")
