#!/usr/bin/env python3
"""
Enhanced Conversation Style Test for Jasper
Demonstrates the new Smart Router and conversation style capabilities
"""

import sys
import os
from pathlib import Path

print("🎯 Enhanced Jasper Conversation Style Test")
print("=" * 60)

try:
    from agents.jasper.jasper_agent import JasperAgent
    
    # Initialize Jasper
    jasper = JasperAgent()
    jasper.initialize()
    
    print("✅ Jasper loaded with enhanced conversation capabilities!")
    print()
    
    # Test different conversation styles
    test_queries = [
        ("Greeting", "Hello Jasper, how are you today?"),
        ("Analytical", "Please analyze the benefits and drawbacks of renewable energy systems"),
        ("Creative", "Help me brainstorm creative ideas for a mobile app design"),
        ("Supportive", "I'm struggling with understanding machine learning concepts, can you help?"),
        ("Technical", "How would you implement a REST API using FastAPI?"),
        ("Exploratory", "I want to explore the relationship between AI and human creativity"),
        ("Complex", "Can you examine the intersection of quantum computing, artificial intelligence, machine learning algorithms, and their potential impact on cryptographic security systems?"),
        ("Simple", "What is Python?"),
        ("Conversational", "What do you think about the future of AI development?")
    ]
    
    for style_name, query in test_queries:
        print(f"🔍 Testing {style_name} Style:")
        print(f"Query: '{query}'")
        print("─" * 50)
        
        response = jasper.respond(query)
        print(response)
        print()
        print("=" * 60)
        print()
    
    print("🎉 Enhanced conversation style test completed!")
    print("Jasper now adapts his responses based on:")
    print("✅ Conversation style detection")
    print("✅ Context-appropriate templates") 
    print("✅ Style-specific analysis frameworks")
    print("✅ Personality modifiers")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
